source("plot_service.R")

shinyServer(function(input, output, session) {
  df <- reactiveVal(NULL)


  # login status and info will be managed by shinyauthr module and stores here
  credentials <- callModule(shinyauthr::login, "login",
    data = user_base,
    user_col = user,
    pwd_col = password,
    sodium_hashed = TRUE,
    log_out = reactive(logout_init())
  )

  # logout status managed by shinyauthr module and stored here
  logout_init <- callModule(shinyauthr::logout, "logout", reactive(credentials()$user_auth))


  # this opens or closes the sidebar on login/logout
  observe({
    if (credentials()$user_auth) {
      shinyjs::removeClass(selector = "body", class = "sidebar-collapse")
    } else {
      shinyjs::addClass(selector = "body", class = "sidebar-collapse")
    }
  })

  # only when credentials()$user_auth is TRUE, render your desired sidebar menu
  output$sidebar <- renderMenu({
    req(credentials()$user_auth)
    sidebarMenu(
      verbatimTextOutput("last_update"),

      pickerInput("country", "country :",
        choices = country.list, multiple = TRUE, selected = c("AT"), options = list(`actions-box` = TRUE)
      ),


      menuItemOutput("dropdown_keys"),
      radioButtons(
        "pop", "value",
        c(
          "Absolute" = "abs",
          "per 100.000 ha" = "per.100.t.ha"
        )
      ),

      menuItem("Chart", tabName = "chart"),
      menuItem("Table", tabName = "table"),
      menuItem("Export data", tabName = "rawdata"),
      menuItem("Patch data", tabName = "importdata"),
      menuItem("About", tabName = "about")
    )
  })

  # outVar <- reactive({
  #   vars <- unique(DT[country %in% input$country]$key)
  #   return(sort(vars))
  # })

  output$last_update <-
    renderText({
      paste0("lastUpdate : ", max(DT$date))
    })


  country.timeline <-
    eventReactive(c(input$country, input$key), {
      filtered.DT <-
        DT[(country %in% input$country) &
          (key == input$key)]

      filtered.DT
    })

  output$timeline.1 <- renderPlotly({
    req(credentials()$user_auth)
    data <- country.timeline()

    if (input$pop == "per.100.t.ha") {
      data$value <- data$value * 100000 / data$population
    }

    fig <- plotlyChart(data, input)
    fig
  })

  output$table <- DT::renderDataTable({
    req(credentials()$user_auth)
    if (input$show.all.keys == FALSE) {
      data <- country.timeline()
    } else {
      data <- DT[country %in% input$country]
    }
    data <-
      data[(date >= input$date.from) &
        (date <= input$date.to)]

    DT::datatable(castTable(data), rownames = FALSE, options = list(pageLength = 15)) %>% 
      formatDate("updated_on", method = "toLocaleString") %>%
      formatDate("date", method = "toLocaleDateString")
  })

  output$dropdown_keys <- renderUI({
    pickerInput("key",
      "key :",
      # choices = levels(outVar()),
      choices = levels(keys.list),
      multiple = FALSE
    )
  })

  output$downloadXLSX <- downloadHandler(
    filename = function() {
      paste("checker_covid_export_", Sys.Date(), ".xlsx", sep = "")
    },
    content = function(file) {
      write_xlsx(
        DT,
        file
      )
    }
  )

  output$downloadImportTemplate <- downloadHandler(
    filename = function() {
      "import_template.xlsx"
    },
    content = function(file) {
      df.import <- setNames(data.frame(matrix(ncol = 4, nrow = 0)), c("date", "country", "key", "value"))
      write_xlsx(
        df.import,
        file
      )
    }
  )


  observeEvent(input$do_update, {
    showModal(modalDialog("Patching with all files...", footer = NULL))
    DT <<- patchAllData()
    update_options()

    removeModal()
    shinyjs::reset("form")
    shinyalert("OK.", "data have been updated.", type = "success")
  })


  output$contents <- renderDataTable({

    # input$file1 will be NULL initially. After the user selects
    # and uploads a file, head of that data file by default,
    # or all rows if selected, will be shown.

    req(input$file1)
    df.from.file <- NULL

    # when reading semicolon separated files,
    # having a comma separator causes `read.csv` to error
    tryCatch(
      {
        df.from.file <- readxl::read_xlsx(input$file1$datapath)
      },
      error = function(e) {
        # return a safeError if a parsing error occurs
        stop(safeError(e))
      }
    )

    df.from.file$date <- as_date(df.from.file$date, tz = "Europe/Berlin")
    df(df.from.file)

    table <- DT::datatable(df(), rownames = FALSE) %>% formatStyle(names(df()),
      backgroundColor = "lightgreen"
    )
    return(table)
  })

  # show hide import file button and update
  observe({
    shinyjs::hide("action")

    if (!is.null(df())) {
      shinyjs::show("action")
    }
  })

  output$do_update <- renderUI({
    req(credentials()$info$permissions == "admin")
    actionButton(
      "do_update",
      "Repatch all"
    )
  })

  observeEvent(input$action, {
    showModal(modalDialog("Patching the data with your file...", footer = NULL))
    DT.to.import <- df()
    setDT(DT.to.import)
    user_name <- credentials()$info$user[1]
    ts <- now() %>%
      as.numeric(.) %>%
      round(0)
    DT.to.import$ts <- ts
    file_import_name <- paste0("patch_", ts, "_", user_name, ".csv.gz")

    DT.to.import[, updated_on := as_datetime(ts, tz = "Europe/Berlin")]

    DT.to.import$source_url <- paste0("patched by ", user_name, " via excel import.")

    saveDTtoS3(DT.to.import, file_import_name)
    DT <<- patchSingle(DT, DT.to.import)
    update_options()
    
    removeModal()
    shinyjs::reset("form")
    shinyalert("OK.", "data have been patched.", type = "success")
  })
})
