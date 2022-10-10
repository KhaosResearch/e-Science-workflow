# Name
Upload to DB

# Version
1.0

# Author
Khaos Research Group

# Description
Upload pollen + Aemet json file into Mongo database. 

# Docker
## Build
```shell
docker build -t enbic2lab/air/aemet_upload_database -f AemetUpload2DB.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/aemet_upload_database --input-filepath "best_6155A_aemet_pollen_meteo_taxus_data_updated_mean_interpolation_statistics.json" --user "user" --password "password" --path "mongodb://111.111.111.1:11111" --database "pollen" --collection "test_pollen"
```

### Parameters
* --input-filepath (str) -> File path of the JSON file.
* --user (str) -> Username of MongoDB.
* --password (str) -> Password of MongoDB.
* --path (str) -> Path of MongoDB.
* --database (str) -> Database of MongoDB.
* --collection (str) -> Collection of MongoDB.

### Outputs
None
