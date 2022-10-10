import os
from pathlib import Path

import pandas as pd
import typer


def joinCsvByRows(
    filepath_first: str = typer.Option(..., help="Filepath of first CSV file"),
    delimiter_first: str = typer.Option(..., help="Delimiter of first CSV file"),
    filepath_second: str = typer.Option(..., help="Filepath of second CSV file"),
    delimiter_second: str = typer.Option(..., help="Delimiter of second CSV file"),
    outfile_name: str = typer.Option(..., help="Name of output file"),
):
    os.chdir("data")

    first_csv = pd.read_csv(filepath_first, sep=delimiter_first, index_col=False)
    second_csv = pd.read_csv(filepath_second, sep=delimiter_second, index_col=False)

    columns_first = set(first_csv.columns)

    columns_second = set(second_csv.columns)

    same_columns = False

    if columns_first == columns_second:
        same_columns = True
    else:
        raise ValueError("CSV files do not have the same columns.")

    if same_columns:
        result = pd.concat([first_csv, second_csv])
        final_csv = result.reset_index()
        final_csv = final_csv.drop("index", axis=1)
        final_csv.to_csv(outfile_name + ".csv", sep=delimiter_first, index=False)


if __name__ == "__main__":
    typer.run(joinCsvByRows)
