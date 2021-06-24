library(tidyverse)
library(leaflet)

junctions <- read.csv(file = "link_positions.csv")
junctions <- junctions %>% distinct(site, .keep_all = TRUE)

missing_junctions <- junctions %>%
  filter(latitude==0 & longitude == 0)

write.csv(missing_junctions,"MissingData.csv", row.names = FALSE)

leaflet(data = junctions) %>% 
  addTiles() %>% 
  addMarkers(~longitude, ~latitude, popup = ~site, label = ~site,
  clusterOptions = markerClusterOptions()
)
