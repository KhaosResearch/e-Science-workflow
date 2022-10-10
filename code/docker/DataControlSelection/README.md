# Name
Data Control Selection

# Version
1.0

# Author
Khaos Research Group

# Description
Select the best CSV by metrics comparison.

# Docker
## Build
```shell
docker build -t enbic2lab/air/choose_metric_csv -f ChooseMetricCSV.dockerfile . 
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/choose_metric_csv --filepath-metrics "6155A_aemet_pollen_meteo_taxus_metrics.csv" --filepath-pandas "6155A_aemet_pollen_meteo_taxus_data_updated_mean_interpolation_statistics.csv" --filepath-mean "6155A_aemet_pollen_meteo_platanus_data_updated_linear_interpolation_statistics.csv" --delimiter ";"
```

### Parameters
* --filepath-metrics (str) --> Filepath of the csv metrics file.
* --filepath-pandas (str) --> Filepath of the pandas interpolation or non-interpolate file.
* --filepath-mean  (str) --> Filepath of the mean interpolation file.
* --delimiter (str) --> Delimiter of the input CSV File.

### OUTPUTS
* best_filename.csv