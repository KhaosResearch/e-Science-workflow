# Name
Join Dataset

# Version
1.0

# Author
Khaos Research Group

# Description
Join two csv datasets using columns as keys

# Docker
## Build
```shell
docker build -t enbic2lab/generic/join_dataset -f JoinDataset.dockerfile .
```
## Run
```shell
docker run -v $(pwd)/data:/usr/local/src/data/ docker.io/enbic2lab/generic/join_dataset --first-file-path "6155A_aemet_data.csv" --index-column-first-file "fecha" --second-file-path "munich_taxus_doy.csv" --index-column-second-file "date" --outfile-name "6155A_aemet_pollen_data.csv" --delimiter-file-1 ";" --delimiter-file-2 ";" --delimiter ";" --join-how-parameter "left"
```

### Parameters
* --first-file-path (str) -> File path of the first file.
* --index-column-first-file (str) -> Name of the column of the firs file. This will be use for merge datasets using index column as keys.
* --second-file-path (str) -> File path of the second file.
* --index-column-second-file (str) -> Name of the column of the firs file. This will be use for merge datasets using index column as keys.
* --outfile-name (str) -> Name without extension of the outfile. Example: for data.csv write data.
* --delimiter-file-1 (str) -> Delimiter of the first file.
* --delimiter-file-2 (str) -> Delimiter of the second file.
* --delimiter-outfile (str) -> Delimiter of the output file.
* --join-how-parameter (str) -> How to handle the operation of the two objects.
  * left (DEFAULT): use calling frame’s index (or column if on is specified)
  * right: use other’s index.
  * outer: form union of calling frame’s index (or column if on is specified) with other’s index, and sort it. lexicographically.
  * inner: form intersection of calling frame’s index (or column if on is specified) with other’s index, preserving the order of the calling’s one.

### Outputs
* {namefile}.csv
