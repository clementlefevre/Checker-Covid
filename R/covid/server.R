#
# This is the server logic of a Shiny web application. You can run the
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

library(data.table)
library(ggplot2)
library(lubridate)
library(plotly)

source('global.R')


# Define server logic required to draw a histogram


shinyServer(function(input, output) {
    
    

    
    country.timeline <- eventReactive(input$country,{
        
        filtered.DT <-      DT[country==input$country]
     
        filtered.DT
    })
    

    output$distPlot <- renderPlot({

        # generate bins based on input$bins from ui.R
        x    <- faithful[, 2]
        bins <- seq(min(x), max(x), length.out = input$bins + 1)

        # draw the histogram with the specified number of bins
        hist(x, breaks = bins, col = 'darkgray', border = 'white')

    })
    
    output$timeline.1 <-  renderPlotly({
        p <- ggplot(country.timeline(),aes(date,value))+geom_line(aes(color=key))
        ggplotly(p)
    })

})
