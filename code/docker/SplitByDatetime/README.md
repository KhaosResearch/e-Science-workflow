# Name
Split by Datetime

# Version
1.0

# Author
Khaos Research Group

# Description
Given a pandas dataset and start date/end date, select a portion of this dataset.
Date format: 'yyyy-mm-dd'
Returns a portion of the original dataset

# Docker
## Build
```shell
docker build -t enbic2lab/air/split_by_datetime -f SplitByDatetime.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/split_by_datetime --filepath "scaled_dataset.csv" --delimiter ";" --start-date "2010-01-01" --end-date "2015-01-01" --pollen-column "Taxus"

```

### Parameters
* --filepath (str) --> File path of the CSV File.
* --delimiter (str) --> Delimiter of the CSV File.
* --start-date (str) --> Start date to analyse.
* --end-date (str) --> End date to analyse.
* --pollen-column (str) -> Name of the pollen column.

### Outputs
* split_dataset.csv
* seasonal_plot.pdf
