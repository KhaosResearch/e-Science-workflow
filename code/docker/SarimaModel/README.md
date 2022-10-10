# Name
SARIMA Model

# Version
1.0

# Author
Khaos Research Group

# Description
Train SARIMA model with a specific scaled dataset.
Return a trained SARIMA model and X_test, y_test for evaluation metrics.

# Docker
## Build
```shell
docker build -t enbic2lab/air/sarima_model -f SarimaModel.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/sarima_model --filepath "split_dataset.csv" --delimiter ";" --seasonality 12
```

### Parameters
* --filepath (str) --> File path of the CSV File.
* --delimiter (str) --> Delimiter of the CSV File.
* --seasonality (int) --> Set the seasonality of the pollen. 

### Outputs
* Sarima_model.pkl
* Sarima_X_test.csv
* Sarima_Y_test.csv 