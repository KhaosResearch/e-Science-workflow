import json
import os
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List
from urllib.parse import urljoin

import httpx
import numpy as np
import typer
from dateutil.relativedelta import relativedelta


# ================ Classes ================
# Period
class Period(Enum):
    WEEKLY = "WEEKLEY"
    HOURLY = "HOURLY"


# Aemet
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

    def get_daily_weather(self, start_date: str, end_date: str, station: str):
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


# ================ Methods ================
def aemet_station_weather_attributes(
    aemet_api_key: str = typer.Option(
        ...,
        help="Api Key providing by AEMET web page (https://opendata.aemet.es/centrodedescargas/altaUsuario?).",
    ),
    start_date: str = typer.Option(
        ...,
        help="First date of the range date for search data in AEMET. Format yyyy-mm-dd.",
    ),
    end_date: str = typer.Option(
        ...,
        help="Last date of the range date for search data in AEMET. Format yyyy-mm-dd.",
    ),
    analysis_stations: List[str] = typer.Option(
        ..., help="Station list for AEMET data search."
    ),
):
    os.chdir("data")

    # Parsing date
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Download AEMET Data
    aemet_client = Aemet(api_key=aemet_api_key)
    stations_weather_values = []
    try:
        for station in analysis_stations:
            daily_weather_values = []
            start = start_date
            while start <= end_date:
                try:
                    daily_weather_values.extend(
                        aemet_client.get_daily_weather(
                            start, start + relativedelta(years=3), station
                        )
                    )
                except Exception as e:
                    print(f"Warning in station {station} at start date {start}: {e}")
                    pass

                start = start + relativedelta(day=1, years=3)
            stations_weather_values.append(daily_weather_values)
    except Exception as e:
        print(f"Warning in station {station} at start date {start}: {e}")

    # JSON Dumps with UTF-8 encoding
    dirname = ""
    filename = "stations_weather_attributes"
    suffix = ".json"
    path = Path(dirname, filename).with_suffix(suffix)

    print()
    try:
        if np.array(stations_weather_values).size > 0:
            with open(path, "w", encoding="utf8") as f:
                json.dump(stations_weather_values, f, ensure_ascii=False)
        else:
            raise Exception("Error: Station Weather Values array is empty")
    except Exception as e:
        print(e)


# ================ Main ================
if __name__ == "__main__":
    typer.run(aemet_station_weather_attributes)
