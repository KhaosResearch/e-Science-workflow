### Name
Mean Interpolation

# Version
1.0

# Author
Khaos Research Group

# Description
Fill Nan values using column mean interpolation by range.

# Docker
## Build
```shell
docker build -t enbic2lab/generic/dataframe_mean_interpolation -f dataframe_mean_interpolation.dockerfile . 
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/generic/dataframe_mean_interpolation --filepath "6155A_aemet_pollen_meteo_taxus_data_updated.csv" --delimiter ";" --date-column "fecha" --initial-year "2010" --final-year "2015" --outfile-name "6155A_aemet_pollen_meteo_taxus_data_updated_mean_interpolation"
```

### Parameters
* --filepath (str) --> Filepath for the input CSV File.
* --delimiter (str) --> Delimiter of te input CSV File.
* --date-column (str) --> Name of the date column.
* --initial-year (str) --> Intial year of the dataset.
* --final-year (str) --> Final year of the dataset
* --outfile-name (str) --> Name of the output file.

### OUTPUTS
* {outfile-name}.csv