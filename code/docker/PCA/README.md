# Name
Dimensionality Reduction (PCA)

# Version
1.0

# Author
Khaos Research Group

# Description
Given a pandas dataset perform a PCA analysis to select the most important features

# Docker
## Build
```shell
docker build -t enbic2lab/air/pca_analysis -f PCA.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/air/pca_analysis --filepath "lagged_dataset.csv" --delimiter ";" 
```

### Parameter
* filepath (str) --> File path of the CSV File.
* delimiter (str) --> Delimiter of the CSV File.

### Output
* pca_dataset.csv
