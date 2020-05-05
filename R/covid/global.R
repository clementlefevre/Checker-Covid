library(data.table)
library(lubridate)
library(plotly)
library(DT)

print("coucou")

VERSION <- "0.2"

COLS_FOR_TABLE <- c(
  "cases",
  "cum_tests",
  "tested",
  "curr_hospi",
  "cum_hospi",
  "curr_icu",
  "cum_icu",
  "curr_respi",
  "curr_ipc",
  "owid_cases",
  "owid_tested",
  "new_cases",
  "dead",
  "recovered",
  "owid_new_cases",
  "owid_dead",
  "owid_new_dead",
  "owid_new_tested",
  "current_ecmo",
  "new_hospi",
  "new_out",
  "cured",
  "cum_out_hospi",
  "current_out_hospi",
  "cum_dead",
  "cum_tested",
  "curr_tested",
  "tested_positive",
  "infected",
  "curr_cases",
  "curr_dead",
  "new_cases_brutto",
  "new_dead",
  "new_cured",
  "curr_cured",
  "new_suspected_cases",
  "icu_with_al_one_case"
)



loadData <-  function() {
  print("LOADING DATA FROM S3...")
  DT <-  fread('https://checkercovid.s3.amazonaws.com/all_EU.csv')
  #DT <- fread("../../data/cleaned_data_archives/all_EU.csv")
  
 
  DT$date <- ymd(DT$date)
  DT$value <-  as.numeric(DT$value)
  DT <-  DT[!is.na(value)]
  DT <-  DT[!is.na(key)]
  DT <-  unique(DT, by = c("date", "country", "key"))
  
  
  
  DT$key <- factor(DT$key, levels = COLS_FOR_TABLE)
  return(DT)
  
}


DT <-  loadData()


country.list <-  unique(DT$country) %>% sort()
dates.list <-   unique(DT$date) %>% sort(decreasing = TRUE)
keys.list <-  unique(DT$key) %>% sort()

dates.list.labels <- dates.list %>% format(., format = "%d.%m.%Y")
dates.named.list <-
  setNames(as.list(dates.list), dates.list.labels)



castTable <-  function(DT, for.download = FALSE) {
  if (for.download == TRUE) {
    DT.casted <-
      dcast(
        DT,
        date + country ~ key,
        fill = "no data",
        value.var = c('value', 'source_url', 'updated_on')
      )[order(-date)]
    
    
  } else{
    
    DT.casted <-
      dcast(
        DT,
        date + country + updated_on ~ key,
        fill = "no data",
        value.var = c('value')
      )[order(-date)]
  }
  
  return (DT.casted)
}


print("ciao")
