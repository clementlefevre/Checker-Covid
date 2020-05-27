library(shinydashboard)
library(shinythemes)
library(shinyWidgets)
library(shinyalert)
library(dashboardthemes)

### creating custom logo object
logo_blue_gradient <- shinyDashboardLogoDIY(
  
  boldText = "Checker"
  ,mainText = "Covid"
  ,textSize = 16
  ,badgeText = "BETA"
  ,badgeTextColor = "white"
  ,badgeTextSize = 2
  ,badgeBackColor = "#40E0D0"
  ,badgeBorderRadius = 3
  
)


dashboardPage(

  # put the shinyauthr logout ui module in here
  dashboardHeader(### changing logo
    
    
    tags$li(class = "dropdown", style = "padding: 8px;", shinyauthr::logoutUI("logout")),
    title =logo_blue_gradient
  ),

  # setup a sidebar menu to be rendered server-side
  dashboardSidebar(
    useShinyalert(),
    collapsed = TRUE, sidebarMenuOutput("sidebar")
  ),


  dashboardBody( ### changing theme
    shinyDashboardThemes(
      theme = "onenote"
    ),
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
      ),
tabItem(
  "about",
 box(h3("For any questions, problem, contact clement.san@gmail.com"))
)
    )
  )
)
