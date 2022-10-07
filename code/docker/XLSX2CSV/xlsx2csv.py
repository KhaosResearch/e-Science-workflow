import os
from pathlib import Path

import pandas as pd
import typer


# ============== METHODS ==============
def xlsx2csv(
    filepath: str = typer.Option(..., help="Filepath of the xlsx file."),
    delimiter: str = typer.Option(..., help="Delimiter of the csv outfile"),
    header: bool = typer.Option(..., help="Has header or not use --help for more info"),
):
    os.chdir("data")
    # Read xlsx file
    if header:
        dataframe = pd.read_excel(filepath)
    else:
        dataframe = pd.read_excel(filepath, header=None)
    # Get outfile path and filename
    dirname = "./"
    filename = Path(filepath).stem
    suffix = ".csv"
    path = Path(dirname, filename).with_suffix(suffix)
    # Export csv file
    dataframe.to_csv(path, sep=delimiter, index=None, decimal=".")


# ================= MAIN ===============
if __name__ == "__main__":
    typer.run(xlsx2csv)
