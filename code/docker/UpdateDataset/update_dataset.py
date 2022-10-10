import os
from pathlib import Path

import pandas as pd
import typer


# ============= METHODS =============
def update_dataset(
    first_file: str = typer.Option(..., help="Path of the file that will be updataed"),
    second_file: str = typer.Option(
        ..., help="Path of the aux file used to update the main file"
    ),
    col_first_file: str = typer.Option(
        ..., help="Column of the main file to be updated"
    ),
    col_second_file: str = typer.Option(
        ..., help="Column of the aux file used to update de main file"
    ),
    index_column_first_file: str = typer.Option(
        ..., help="Column of the main file used to join with the aux file as key"
    ),
    index_column_second_file: str = typer.Option(
        ..., help="Column of the aux file used to join with te main file as key"
    ),
    delimiter_first_file: str = typer.Option(
        ..., help="Delimiter of the CSV main file"
    ),
    delimiter_second_file: str = typer.Option(
        ..., help="Delimiter of the CSV aux file"
    ),
    outfile_name: str = typer.Option(
        ..., help="Name of the output file without extension"
    ),
):
    os.chdir("data")

    main_dataframe = pd.read_csv(first_file, sep=delimiter_first_file)
    main_dataframe = main_dataframe.drop(col_first_file, axis=1)

    aux_dataframe = pd.read_csv(second_file, sep=delimiter_second_file)
    aux_dataframe = aux_dataframe.rename(columns={col_second_file: col_first_file})

    main_dataframe = main_dataframe.join(
        aux_dataframe.set_index(index_column_second_file), on=index_column_first_file
    )

    dirname = ""
    filename = outfile_name
    suffix = ".csv"

    path = Path(dirname, filename).with_suffix(suffix)

    main_dataframe.to_csv(path, sep=delimiter_first_file, index=None)


# ============= MAIN =============
if __name__ == "__main__":
    typer.run(update_dataset)
