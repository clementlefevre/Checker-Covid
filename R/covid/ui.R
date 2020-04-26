#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#


country.list <-  unique(DT$country)
library(shiny)

# Define UI for application that draws a histogram
shinyUI(fluidPage(

    # Application title
    titlePanel("EuroCoro"),

    # Sidebar with a slider input for number of bins
    sidebarLayout(
        sidebarPanel(
           
            selectInput("country", "country :", 
                        choices=country.list)
        ),

        # Show a plot of the generated distribution
        mainPanel(
           
            plotlyOutput("timeline.1")
        )
    )
))
