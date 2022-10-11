### NAME
LSTM model building

### VERSION
1.0

### AUTHOR
Khaos Research Group
Sandro Hurtado Requena (sandrohr@uma.es),
María Luisa Antequera (marialan@uma.es)

### DATE
28/09/2022

### DESCRIPTION
Given X_test, y_test and the trained model, make predictions and evaluate the model

Returns the model' metrics 
### DOCKER
#### Build
```shell
docker build -t enbic2lab/air/lstm_evaluation -f LSTM_Evaluation.dockerfile .
```
#### Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/lstm_evaluation --filepath-x "lstm_X_test.npy" --filepath-y "lstm_Y_test.npy" --filepath-model "lstm_model.h5" --filepath-scaler-y "scaler_target.pkl" --delimiter ";" 

```

### PARAMETERS
* filepath_X (str) --> File path of the x_test.
* filepath_y (str) --> File path of the y_test 
* filepath_model (str) --> File path of the model
* filepath_scaler_y (str) --> File path of the Scaler target object used for data normalization
* delimiter (str) --> Delimiter of the CSV File.

### OUTPUTS
* lstm_metrics.csv
* lstm_predictions.csv
