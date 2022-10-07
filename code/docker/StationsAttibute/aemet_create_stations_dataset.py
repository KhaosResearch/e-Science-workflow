import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import typer


# ============== METHODS ==============
def aemet_create_stations_dataset(
    json_file: str = typer.Option(..., help="JSON file path"),
    attribute: str = typer.Option(
        ...,
        help="Attribute name from AEMET, could be: prec, tmin, tmax, tmed, dir, velmedia, racha, sol, presMax or presMin",
    ),
    delimiter: str = typer.Option(..., help="Delimiter for CSV output file"),
):
    os.chdir("data")

    # Read JSON file
    f = open(json_file)
    json_data = json.load(f)

    # Create Dataframe
    dataframe = pd.DataFrame()

    # Add data to Dataframe
    for station in json_data:
        for data_station in station:
            if attribute in data_station:
                dataframe.loc[
                    data_station["fecha"], data_station["indicativo"]
                ] = data_station[attribute]
                dataframe.loc[data_station["fecha"], "DATE"] = data_station["fecha"]
                if data_station[attribute] == "Ip":
                    dataframe.loc[
                        data_station["fecha"], data_station["indicativo"]
                    ] = dataframe.loc[
                        data_station["fecha"], data_station["indicativo"]
                    ].replace(
                        "Ip", "0"
                    )

                    dataframe.loc[
                        data_station["fecha"], data_station["indicativo"]
                    ] = dataframe.loc[
                        data_station["fecha"], data_station["indicativo"]
                    ].replace(
                        ",", "."
                    )

                    dataframe.loc[
                        data_station["fecha"], data_station["indicativo"]
                    ] = float(
                        dataframe.loc[data_station["fecha"], data_station["indicativo"]]
                    )
                else:
                    dataframe.loc[
                        data_station["fecha"], data_station["indicativo"]
                    ] = dataframe.loc[
                        data_station["fecha"], data_station["indicativo"]
                    ].replace(
                        ",", "."
                    )

                    dataframe.loc[
                        data_station["fecha"], data_station["indicativo"]
                    ] = float(
                        dataframe.loc[data_station["fecha"], data_station["indicativo"]]
                    )
            else:
                dataframe.loc[
                    data_station["fecha"], data_station["indicativo"]
                ] = np.nan
                dataframe.loc[data_station["fecha"], "DATE"] = data_station["fecha"]

    # Output file
    dirname = ""
    filename = "Aemet_" + attribute + "_stations"
    suffix = ".csv"
    path = Path(dirname, filename).with_suffix(suffix)

    dataframe.to_csv(path, sep=delimiter, index=False, decimal=".")


# ============== MAIN ==============
if __name__ == "__main__":
    typer.run(aemet_create_stations_dataset)
