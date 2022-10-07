# Name
Aemet Download

# Version
1.0

# Author
Khaos Research Group

# Description
Create a CSV File with data about an attribute from Aemet for differents stations

# Docker
## Build
```shell
docker build -t enbic2lab/air/aemet_create_stations_dataset -f AemetCreateStationsDataset.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/aemet_create_stations_dataset --json-file "stations_weather_attributes.json" --attribute "prec" --delimiter ";" 
```

### Parameters
* json_file (str) --> JSON file path.
* attribute (str) --> Attribute name from AEMET.
* delimiter (str) --> Delimiter for CSV output file.
  
### Outputs
* Aemet_{attribute}_stations.csv