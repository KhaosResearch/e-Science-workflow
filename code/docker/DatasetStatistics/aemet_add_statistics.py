import os
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import typer


# =============== METHODS ===============
def aemet_add_statistics(
    filepath: str = typer.Option(..., help="File path of the CSV File"),
    acum_list_attr: List[str] = typer.Option(
        ..., help="List of attributes for doing statistics with them"
    ),
    mm_list_attr: List[str] = typer.Option(
        ..., help="List of attributes for mm statistic"
    ),
    delimiter: str = typer.Option(..., help="Delimiter of the CSV File"),
    outfile_name: str = typer.Option(
        ..., help="Name of the output CSV file without extension"
    ),
):
    os.chdir("data")

    total_list_attr = mm_list_attr + acum_list_attr
    total_list_attr = list(dict.fromkeys(total_list_attr))

    # Read dataframe
    dataframe = pd.read_csv(filepath, sep=delimiter)

    # Statistics for each attribute
    cnt_i = 0
    while cnt_i < len(dataframe):
        for attr in total_list_attr:
            if cnt_i in range(0, 3, 1):
                if attr in acum_list_attr:
                    dataframe.loc[cnt_i, attr + "_acum_5"] = np.nan
                    dataframe.loc[cnt_i, attr + "_acum_3"] = np.nan
                if attr in mm_list_attr:
                    dataframe.loc[cnt_i, attr + "_MM5"] = np.nan
                    dataframe.loc[cnt_i, attr + "_MM3"] = np.nan
            elif cnt_i in range(3, 5, 1):
                if attr in mm_list_attr:
                    dataframe.loc[cnt_i, attr + "_MM3"] = round(
                        (
                            dataframe.loc[cnt_i - 2, attr]
                            + dataframe.loc[cnt_i - 1, attr]
                            + dataframe.loc[cnt_i, attr]
                        )
                        / 3,
                        3,
                    )
                    dataframe.loc[cnt_i, attr + "_MM5"] = np.nan
                if attr in acum_list_attr:
                    dataframe.loc[cnt_i, attr + "_acum_3"] = round(
                        (
                            dataframe.loc[cnt_i - 2, attr]
                            + dataframe.loc[cnt_i - 1, attr]
                            + dataframe.loc[cnt_i, attr]
                        ),
                        3,
                    )
                    dataframe.loc[cnt_i, attr + "_acum_5"] = np.nan
            else:
                if attr in mm_list_attr:
                    dataframe.loc[cnt_i, attr + "_MM3"] = round(
                        (
                            dataframe.loc[cnt_i - 2, attr]
                            + dataframe.loc[cnt_i - 1, attr]
                            + dataframe.loc[cnt_i, attr]
                        )
                        / 3,
                        3,
                    )
                    dataframe.loc[cnt_i, attr + "_MM5"] = round(
                        (
                            dataframe.loc[cnt_i - 4, attr]
                            + dataframe.loc[cnt_i - 3, attr]
                            + dataframe.loc[cnt_i - 2, attr]
                            + dataframe.loc[cnt_i - 1, attr]
                            + dataframe.loc[cnt_i, attr]
                        )
                        / 5,
                        3,
                    )
                if attr in acum_list_attr:
                    dataframe.loc[cnt_i, attr + "_acum_3"] = round(
                        (
                            dataframe.loc[cnt_i - 2, attr]
                            + dataframe.loc[cnt_i - 1, attr]
                            + dataframe.loc[cnt_i, attr]
                        ),
                        2,
                    )
                    dataframe.loc[cnt_i, attr + "_acum_5"] = round(
                        (
                            dataframe.loc[cnt_i - 4, attr]
                            + dataframe.loc[cnt_i - 3, attr]
                            + dataframe.loc[cnt_i - 2, attr]
                            + dataframe.loc[cnt_i - 1, attr]
                            + dataframe.loc[cnt_i, attr]
                        ),
                        3,
                    )
        cnt_i += 1

    # Outfile
    dirname = ""
    filename = outfile_name
    suffix = ".csv"
    path = Path(dirname, filename).with_suffix(suffix)

    dataframe.to_csv(path, sep=delimiter, index=None)


# =============== MAIN ===============
if __name__ == "__main__":
    typer.run(aemet_add_statistics)
