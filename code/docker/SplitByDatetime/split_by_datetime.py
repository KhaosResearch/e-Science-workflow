import os
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import typer


def split_by_datetime(
    filepath: str = typer.Option(..., help="File path of the csv file"),
    delimiter: str = typer.Option(
        ..., help="Delimiter of the input file and output file. Must be the same"
    ),
    start_date: str = typer.Option(..., help="Select start date to split the dataset"),
    end_date: str = typer.Option(..., help="Select end date to split the dataset"),
    pollen_column: str = typer.Option(
        ..., help="Select the pollen column of the dataset"
    ),
):
    """
    Given a pandas dataset and start date/end date, select a portion of this dataset

    Date format: 'yyyy-mm-dd'

    Returns a portion of the original dataset
    """

    os.chdir("data")
    # Read dataframe
    dataframe = pd.read_csv(filepath, sep=delimiter, index_col="date")
    dataframe = dataframe.rename(columns={pollen_column: "pollen"})

    mask = (dataframe.index > start_date) & (dataframe.index <= end_date)
    dataframe = dataframe.loc[mask]

    # Plotting the data:
    ax_platanus = dataframe["pollen"].plot(linewidth=0.8)
    ax_platanus.set_xlabel("Date")
    ax_platanus.set_ylabel("Pollen / m3")
    ax_platanus.set_title("Seasonal Plot " + pollen_column)
    plt.savefig("seasonal_plot.pdf")

    # Save Outfile
    dirname = ""
    filename = "split_dataset"
    suffix = ".csv"
    path = Path(dirname, filename).with_suffix(suffix)

    dataframe.to_csv(path, sep=delimiter)


# ============ MAIN ============
if __name__ == "__main__":
    typer.run(split_by_datetime)
