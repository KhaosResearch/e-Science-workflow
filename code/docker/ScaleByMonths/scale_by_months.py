import os
from pathlib import Path

import pandas as pd
import typer


def scale_by_months(
    filepath: str = typer.Option(..., help="File path of the csv file"),
    delimiter: str = typer.Option(
        ..., help="Delimiter of the input file and output file. Must be the same"
    ),
    date_column: str = typer.Option(..., help="Name of the date column"),
):
    """
    Given a Pollen Dataframe by days, it is scaled to months.

    Returns the scaled Dataframe in months
    """

    os.chdir("data")
    # Read data
    dataframe = pd.read_csv(filepath, sep=delimiter)
    # Rename date column to keep it in the entire workflow
    dataframe = dataframe.rename(columns={date_column: "date"})

    dataframe["date"] = pd.to_datetime(dataframe["date"])
    dataframe["date"] = dataframe["date"].dt.to_period("M")
    dates = dataframe["date"].unique()
    df_month = pd.DataFrame()
    df_month["date"] = dates
    df_month = df_month.set_index("date")

    dataframe_aux = dataframe.drop(["date"], axis=1)

    for date in dates:
        df_month.loc[date, dataframe_aux.columns] = dataframe.loc[
            dataframe["date"] == date, dataframe_aux.columns
        ].sum()

    # Save Outfile
    dirname = ""
    filename = "scaled_dataset"
    suffix = ".csv"
    path = Path(dirname, filename).with_suffix(suffix)

    df_month.to_csv(path, sep=delimiter)


# ============ MAIN ============
if __name__ == "__main__":
    typer.run(scale_by_months)
