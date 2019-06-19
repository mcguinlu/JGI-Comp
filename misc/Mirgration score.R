# Load required packages #######################################################
library(tidyverse)

# Create town -> county -> region dataset ######################################
# Import town list
town.county <- read.csv("data/Towns_List.csv")
town.county <- town.county[which(town.county$Country=="England"),]
town.county <- town.county[,c(1:2)]

# Sourced from here: https://wiki.freecycle.org/UK_Counties_and_Regions
county.region <- data.frame(stringsAsFactors=FALSE,
                            County = c("Bedfordshire", "Berkshire", "Bristol", "Buckinghamshire",
                                       "Cambridgeshire", "Cheshire", "City of London", "Cornwall",
                                       "County Durham", "Cumbria", "Derbyshire", "Devon", "Dorset",
                                       "East Riding of Yorkshire", "East Sussex", "Essex",
                                       "Gloucestershire", "Greater London", "Greater Manchester", "Hampshire",
                                       "Herefordshire", "Hertfordshire", "Isle of Wight", "Kent", "Lancashire",
                                       "Leicestershire", "Lincolnshire", "Merseyside", "Norfolk",
                                       "North Yorkshire", "Northamptonshire", "Northumberland",
                                       "Nottinghamshire", "Oxfordshire", "Rutland", "Shropshire", "Somerset",
                                       "South Yorkshire", "Staffordshire", "Suffolk", "Surrey",
                                       "Tyne and Wear", "Warwickshire", "West Midlands", "West Sussex",
                                       "West Yorkshire", "Wiltshire", "Worcestershire"),
                            Region = c("East", "South East", "South West", "South East", "East",
                                       "West Midlands", "London", "South West", "North East",
                                       "North West", "West Midlands", "South West", "South West",
                                       "Yorkshire & Humber", "South East", "East", "South West", "London",
                                       "North West", "South East", "West Midlands", "East", "South East",
                                       "South East", "North West", "East Midlands", "Yorkshire & Humber",
                                       "North West", "East", "Yorkshire & Humber", "East Midlands",
                                       "North East", "East Midlands", "South East", "East Midlands",
                                       "West Midlands", "South West", "Yorkshire & Humber", "West Midlands",
                                       "East", "South East", "North East", "West Midlands",
                                       "West Midlands", "South East", "Yorkshire & Humber", "South West",
                                       "West Midlands")
)

# Merge above datasets on county column
town.county.region <- merge(town.county, county.region)

# Migration analysis ###########################################################
# Read in required data
data.move <- read.csv("data/Movement data.csv", header = FALSE)

# Remove description of dataset and rename to prevent having to re-read it
data.move <- data.move[18:nrow(data.move),]

# Add first row to column headers and delete first row
colnames(data.move) = make.names(as.character(unlist(data.move[1, ])))
data.move = data.move[-1, ]

data.move <- as_tibble(data.move)

# Students moving to region ####################################################
# Limit dataset to those travelling to HE provider within England
data.into.region <- filter(
  data.move,
  Region.of.HE.provider == "West Midlands" |
    Region.of.HE.provider == "Yorkshire and the Humber" |
    Region.of.HE.provider == "South West" |
    Region.of.HE.provider == "South East" |
    Region.of.HE.provider == "North West" |
    Region.of.HE.provider == "North East" |
    Region.of.HE.provider == "London" |
    Region.of.HE.provider == "East of England"|
    Region.of.HE.provider == "East Midlands"
)

# Create sum of people moving into each region of England
data.into.region <- filter(data.into.region, X4.way.domicile == "All", Level.of.study == "All", Mode.of.study == "All") %>%
  group_by(Academic.Year, Region.of.HE.provider) %>%
  summarise(sum.number = sum(as.numeric(as.character(Number))))

# PLot results
ggplot(data.into.region, aes(x = data.into.region$Region.of.HE.provider, y=data.into.region$sum.number)) +
  geom_bar(stat="identity") +
  coord_flip() +
  labs(x = "Region of HE provider (limited to England)",
       y = "Total number of students moving to this region")


# Students moving from domicile ################################################
# Remove rows corresponding to totals to prevent double counting
data.outof.domicile <- filter(
  data.move,
  Region.of.HE.provider != "Total England" & Region.of.HE.provider != "Total United Kingdom")

# Create sum of people moving from each domicile 
data.outof.domicile <- filter(data.outof.domicile, X4.way.domicile == "All", Level.of.study == "All", Mode.of.study == "All") %>%
  group_by(Academic.Year, Domicile) %>%
  summarise(sum.no = sum(as.numeric(as.character(Number))))

# Need to limit to UK data

# Link migration data to county level ##########################################




countydata.grp <- group_by(countydata, Academic.Year, County) %>%
  summarise(sum.no = sum(sum.no))
