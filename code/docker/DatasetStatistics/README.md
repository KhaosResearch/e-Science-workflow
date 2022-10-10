# Name
Dataset Statistics

# Version
1.0

# Author
Khaos Research Group

# Description
Create a CSV File with extra columns based on statistics.

### Docker
#### Build
```shell
docker build -t enbic2lab/air/aemet_add_statistics -f AemetAddStatistics.dockerfile .
```
#### Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/aemet_add_statistics --filepath "6155A_aemet_pollen_meteo_taxus_data_updated_mean_interpolation.csv" --delimiter ";" --outfile-name "6155A_aemet_pollen_meteo_taxus_data_updated_mean_interpolation_statistics.csv" --acum-list-attr "prec" --acum-list-attr "tmed" --acum-list-attr "tmax" --acum-list-attr "tmin" --acum-list-attr "sol" --acum-list-attr "presMax" --acum-list-attr "presMin" --acum-list-attr "Taxus" --mm-list-attr "prec" --mm-list-attr "tmed" --mm-list-attr "tmax" --mm-list-attr "tmin" --mm-list-attr "sol" --mm-list-attr "presMax" --mm-list-attr "presMin" --mm-list-attr "Taxus"

```

### Parameters
* filepath (str) --> File path of the CSV File.
* acum-list-attr (List[str]) --> List of attributes for doing statistics with them.
* mm_list_attr (List[str]) --> List of attributes for mm statistic. 
* delimiter (str) --> Delimiter of the CSV File.
* outfile_name (str) --> Name of the output CSV file without extension.

### Outputs
* outfile_name.csv