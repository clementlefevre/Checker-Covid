library(shiny)
library(shinydashboard)
library(shinyauthr)
library(dplyr)
library(shinyjs)
library(data.table)
library(lubridate)
library(plotly)
library(DT)
library(R.utils)
library(readxl)
library(writexl)
library("aws.s3")

source("cols.R")
source("secret_config.R")
source("patch.R")


dir.create(file.path("./temp"), showWarnings = FALSE)

# sample logins dataframe with passwords hashed by sodium package
user_base <- read.csv("data/users.csv", stringsAsFactors = F) %>% as_tibble()
user_base$password <- sapply(user_base$password, sodium::password_store)

loadData <- function() {
  print("LOADING DATA FROM S3...")


  # if (object_exists("all_EU_patched.csv.gz",
  #   bucket = "checkercovid", key = AWS_ACCESS_KEY_ID,
  #   secret = AWS_SECRET_ACCESS_KEY
  # )) {
  #   print("LOADING all_EU_patched.csv.gz...")
  #   DT <- fread(paste0(ROOT_S3, "all_EU_patched.csv.gz"))
  # }
  # else {
    print("all_EU_patched.csv.gz not found, creating it...")
    DT <- patchAllData()
  #}




  DT <- cleanDT(DT)
  # we add the columns that are not un the COLS_FOR_TABLE avoid NA by setting factor on key :
  missing.cols <- setdiff(unique(DT$key), COLS_FOR_TABLE)

  COLS_FOR_TABLE <- c(COLS_FOR_TABLE, missing.cols)

  DT$key <- factor(DT$key, levels = COLS_FOR_TABLE)

  DT.pop <- fread("data/populations.csv")
  DT <- merge(DT, DT.pop, by.x = "country", by.y = "geo")
  return(DT)
}

update_options <- function() {
  country.list <<- unique(DT$country) %>% sort()
  
  dates.list <<- unique(DT$date) %>% sort(decreasing = TRUE)
  keys.list <<- unique(DT$key) %>% sort()
  
  dates.list.labels <<- dates.list %>% format(., format = "%d.%m.%Y")
  dates.named.list <<-
    setNames(as.list(dates.list), dates.list.labels)
}



castTable <- function(DT, for.download = FALSE) {
  if (for.download == TRUE) {
    DT.casted <-
      dcast(
        DT,
        date + country ~ key,
        fill = "no data",

        value.var = c("value", "source_url", "updated_on")
      )[order(-date)]
  } else {
    DT.casted <-
      dcast(
        DT,
        date + country + updated_on ~ key,
        fill = "no data",
        value.var = c("value")
      )[order(-date)]
  }

  return(DT.casted)
}



saveDTtoS3 <- function(DT, filename) {
  filepath <- paste0("./temp/", filename)
  data.table::fwrite(DT, file = filepath, compress = "gzip")


  aws.s3::put_object(filepath,
    bucket = "checkercovid", object = filename, key = AWS_ACCESS_KEY_ID,
    secret = AWS_SECRET_ACCESS_KEY
  )
  print(paste0(filename, " saved to S3."))

  if (file.exists(filepath)) {
    # Delete file if it exists
    file.remove(filepath)
  }
}

DT <- loadData()

country.list <- NULL
dates.list <- NULL
keys.list <- NULL
dates.list.labels <- NULL
dates.named.list <- NULL


update_options()
