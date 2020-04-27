library(data.table)
library(lubridate)
library(plotly)
library(DT)



DT <-  fread('https://checkercovid.s3.amazonaws.com/all_EU.csv')
DT$date <- ymd(DT$date)
DT$value <-  as.numeric(DT$value)
DT <-  DT[!is.null(value)]


country.list <-  unique(DT$country) %>% sort()
date.list <-   unique(DT$date) %>% sort(decreasing = TRUE)
keys.list <-  unique(DT$key) %>% sort()