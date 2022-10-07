# Name
Split Dataset

# Version
1.0

# Author
Khaos Research Group

# Description
Split the dataset and return another with the columns that you want to keep

# Docker
## Build
```shell
docker build -t enbic2lab/generic/split_dataset -f SplitDataset.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/generic/split_dataset --filepath "6155A_aemet_pollen_data.csv" --outfile-name "6155A_aemet_pollen_meteo_taxus_data_split" --delimiter ";" --attribute-list "fecha"  --attribute-list "tmed" --attribute-list "prec" --attribute-list "tmin" --attribute-list "tmax" --attribute-list "dir" --attribute-list "velmedia" --attribute-list "racha" --attribute-list "sol" --attribute-list "presMax" --attribute-list "presMin" --attribute-list "DOY" --attribute-list "Taxus"
```

### Parameters
* --filepath (str) -> File path of the csv file.
* --attribute-list (List[str]) -> List of attributes that you want to keep.
* --outfile-name (str) -> Name of the output file without extensions.
* --delimiter (str) -> Delimiter of the input file and output file. Must be the same.

### Outputs
* {outfile-name}.csv
