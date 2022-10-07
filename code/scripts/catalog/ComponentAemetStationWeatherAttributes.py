import shutil
from pathlib import Path
from typing import List

import docker
from drama.models.task import TaskResult
from drama.process import Process
from drama_enbic2lab.model import JSONFile


def execute(
    pcs: Process,
    start_date: str,
    end_date: str,
    analysis_stations: List[str],
    aemet_api_key: str,
):
    """

    Name:
        Data Download

    Description:
        Download meteorological data from AEMET for multiple Stations.

    Author:
        Khaos Research Group

    Parameters:
        start-date (str) -> First date of the date range, format (yyyy-mm-dd).
        end-date (str) -> Last date of the date range, format (yyyy-mm-dd).
        analysis_stations (List[str]) -> Station list for AEMET data search.
        aemet-api-key (str) -> Api Key providing by AEMET web page (https://opendata.aemet.es/centrodedescargas/altaUsuario?).


    Mutually Inclusive:
        star_date and end_date

    Inputs:
        None

    Outputs:
       JSON: A JSON file with the data downloaded per station.

    Outfiles:
        stations_weather_attributes.json

    """

    local_component_path = Path(pcs.storage.local_dir)

    station_param = " ".join(
        f"--analysis-stations '{attribute}'" for attribute in analysis_stations
    )

    # Docker
    image_name = "enbic2lab/air/aemet_station_weather_attributes"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--start-date '{start_date}' --end-date '{end_date}' --aemet-api-key '{aemet_api_key}' "
        f"{station_param}",
        detach=True,
        tty=True,
    )

    r = container.wait()
    logs = container.logs()
    if logs:
        pcs.debug([logs.decode("utf-8")])

    container.stop()
    container.remove(v=True)

    # Outputs
    out_json = Path(pcs.storage.local_dir, "stations_weather_attributes.json")
    # send time to remote storage
    if not out_json.is_file():
        raise FileNotFoundError(f"{out_json} is missing")

    dfs_dir = pcs.storage.put_file(out_json)

    # send to downstream
    output_json = JSONFile(resource=dfs_dir)
    pcs.to_downstream(output_json)

    return TaskResult(files=[dfs_dir])
