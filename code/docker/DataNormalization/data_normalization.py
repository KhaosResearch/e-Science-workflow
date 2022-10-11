import os
from pathlib import Path
from pickle import dump
from typing import Tuple

import pandas as pd
import typer
from numpy import savetxt
from sklearn.preprocessing import MinMaxScaler


def minmax_scaler(df: pd.DataFrame) -> Tuple[pd.DataFrame, MinMaxScaler]:
    """
    Given a pandas dataframe, it is normalized with MinMaxScaler

    Returns a normalized dataframe and its scaler
    """

    scaler = MinMaxScaler()
    scaler.fit(df)
    scaled_data = scaler.transform(df)
    return scaled_data, scaler


def data_normalization(
    filepath: str = typer.Option(..., help="File path of the csv file"),
    delimiter: str = typer.Option(
        ..., help="Delimiter of the input file and output file. Must be the same"
    ),
):
    """
    Given a pandas dataframe, it's split in two dataframes (features and target) and then they are normalized with MinMaxScaler

    Returns two normalized dataframes (features and target) and their scalers
    """

    os.chdir("data")

    # Read dataframe
    dataframe = pd.read_csv(filepath, sep=delimiter, index_col="date")

    # Split features and target to normalize
    target_df = dataframe[["pollen"]]
    data = dataframe.drop(["pollen"], axis=1)

    scaled_data, scaler = minmax_scaler(data)
    scaled_target, scaler_target = minmax_scaler(target_df)

    # Save numpy array as CSV
    dirname = ""
    filename = "dataset_norm" + "_features"
    filename_target = "dataset_norm" + "_target"
    suffix = ".csv"
    path = Path(dirname, filename).with_suffix(suffix)
    path_target = Path(dirname, filename_target).with_suffix(suffix)

    savetxt(path, scaled_data, delimiter=delimiter)
    savetxt(path_target, scaled_target, delimiter=delimiter)

    # save the scaler
    scaler_suffix = ".pkl"
    scaler_features_path = Path(dirname, "scaler_features").with_suffix(scaler_suffix)
    scaler_target_path = Path(dirname, "scaler_target").with_suffix(scaler_suffix)

    dump(scaler, open(scaler_features_path, "wb"))
    dump(scaler_target, open(scaler_target_path, "wb"))


# ============ MAIN ============
if __name__ == "__main__":
    typer.run(data_normalization)
