# Name
Interpolation

# Version
1.0

# Author
Khaos Research Group

# Description
Fill Nan values using pandas interpolation.

# Docker
## Build
```shell
docker build -t enbic2lab/generic/dataframe_interpolation -f DataframeInterpolation.dockerfile . 
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/generic/dataframe_interpolation --filepath "6155A_aemet_pollen_meteo_taxus_data_updated.csv" --delimiter ";" --interpolation-method "spline"
```

### Parameters
* filepath (str) --> Filepath for the input CSV File.
* delimiter (str) --> Delimiter of te input CSV File.
* interpolation-method (str) --> Interpolation technique to use. For mor info see https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.interpolate.html

### OUTPUTS
* {filename}_{interpolation-method}.csv