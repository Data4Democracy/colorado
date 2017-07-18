

unzip("./data/CityOfDenverHousingPermits_2015-2017.zip", "./data/CityOfDenverHousingPermits_2015-2017.csv")

extract.zip(file, extractpath = dirname(file)[1])

data15_17 <- read.csv("./data/CityOfDenverHousingPermits_2015-2017.csv", stringsAsFactors = FALSE)
data15_17$City <- 'Denver'
data15_17$State <- 'Colorado'

data_geo <- data15_17[(data15_17$Permit.Type == "Building Residential Construction" | 
                             data15_17$Permit.Type == "Building Demolition") & !is.na(data15_17$Permit.Type), ]

iter <- round(nrow(data_geo) / 2500)
res <- nrow(data_geo) - iter*2500

# write files to geocoding with QGIS for geocoding using Goodle Maps (not more than 2500 objects per day)
for (i in 0:(iter-1)) {
        if (i < iter-1) {
                subset_data <- data_geo[(i*2500):(i*2500+2499),]
        } else {
                subset_data <- data_geo[(i*2500):(i*2500+res),]
        }
        file_name <- paste0("./geocoding/geocoding",i+1,".csv")
        write.csv(subset_data, file = file_name, row.names = F)
}
