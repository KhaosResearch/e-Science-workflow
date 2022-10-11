# Name
Lagged Time-series generation 

# Version
1.0

# Author
Khaos Research Group

# Description
Given a pollen dataframe and the number of lags, it produces a lagged dataframe.

# Docker
## Build
```shell
docker build -t enbic2lab/air/lagged_time_series -f LaggedTimeSeries.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/lagged_time_series --filepath "split_dataset.csv" --delimiter ";" --n-lag 12 
```

### Parameters
* --filepath (str) --> File path of the CSV File.
* --delimiter (str) --> Delimiter of the CSV File.
* --n-lag (int) --> Number of lags


### OUTPUTS
* lagged_dataset.csv
