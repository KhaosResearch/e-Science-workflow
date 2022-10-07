# Name
Aemet Stations

# Version
1.0

# Author
Khaos Research Group

# Description
Download meteorological data from AEMET for multiple Stations.

# Docker
## Build
```shell
docker build -t enbic2lab/air/aemet_station_weather_attributes -f AemetStationWeatherAttributes.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/aemet_station_weather_attributes --aemet-api-key "Aemet api Key" --start-date "2010-01-01" --end-date "2015-09-01" --analysis-stations "6155A" --analysis-stations "6172O" --analysis-stations "6156X"
```

### Parameters
* --start-date (str) -> First date of the date range, format (yyyy-mm-dd).
* --end-date (str) -> Last date of the date range, format (yyyy-mm-dd).
* --analysis-stations (List[str]) -> Station list for AEMET data search.
* --aemet-api-key (str) -> Api Key providing by AEMET web page (https://opendata.aemet.es/centrodedescargas/altaUsuario?).

### Outputs
* stations_weather_attributes.json
