### NAME
Dataframe Mean Interpolation

### VERSION
1.0

### AUTHOR
Khaos Research Group
Daniel Doblas Jiménez (dandobjim@uma.es)

### DATE
13/12/2021

### DESCRIPTION
Fill Nan values using column mean interpolation by range.

### DOCKER
#### Build
```shell
docker build -t enbic2lab/generic/dataframe_mean_interpolation -f dataframe_mean_interpolation.dockerfile . 
```
#### Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/generic/dataframe_mean_interpolation --filepath "6155A_aemet_pollen_meteo_taxus_data_updated.csv" --delimiter ";" --date-column "fecha" --initial-year "2010" --final-year "2015" --outfile-name "6155A_aemet_pollen_meteo_taxus_data_updated_mean_interpolation"
```

### PARAMETERS
* filepath (str) --> Filepath for the input CSV File.
* delimiter (str) --> Delimiter of te input CSV File.
* date_column (str) --> Name of the date column.
* initial_year (str) --> Intial year of the dataset.
* final_year (str) --> Final year of the dataset
* outfile_name (str) --> Name of the output file.

### OUTPUTS
* filename_mean.csv