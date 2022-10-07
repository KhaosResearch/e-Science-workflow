# ======================== MODULES ============
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List
from urllib.parse import urljoin

import httpx
import pandas as pd
import typer
from dateutil.relativedelta import relativedelta

# ================== CLASES ================


# This class provides an enumeration for future uses in Aemet class
class Period(Enum):
    WEEKLY = "WEEKLY"
    HOURLY = "HOURLY"


class Aemet:
    BASE_URL = "https://opendata.aemet.es/opendata/api/"
    EMA_API_URL_STATIONS = urljoin(
        BASE_URL, "valores/climatologicos/inventarioestaciones/todasestaciones"
    )
    DAILY_WEATHER_VALUE = urljoin(
        BASE_URL,
        "valores/climatologicos/diarios/datos/fechaini/{}/fechafin/{}/estacion/{}/?api_key={}",
    )

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_daily_weather(self, start_date: datetime, end_date: datetime, station: str):
        start_date_parse = start_date.strftime("%Y-%m-%dT%H:%M:%SUTC")
        end_date_parse = end_date.strftime("%Y-%m-%dT%H:%M:%SUTC")
        url = self.DAILY_WEATHER_VALUE.format(
            start_date_parse, end_date_parse, station, self.api_key
        )
        try:
            r = httpx.get(url, headers=self._get_headers())
        except Exception as e:
            print(e)
        data = r.json().get("datos")
        all_data: List[Dict[str, str]] = httpx.get(data)
        return all_data.json()

    def _get_headers(self):
        return {"api_key": self.api_key}


# ===================== METHODS =====================


def aemet_download_data(
    station: str = typer.Option(..., help="Code of the station from AEMET"),
    start_date: str = typer.Option(
        ..., help="First date of the date range, format (yyyy-mm-dd)"
    ),
    end_date: str = typer.Option(
        ..., help="Last date of the date range, format (yyyy-mm-dd)"
    ),
    aemet_api_key: str = typer.Option(
        ...,
        help="Api Key providing by AEMET web page (https://opendata.aemet.es/centrodedescargas/altaUsuario?)",
    ),
    delimiter: str = typer.Option(..., help="Delimiter of the output CSV File"),
):
    # Parse Date
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Download Aemet Data
    aemet_client = Aemet(api_key=aemet_api_key)
    daily_weather_values = []
    start = start_date
    try:
        while start <= end_date:
            daily_weather_values.extend(
                aemet_client.get_daily_weather(
                    start, start + relativedelta(years=3), station
                )
            )

            start = start + relativedelta(day=1, years=3)
    except Exception as e:
        print(e)

    # Create Dataframe with Aemet Data
    dataframe = pd.json_normalize(daily_weather_values)

    dataframe[
        [
            "tmed",
            "prec",
            "tmin",
            "tmax",
            "dir",
            "velmedia",
            "racha",
            "sol",
            "presMax",
            "presMin",
        ]
    ] = dataframe[
        [
            "tmed",
            "prec",
            "tmin",
            "tmax",
            "dir",
            "velmedia",
            "racha",
            "sol",
            "presMax",
            "presMin",
        ]
    ].apply(
        lambda x: x.str.replace(",", ".")
    )
    dataframe["fecha"] = pd.to_datetime(dataframe["fecha"], format="%Y-%m-%d").dt.date
    dataframe = dataframe.drop(dataframe[dataframe["fecha"] > end_date].index)
    dataframe["prec"].loc[dataframe["prec"] == "Ip"] = 0

    # Create CSV Outfile
    dirname = "data"
    filename = station + "_aemet_data"
    suffix = ".csv"
    path = Path(dirname, filename).with_suffix(suffix)

    dataframe.to_csv(path, sep=delimiter, index=None)


# ================ MAIN ============
if __name__ == "__main__":
    typer.run(aemet_download_data)
