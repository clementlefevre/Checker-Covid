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
library(ggthemes)
library(writexl)


# Define server logic required to draw a histogram


shinyServer(function(input, output, session) {
    outVar <- reactive({
        vars <- unique(DT[country %in% input$country]$key)
        
        return(sort(vars))
    })
    
    
    output$last_update <-
        renderText({
            paste0("lastUpdate : ", max(DT$date))
        })
    
    
    country.timeline <-
        eventReactive(c(input$country, input$key) , {
            filtered.DT <-
                DT[(country %in%  input$country) &
                       (key == input$key)]
            filtered.DT
            
        })
    
    
    
    output$timeline.1 <-  renderPlotly({
        data <-  country.timeline()
        
        if (input$pop == "per.100.t.ha") {
            data$value <-  data$value * 100000 / data$pop_2019
        }
        
       
        
        fig <- plot_ly(data)
        fig <-
            fig %>% add_trace(
                x = ~ date,
                y = ~ value,
                type = 'scatter',
                mode = 'lines+markers',
                marker = list(size = 5, opacity = 0.5),
                color =  ~ country,
                text =  ~ country,
                hovertemplate = paste("<b>%{text}</b>",
                                      "%{y:,.0f}<br>",
                                      "%{x}<br>")
            )
        t <- list(family = "Arial",
                  size = 10,
                  color = 'darkgrey')
        
        fig %>% layout(title = input$key,
                       font = t, xaxis = list(range = c(min(data$date), max(data$date))),
        yaxis = list(range = c(0, max(data$value)*1.05)))
        
        
    })
    
    output$mytable = DT::renderDataTable(rownames = FALSE, {
        if (input$show.all.keys == FALSE) {
            data <- country.timeline()
        } else{
            data <-  DT[country %in%  input$country]
        }
        data <-
            data[(date >= input$date.from) &
                     (date <= input$date.to)]
        
        castTable(data)
    })
    
    output$menuitem <- renderUI({
        pickerInput("key",
                    "key :",
                    choices = levels(outVar()),
                    multiple = FALSE)
    })
    
    output$downloadXLSX <- downloadHandler(
        filename = function() {
            paste("data-", Sys.Date(), ".xlsx", sep = "")
        },
        content = function(file) {
            write_xlsx(castTable(DT, for.download = T),
                       file)
        }
    )
    
    observeEvent(input$do_update, {
        loadData()
        shinyalert("OK.", "data have been updated.", type = "success")
    }, ignoreInit = TRUE)

    
    
})
