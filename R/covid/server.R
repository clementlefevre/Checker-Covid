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

source('global.R')


# Define server logic required to draw a histogram


shinyServer(function(input, output,session) {
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
        
        p <-
            ggplot(data, aes(date, value)) + geom_line(aes(color = country,shape=key))
        p <- p   
        
       # ggplotly(p)
        
        fig <- plot_ly(data) 
        fig <-  fig %>% add_trace(x = ~date, y = ~value, type = 'scatter', mode = 'lines+markers',marker = list( size = 5,opacity = 0.5), color=~country,text=~country,
                                  hovertemplate = paste(
                                      "<b>%{text}</b>",
                                      "%{y:,.0f}<br>",
                                      "%{x}<br>"
                                   
                                  ))
        t <- list(
            family = "Arial",
            size = 10,
            color = 'darkgrey')
        
        fig %>% layout(title=input$key,
                                      font=t)
        
        
    })
    
    output$mytable = DT::renderDataTable({
        
        if(input$show.all.keys == FALSE){
            data <- country.timeline() 
        } else{
            data <-  DT[country %in%  input$country]
          
            
        }
     print(input$date.from)
        data[(date >=input$date.from)& (date <=input$date.to)][, c("date", "country", "key", "value")]
    })
    
    output$menuitem <- renderUI({
        pickerInput("key", "key :",
                    choices = outVar(),multiple = FALSE)
    })
    
    output$downloadXLSX <- downloadHandler(
        filename = function() {
            paste("data-", Sys.Date(), ".xlsx", sep="")
        },
        content = function(file) {
            write_xlsx(dcast(unique(DT,by=c("date","country","key")),date+country~key,fill="no data",value.var = c('value','source_url'))[order(country,-date)], file)
        }
    )
    
    observeEvent(input$do_update, {
        DT <-   fread('https://checkercovid.s3.amazonaws.com/all_EU.csv')
        shinyalert("OK.", "data have been updated.", type = "success")
    })
    
})
