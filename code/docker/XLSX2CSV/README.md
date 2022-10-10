# Name
XLSX to CSV

# Version
1.0

# Author
Khaos Research Group

# Description
Convert a xlsx file into a csv file

# Docker
## Build
```shell
docker build -t enbic2lab/generic/xlsx2csv -f XLSX2CSV.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/generic/xlsx2csv --filepath "munich_taxus_doy.xlsx" --delimiter ";" --header
```

### Parameters
* --filepath (str) -> Path of the xlsx file.
* --delimiter (str) -> Delimiter of the csv outfile.
* --header/ --no-header ->  Has header or not. 

### Outputs
* filename.csv
