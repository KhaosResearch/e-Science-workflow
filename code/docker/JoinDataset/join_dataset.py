import os
from pathlib import Path

import pandas as pd
import typer

# ================= METHODS =================


def createDataFrame(file_name, delimiter):
    if Path(file_name).suffix == ".csv" or Path(file_name).suffix == ".tsv":
        dataframe = pd.read_csv(file_name, delimiter=delimiter)
    else:
        raise Exception("Wrong extension. Only accept .csv files")
    return dataframe


def join_dataset(
    first_file_path: str = typer.Option(..., help="File path of the first file"),
    index_column_first_file: str = typer.Option(
        ...,
        help="Name of the column of the firs file. This will be use for merge datasets using index column as keys",
    ),
    second_file_path: str = typer.Option(..., help="File path of the second file"),
    index_column_second_file: str = typer.Option(
        ...,
        help="Name of the column of the firs file. This will be use for merge datasets using index column as keys",
    ),
    outfile_name: str = typer.Option(
        ...,
        help="Name without extension of the outfile. Example: for data.csv write data.",
    ),
    delimiter_file_1: str = typer.Option(..., help="Delimiter of the first file."),
    delimiter_file_2: str = typer.Option(..., help="Delimiter of the second file."),
    delimiter: str = typer.Option(..., help="Delimiter of the output file."),
    join_how_parameter: str = typer.Option(
        ...,
        help=f"How to handle the operation of the two objects."
        f"left (DEFAULT): use calling frame’s index (or column if on is specified.) "
        f"right: use other’s index. "
        f"outer: form union of calling frame’s index (or column if on is specified) with other’s index, and sort it. lexicographically."
        f"inner: form intersection of calling frame’s index (or column if on is specified) with other’s index, preserving the order of the calling’s one.",
    ),
):
    os.chdir("data")
    # Read first file
    dataframe_first_file = createDataFrame(first_file_path, delimiter_file_1)

    # Read second file
    dataframe_second_file = createDataFrame(second_file_path, delimiter_file_2)

    # Join dataframes
    try:
        final_dataframe = dataframe_first_file.join(
            dataframe_second_file.set_index(index_column_second_file),
            on=index_column_first_file,
            how=join_how_parameter,
        )

        final_dataframe = final_dataframe.drop_duplicates()
    except Exception as e:
        print(e)

    # Outfile
    dirname = "./"
    filename = outfile_name
    suffix = ".csv"
    path = Path(dirname, filename).with_suffix(suffix)

    # Export csv file
    final_dataframe.to_csv(path, sep=delimiter, index=None)


# ================= MAIN =================
if __name__ == "__main__":
    typer.run(join_dataset)
