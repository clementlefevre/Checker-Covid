plotlyChart <- function(data,input){
  data <-  data[order(date)]

fig <- plot_ly(data)
fig <-
  fig %>% add_trace(
    x = ~date,
    y = ~value,
    type = "scatter",
    mode = "lines+markers",
    marker = list(size = 5, opacity = 0.5),
    color = ~country,
    text = ~country,
    hovertemplate = paste(
      "<b>%{text}</b>",
      "%{y:,.0f}<br>",
      "%{x}<br>"
    )
  )
t <- list(
  family = "Arial",
  size = 10,
  color = "darkgrey"
)

final.fig <- fig %>% layout(
  title = input$key,
  font = t, xaxis = list(range = c(min(data$date), max(data$date))),
  yaxis = list(range = c(0, max(data$value) * 1.05))
)
return(final.fig)
}