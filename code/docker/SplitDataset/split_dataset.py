import os
from pathlib import Path
from typing import List

import pandas as pd
import typer


# ============ METHODS ============
def split_dataset(
    filepath: str = typer.Option(..., help="File path of the csv file"),
    attribute_list: List[str] = typer.Option(
        ...,
        help="List of attributes that you want to keep. All must be in the dataframe.",
    ),
    outfile_name: str = typer.Option(
        ..., help="Name of the output file without extensions"
    ),
    delimiter: str = typer.Option(
        ..., help="Delimiter of the input file and output file. Must be the same"
    ),
):
    os.chdir("data")
    # Read data
    dataframe = pd.read_csv(filepath, sep=delimiter)

    # Chek if all attributes in attribute_list is in dataframe columns
    if all(x in dataframe for x in attribute_list):
        # Select columns to keep
        dataframe = dataframe[dataframe.columns.intersection(attribute_list)]
    else:
        raise Exception("Not all attributes in list are in the dataframe.")

    # Outfile
    dirname = ""
    filename = outfile_name
    suffix = ".csv"
    path = Path(dirname, filename).with_suffix(suffix)

    dataframe.to_csv(path, sep=delimiter, index=None)


# ============ MAIN ============
if __name__ == "__main__":
    typer.run(split_dataset)
