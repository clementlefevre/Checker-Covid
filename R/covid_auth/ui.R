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

        DT::dataTableOutput("table")
      ),

      tabItem(
        "rawdata",
       
        downloadButton("downloadXLSX", "Download all data as XLSX")
      ),
      tabItem(
        "importdata",
       h3("To manually update the dataset, first download the Excel Template, fill it and then upload it:"),
uiOutput("do_update"),br(),hr(),
fluidRow(column(4,h3("1 - Downlad patch template"),downloadButton("downloadImportTemplate", "Download Empty Excel Import File")),
      column(4,     h3("2 - Fill it and Upload it"),   fileInput("file1", "Upload your XLSX File",
                  multiple = FALSE,
                  accept = c("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"))),
      column(4,h3("3 - Patch the data !"),actionButton("action", "Import data", icon("paper-plane"), 
                     style="color: #fff; background-color: #00887d; border-color: #00887d"))),
       br(),br(),
       dataTableOutput("contents")
      )
    )
  )
)
