# Name
LSTM Visualisation

# Version
1.0

# Author
Khaos Research Group

# Description
Given the complete dataset, the prediction array, pollen type and the start date.

Returns the R2 visualisation of the predictions.

# Docker
## Build
```shell
docker build -t enbic2lab/air/lstm_visualisation -f LSTM_Visualisation.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/lstm_visualisation --filepath "split_dataset.csv" --filepath-prediction "lstm_predictions.csv" --delimiter ";" --start-date "2010-01-01" --n-steps-out 12
```

### Parameters
* --filepath (str) -> File path of the complete dataset csv file.
* --filepath-prediction (str) -> File path of the prediction csv file.
* --delimiter (str) -> Delimiter of the CSV File.
* --start-date (str) -> Start date to visualise the plot.
* --n-steps-out (int) -> Number of steps we want to predict.

### Outputs
* lstm_visualisation.png
