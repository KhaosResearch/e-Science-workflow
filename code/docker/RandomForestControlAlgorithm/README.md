# Name
Random Forest Control Algorithm

# Version
1.0

# Author
Khaos Research Group

# Description
Execute standard linear regression.

# Docker
## Build
```shell
docker build -t enbic2lab/air/aemet_random_forest_regression -f AemetRandomForestRegression.dockerfile . 
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/aemet_random_forest_regression --filepath "6155A_aemet_pollen_meteo_taxus_data_updated_mean_interpolation_statistics.csv" --delimiter ";" --date-column "fecha" --dependent-variable "Taxus"
```

### Parameters
* --filepath (str) -> Filepath for the input CSV File.
* --delimiter (str) -> Delimiter of te input CSV File.
* --date-column (str) -> Name of the date column.
* --dependent-variable (str) -> Name of the dependent variable column.

### Outputs
* filename_metrics.csv