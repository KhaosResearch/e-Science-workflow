import os
from pathlib import Path

import pandas as pd
import typer


# ========= METHODS =========
def csv2json(
    input_filepath: str = typer.Option(..., help="Filepath for the input CSV File"),
    delimiter: str = typer.Option(..., help="Delimiter of te input CSV File"),
):
    # Set working directory
    os.chdir("data")

    # Read CSV File
    data = pd.read_csv(input_filepath, sep=delimiter)
    columns = data.columns
    for column in columns:
        data = data.rename(columns={column: column.replace(".", "")})
    # OutputFile
    dirname = "./"
    filename = Path(input_filepath).stem
    suffix = ".json"
    path = Path(dirname, filename).with_suffix(suffix)

    data.to_json(path, orient="records", force_ascii=False)


# ========= MAIN =========
if __name__ == "__main__":
    typer.run(csv2json)
