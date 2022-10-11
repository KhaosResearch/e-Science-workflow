# Name
Data Normalization

# Version
1.0

# Author
Khaos Research Group

# Description
Given a pandas dataframe, it's split in two dataframes (features and target) and then they are normalized with MinMaxScaler.
    
Returns two normalized dataframes (features and target) and their scalers.

# Docker
## Build
```shell
docker build -t enbic2lab/air/data_normalization -f DataNormalization.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/data_normalization --filepath "pca_dataset.csv" --delimiter ";" 
```

### Parameters
* filepath (str) --> File path of the CSV File.
* delimiter (str) --> Delimiter of the CSV File.

### Outputs
* dataset_norm_features.csv
* scaler_features.pkl
* dataset_norm_target.csv
* scaler_target.pkl
