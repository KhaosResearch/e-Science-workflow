# Name
Update Dataset

# Version
1.0

# Author
Khaos Research Group

# Description
Update a CSV main file using data from another CSV aux file.

# Docker
## Build
```shell
docker build -t enbic2lab/generic/update_dataset -f UpdateDataset.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/generic/update_dataset --first-file "6155A_aemet_pollen_meteo_taxus_data_split.csv" --second-file "6155A_completed.csv" --col-first-file "prec" --col-second-file "6155A" --index-column-first-file "fecha" --index-column-second-file "DATE" --delimiter-first-file ";" --delimiter-second-file ";" --outfile-name "6155A_aemet_pollen_meteo_taxus_data_updated.csv"
```

### Parameters
* --first-file (str) -> Path of the file that will be updataed.
* --second-file (str) -> Path of the aux file used to update the main file.
* --col-first-file (str) -> Column of the main file to be updated.
* --col-second-file (str) -> Column of the aux file used to update de main file.
* --index-column-first-file (str) -> Column of the main file used to join with the aux file as key.
* --index-column-second-file (str) -> Column of the aux file used to join with te main file as key.
* --delimiter-first-file (str) -> Delimiter of the CSV main file.
* --delimiter-second-file (str) -> Delimiter of the CSV aux file.
* --outfile-name (str) -> Name of the output file without extension.

### Outputs
* outfile_name.csv
