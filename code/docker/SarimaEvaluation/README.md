# Name
SARIMA Evaluation

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
docker build -t enbic2lab/air/sarima_evaluation -f SarimaEvaluation.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/sarima_evaluation --filepath-x "Sarima_X_test.csv" --filepath-y "Sarima_Y_test.csv" --filepath-model "Sarima_model.pkl" --delimiter ";" --validation-time "2013-01-01"
```

### Parameters
* --filepath_x (str) -> File path of X_test csv file
* --filepath-y (str) -> File path of Y_test csv file
* --filepath-model (str) -> File path of the Sarima model
* --delimiter (str) -> Delimiter of the CSV File.
* --validation-time (str) -> Indicate from which period of time you want to make the validation

### Outputs
* Sarima_metrics.csv
* Sarima_predictions.csv 