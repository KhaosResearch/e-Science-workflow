import os
from datetime import datetime
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import typer


# =========== METHODS ============
def date_range(start, end):
    """[summary]

    Args:
        start ([datetime]): [initial date]
        end ([datetime]): [final date]

    Returns:
        Date Range between start and end date
    """
    date_list = []
    curr_date = start
    while curr_date <= end:
        date_list.append(curr_date)
        curr_date = curr_date.replace(year=curr_date.year + 1)
    return date_list


def dataframe_interpolation(
    filepath: str = typer.Option(..., help="Filepath of the csv file"),
    delimiter: str = typer.Option(..., help="Delimiter of the csv file"),
    initial_year: int = typer.Option(..., help="Intial year of the dataset"),
    final_year: int = typer.Option(..., help="Final year of the dataset"),
    date_column: str = typer.Option(..., help="Name of the date column"),
    outfile_name: str = typer.Option(..., help="Name of the output file"),
):
    os.chdir("data")

    data = pd.read_csv(filepath, sep=delimiter, parse_dates=[date_column])
    data = data.rename(columns={date_column: "fecha"})
    nan_values = data[data.isna().any(axis=1)]

    for row in nan_values.itertuples():
        for column in nan_values.columns:
            if pd.isna(getattr(row, column)):
                row_fecha = row.fecha
                if type(row.fecha) == str:
                    row_fecha = datetime.strptime(row_fecha, "%Y-%m-%d")
                day, month = row_fecha.day, row_fecha.month
                subset = date_range(
                    start=datetime(initial_year, month, day),
                    end=datetime(final_year, month, day),
                )
                mean = round(
                    data.loc[data["fecha"].isin(subset)][column].mean(skipna=True), 2
                )
                data.at[row.Index, column] = mean

    data = data.rename(columns={"fecha": date_column})

    dirname = ""
    filename = outfile_name
    extension = ".csv"
    path = Path(dirname, filename).with_suffix(extension)
    data.to_csv(path, sep=";", index=None)


# =========== MAIN ============
if __name__ == "__main__":
    typer.run(dataframe_interpolation)
