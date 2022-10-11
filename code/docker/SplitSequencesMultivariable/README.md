# Name
Split Sequence Multivariable

# Version
1.0

# Author
Khaos Research Group

# Description
Generates supervised data from a multidimensional array.

Returns both data and its target for supervised learning.

# Docker
## Build
```shell
docker build -t enbic2lab/air/split_sequences_multivariable -f SplitSequencesMultivariable.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/split_sequences_multivariable --filepath-features "dataset_norm_features.csv" --filepath-target "dataset_norm_target.csv" --delimiter ";" --n-steps-in 12 --n-steps-out 12
```

### Parameters
* --filepath (str) -> File path of the CSV File.
* --delimiter (str) -> Delimiter of the CSV File.
* --n-steps-in (int) -> Time window to train the model
* --n-steps-out (int) -> Period of time to predict

### Outputs
* sequences_X.npy
* sequences_Y.csv
