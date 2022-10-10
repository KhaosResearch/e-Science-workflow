# Name
Merge Dataset

# Version
1.0.0

# Author
Khaos Research Group

# Description
Join two CSV files by rows if their columns names are equals.

# Docker
## Build
```shell
docker build -t enbic2lab/generic_components/join_csv_by_rows -f JoinCsvByRows.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/generic_components/join_csv_by_rows --filepath-first "6155A_aemet_pollen_meteo_taxus_data_updated_spline_metrics.csv" --delimiter-first ";" --filepath-second "6155A_aemet_pollen_meteo_taxus_data_updated_mean_interpolation_statistics_metrics.csv" --delimiter-second ";" --outfile-name "6155A_aemet_pollen_meteo_taxus_metrics"
```

### Parameters
* --filepath-first (str) -> Filepath of first CSV file.
* --filepath-second (str) -> Filepath of second CSV file.
* --delimiter-first (str) -> Delimiter of first CSV file.
* --delimiter-second (str) -> Delimiter of second CSV file.
* --outfile-name (str) -> Name of output file.

### Outputs
* {outfile-name}_metrics.csv
```