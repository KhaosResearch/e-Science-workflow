# Name
Aemet Download

# Version
1.0

# Author
Khaos Research Group

# Description
Download meteorological data from AEMET

# Docker
## Build
```shell
docker build -t enbic2lab/air/aemet_download_data -f AemetDownloadData.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/aemet_download_data --start-date "2010-01-01" --end-date "2015-01-01" --station "6155A" --aemet-api-key "API KEY" --delimiter ";"
```

### Parameters
* --start-date (str) -> First date of the date range, format (yyyy-mm-dd).
* --end-date (str) -> Last date of the date range, format (yyyy-mm-dd).
* --station (str) -> Code of the station from AEMET
* --aemet-api-key (str) -> Api Key providing by AEMET web page (https://opendata.aemet.es/centrodedescargas/altaUsuario?).
* --delimiter (str) -> Delimiter of the output CSV File.
  
### Outputs
* {station}_aemet_data.csv
