import os
from pathlib import Path

import pandas as pd
import typer


def lagged_time_series(
    filepath: str = typer.Option(..., help="File path of the csv file"),
    delimiter: str = typer.Option(
        ..., help="Delimiter of the input file and output file. Must be the same"
    ),
    n_lag: int = typer.Option(12, help="Select number of lags"),
):
    """
    Given a pollen dataframe and number of lags, it produces a lagged dataframe

    Returns a lagged dataframe
    """

    os.chdir("data")

    # Read dataframe
    dataframe = pd.read_csv(filepath, sep=delimiter, index_col="date")

    df_k = dataframe[["pollen"]]

    # remove target column
    df = dataframe.drop(["pollen"], axis=1)
    df_atr = dataframe[df.columns]
    lags = range(1, int(n_lag) + 1)

    final_df = df_atr.assign(
        **{f"{col} (t-{lag})": df_atr[col].shift(lag) for lag in lags for col in df_atr}
    )

    final_df["pollen"] = df_k["pollen"]

    # Remove nan values inserted by lags in the n lags firts rows
    final_df = final_df.dropna()

    # Save Outfile
    dirname = ""
    filename = "lagged_dataset"
    suffix = ".csv"
    path = Path(dirname, filename).with_suffix(suffix)

    final_df.to_csv(path, sep=delimiter)


# ============ MAIN ============
if __name__ == "__main__":
    typer.run(lagged_time_series)
