import os
from pathlib import Path

import pandas as pd
import typer


# ======== METHOD ========
def choose_metric_csv(
    filepath_metrics: str = typer.Option(..., help="Filepath of the csv metrics file"),
    filepath_pandas: str = typer.Option(
        ..., help="Filepath of the pandas interpolate file"
    ),
    filepath_mean: str = typer.Option(
        ..., help="Filepath of the mean interpolate file"
    ),
    delimiter: str = typer.Option(..., help="Delimiter of the csv file"),
):
    os.chdir("data")

    df = pd.read_csv(filepath_metrics, delimiter=delimiter)

    best_file = ""

    best_r2_ = df["r2_mean"].idxmax()
    best_mae_mean = df["mae_mean"].idxmin()
    best_rmse_mean = df["rmse_mean"].idxmin()
    best_rmse_mae_mean = df["rmse_mae_mean"].idxmin()

    list_best = [best_r2_, best_mae_mean, best_rmse_mean, best_rmse_mae_mean]

    dict_ocurrence = dict()
    for index, row in df.iterrows():
        dict_ocurrence[index] = list_best.count(index)

    ocurrence_values = list(dict_ocurrence.values())
    max_ocurrence = max(ocurrence_values)
    count_max_ocurrence = ocurrence_values.count(max_ocurrence)

    if count_max_ocurrence == 1:
        indx = ocurrence_values.index(max_ocurrence)
        best_file = df["filename"].iloc[indx] + ".csv"
    else:
        max_r2 = 0
        for elem in dict_ocurrence:
            if dict_ocurrence[elem] == max_ocurrence:
                if df["r2_mean"].iloc[elem] > max_r2:
                    max_r2 = df["r2_mean"].iloc[elem]
                    best_file = df["filename"].iloc[elem] + ".csv"

    if best_file == filepath_pandas:
        df_final = pd.read_csv(filepath_pandas, sep=delimiter)
    elif best_file == filepath_mean:
        df_final = pd.read_csv(filepath_mean, sep=delimiter)

    dirname = ""
    filename = "best_" + best_file
    extension = ".csv"

    path = Path(dirname, filename).with_suffix(extension)

    df_final.to_csv(path, sep=delimiter, index=None)


# ======== MAIN ========
if __name__ == "__main__":
    typer.run(choose_metric_csv)
