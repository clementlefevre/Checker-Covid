library(data.table)
library(lubridate)
library(plotly)

DT <-  fread('../../all_EU.csv')
DT$date <- ymd(DT$date)
DT$value <-  as.numeric(DT$value)


country.list <-  unique(DT$country)
