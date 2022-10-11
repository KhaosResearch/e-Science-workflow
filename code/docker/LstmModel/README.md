# Name
LSTM Model Building

# Version
1.0

# Author
Khaos Research Group

# DESCRIPTION
Given some parameters, builds a ConvLSTM model for timeseries analysis.

Returns the built Keras model and X_test, y_test to make predictions.

# Docker
## Build
```shell
docker build -t enbic2lab/air/lstm_model -f LSTM_Model.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/lstm_model --filepath-x "sequences_X.npy" --filepath-y "sequences_Y.csv" --n-neurons 200 --n-steps-in 12 --n-steps-out 12 --delimiter ";"
```

### Parameters
* --filepath-x (str) -> File path of the x_test.
* --filepath-y (str) -> File path of the y_test.
* --n-neurons (int) -> number of neurons to set the model (ej: 100, 200, 500).
* --delimiter (str) -> Delimiter of the CSV File.
* --n-steps-in (int) -> Time window to train the model.
* --n-steps-out (int) -> Period of time to predict.

### Outputs
* lstm_X_test.npy
* lstm_Y_test.npy
* lstm_model.h5
