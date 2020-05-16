#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shinydashboard)
library(shinythemes)
library(shinyWidgets)
library(shinyalert)




dashboardPage( # Set up shinyalert
  dashboardHeader(title = paste0("Checker Covid \n v.", VERSION)),
  dashboardSidebar(
    useShinyalert(),

    sidebarMenu(
      verbatimTextOutput("last_update"),

      pickerInput("country", "country :",
        choices = country.list, multiple = TRUE, selected = c("AT"), options = list(`actions-box` = TRUE)
      ),

      menuItemOutput("menuitem"),
      radioButtons(
        "pop", "value",
        c(
          "Absolute" = "abs",
          "per 100.000 ha" = "per.100.t.ha"
        )
      ),

      menuItem("Dashboard", tabName = "dashboard"),
      menuItem("Table", tabName = "table"),
      menuItem("Download data", tabName = "rawdata")
    )
  ),
  dashboardBody(
    tabItems(
      tabItem(
        "dashboard",

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
      )
    )
  )
)
