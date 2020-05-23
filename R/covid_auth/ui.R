library(shinydashboard)
library(shinythemes)
library(shinyWidgets)
library(shinyalert)


dashboardPage(

  # put the shinyauthr logout ui module in here
  dashboardHeader(
    title = "Checker Covid",
    tags$li(class = "dropdown", style = "padding: 8px;", shinyauthr::logoutUI("logout"))
  ),

  # setup a sidebar menu to be rendered server-side
  dashboardSidebar(
    useShinyalert(),
    collapsed = TRUE, sidebarMenuOutput("sidebar")
  ),


  dashboardBody(
    shinyjs::useShinyjs(),

    # put the shinyauthr login ui module here
    shinyauthr::loginUI("login"),


    tabItems(
      tabItem(
        "chart",

        fluidRow(
          plotlyOutput("timeline.1")
        )
      ),
      tabItem(
        "table",
        fluidRow(
          column(3, pickerInput("date.from", "from :",
            choices = dates.named.list, multiple = FALSE
          )),

          column(
            3,
            pickerInput("date.to", "to :",
              choices = dates.named.list, multiple = FALSE
            )
          ),
          column(3, checkboxInput("show.all.keys", "show all keys", TRUE))
        ),

        DT::dataTableOutput("mytable")
      ),

      tabItem(
        "rawdata",
        actionButton("do_update", "Update Data"),
        downloadButton("downloadXLSX", "Download all data as XLSX")
      ),
      tabItem(
        "importdata",
       h3("To manually update the dataset, please download the Excel Template, fill it and then upload it:"),
        br(),br(),downloadButton("downloadImportTemplate", "Download Empty Excel Import File"),
      
        # Input: Select a file ----
        fileInput("file1", "Choose XLSX File",
                  multiple = FALSE,
                  accept = c("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")),
        actionButton("action", "Import data"),
       dataTableOutput("contents")
      )
    )
  )
)
