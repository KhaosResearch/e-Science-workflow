# Name
SARIMA Visualisation

# Version
1.0

# Author
Khaos Research Group

# Description
Given the prediction array, pollen type and the start date for validation.
Returns the R<sup>2</sup> visualisation.

# Docker
## Build
```shell
docker build -t enbic2lab/air/sarima_visualisation -f SarimaVisualisation.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/sarima_visualisation --filepath "Sarima_Y_test.csv" --filepath-prediction "Sarima_predictions.csv" --delimiter ";" --validation-time "2013-01-01"

```

### Parameters
* --filepath (str) --> File path of X_test csv file
* --filepath-prediction (str) --> File path of Y_test csv file
* --delimiter (str) --> Delimiter of the CSV File.
* --validation-time (str) --> Indicate from which period of time you want to make the validation

### Outputs
* Sarima_visualisation.png