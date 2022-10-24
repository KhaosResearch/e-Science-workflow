# Name
Stationarity and Seasonality

# Version
1.0

# Author
Khaos Research Group

# Description
Generate differents analysis based on Dickey-Fuller and ARIMA methods.

# Docker
## Build
```
docker build -t enbic2lab/air/arima -f arima.dockerfile .
```
## Run
```
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/arima --filepath "best_6155A_aemet_pollen_meteo_alnus_data_updated_mean_interpolation_statistics.csv" --delimiter ";" --pollen "Taxus" --date-column "fecha" --year 2013
```

### Parameters
* filepath (str) -> File path of the CSV file.
* delimiter (str) -> Delimiter of the CSV file.
* date_column (str) -> Name of the Date column.
* pollen (str) -> Name of the Pollen column.
* year (int) -> Year for decomposition


### Outputs
* SARIMAX_plots.pdf
* DickerFuller_seasonality.csv
* decompose.pdf
* DickeyFuller_plot.png
