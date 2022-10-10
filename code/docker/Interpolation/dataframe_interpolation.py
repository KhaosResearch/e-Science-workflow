import os
from pathlib import Path
from tkinter import N
from typing import List, Optional

import pandas as pd
import typer


# ========= METHODS =========
def dataframe_interpolation(
    filepath: str = typer.Option(..., help="File path of the csv File"),
    delimiter: str = typer.Option(..., help="Delimiter of the CSV File"),
    interpolation_method: str = typer.Option(
        ...,
        help="Interpolation technique to use. For mor info see https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.interpolate.html",
    ),
):
    os.chdir("data")

    data = pd.read_csv(filepath, sep=delimiter)
    interpolation_method_name = interpolation_method

    if interpolation_method == "None":
        interpolation_method_name = "None"
    elif interpolation_method == "spline":
        data = round(data.interpolate(method=interpolation_method, order=3), 2)
    else:
        data = round(data.interpolate(method=interpolation_method), 2)

    dirname = ""
    filename = os.path.splitext(filepath)[0] + "_" + str(interpolation_method_name)
    suffix = ".csv"
    path = Path(dirname, filename).with_suffix(suffix)

    data.to_csv(path, sep=delimiter, index=None)


# ========= MAIN =========
if __name__ == "__main__":
    typer.run(dataframe_interpolation)
