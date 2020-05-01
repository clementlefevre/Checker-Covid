library(data.table)
library(lubridate)
library(plotly)
library(DT)

VERSION <- "0.2"



DT <-  fread('https://checkercovid.s3.amazonaws.com/all_EU.csv')
DT$date <- ymd(DT$date)
DT$value <-  as.numeric(DT$value)
DT <-  DT[!is.null(value)]


country.list <-  unique(DT$country) %>% sort()
dates.list <-   unique(DT$date) %>% sort(decreasing = TRUE)
keys.list <-  unique(DT$key) %>% sort()

dates.list.labels <- date.list %>% format(.,format="%d.%m.%Y") 
dates.named.list <-  setNames(as.list(dates.list),dates.list.labels)

