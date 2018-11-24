library(tidyverse)

#read csv files
poi <- read_csv(
  "poi.csv",
  col_names = FALSE
)

View(poi)
