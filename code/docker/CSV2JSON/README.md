# NAME
CSV to JSON

# Version
1.0

# Author
Khaos Research Group

# Description
Convert a CSV file into JSON file.

# Docker
## Build
```shell
docker build -t enbic2lab/generic/csv2json -f CSV2JSON.dockerfile . 
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/generic/csv2json --input-filepath "best_6155A_aemet_pollen_meteo_taxus_data_updated_mean_interpolation_statistics.csv" --delimiter ";"
```

### Parameters
* --input-filepath (str) -> Filepath for the input CSV File.
* --delimiter (str) -> Delimiter of te input CSV File.

### Outputs
* filename.json