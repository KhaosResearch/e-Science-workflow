# Name
Scale by Months

# Version
1.0

# Author
Khaos Research Group

# Description
Given a Pollen Dataframe by days, it is scaled to months.

# Docker
## Build
```shell
docker build -t enbic2lab/air/scale_by_months -f ScaleByMonths.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/scale_by_months --filepath "best_6155A_aemet_pollen_meteo_taxus_data_updated_mean_interpolation_statistics.csv" --delimiter ";" --date-column "fecha"
```

### Parameters
* --filepath (str) --> File path of the CSV File.
* --delimiter (str) --> Delimiter of the CSV File.
* --date-column (str) --> Name of the date column.

### Outputs
* scaled_dataset.csv
