# Name
Series Completion 

# Version
1.0.0

# Author
Khaos Research Group

# Description

```
Completion of data time series using a linear regression.
```

# Docker
## Build
```shell
docker build -t enbic2lab/water/series_completion -f SeriesCompletion.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/water/series_completion --filepath "data/Aemet_prec_stations.csv" --start-date "2010-01-01" --end-date "2015-12-31" --target-station "6155A" --analysis-stations "6172O" --analysis-stations "6156X" --completion-criteria "r2" --tests "pettit" --tests "snht" --tests "buishand" --delimiter ";"
```

### Parameters
* --filepath (str) -> File path of the csv file.
* --start-date (str) -> First date of the date range, format (yyyy-mm-dd).
* --end-date (str) -> Last date of the date range, format (yyyy-mm-dd).
* --target-station (str) -> Target station.
* --analysis-stations (List[str]) -> List of stations that will be used to complete the target station.
* --completion-criteria (List[str]) -> List of criteria that will be used to complete the target station. Values that can be included in the list are 'r2','slope','pair'.
* --tests (List[str]) -> Homogeneity tests. Values that can be included in the list are 'pettit','snht','buishand'.
* --delimiter (str) -> Delimiter of the input file and output file. Must be the same

### Outputs
* {station}_completed.csv
* CompletedData.csv
* HomogeneityTests.csv
* StationAnalysis.csv