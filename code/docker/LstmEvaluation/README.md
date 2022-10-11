# Name
LSTM Evaluation

# Version
1.0

# Author
Khaos Research Group

# Description
Given X_test, y_test and the trained model, make predictions and evaluate the model.

Returns the model' metrics.

# Docker
## Build
```shell
docker build -t enbic2lab/air/lstm_evaluation -f LSTM_Evaluation.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/lstm_evaluation --filepath-x "lstm_X_test.npy" --filepath-y "lstm_Y_test.npy" --filepath-model "lstm_model.h5" --filepath-scaler-y "scaler_target.pkl" --delimiter ";" 
```

### Parameters
* --filepath-x (str) -> File path of the x_test.
* --filepath-y (str) -> File path of the y_test 
* --filepath-model (str) -> File path of the model
* --filepath-scaler-y (str) -> File path of the Scaler target object used for data normalization
* --delimiter (str) -> Delimiter of the CSV File.

### Outputs
* lstm_metrics.csv
* lstm_predictions.csv
