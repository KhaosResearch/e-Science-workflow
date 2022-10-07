import shutil
from pathlib import Path

import docker
from drama.models.task import TaskResult
from drama.process import Process
from drama.core.model import SimpleTabularDataset


def execute(
    pcs: Process,
    start_date: str,
    end_date: str,
    station: str,
    aemet_api_key: str,
    delimiter: str,
):
    """

    Name:
        Data Download

    Description:
        Download meteorological data from AEMET

    Author:
        Khaos Research Group

    Parameters:
        start-date (str) -> First date of the date range, format (yyyy-mm-dd).
        end-date (str) -> Last date of the date range, format (yyyy-mm-dd).
        station (str) -> Code of the station from AEMET
        aemet-api-key (str) -> Api Key providing by AEMET web page (https://opendata.aemet.es/centrodedescargas/altaUsuario?).
        delimiter (str) -> Delimiter of the output CSV File.


    Mutually Inclusive:
        start_date and end_date

    Inputs:
        None

    Outputs:
       SimpleTabularDataset: A CSV with the data of the station from Aemet Database.

    Outfiles:
        'station'_aemet_data.csv

    """

    # Inputs

    local_component_path = Path(pcs.storage.local_dir)

    # Docker
    image_name = "enbic2lab/air/aemet_download_data"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--start-date  '{start_date}' --end-date '{end_date}' --station '{station}' "
        f"--aemet-api-key {aemet_api_key} --delimiter {delimiter}",
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
    out_csv = Path(pcs.storage.local_dir, f"{station}_aemet_data.csv")
    # send time to remote storage
    if not out_csv.is_file():
        raise FileNotFoundError(f"{out_csv} is missing")

    dfs_dir = pcs.storage.put_file(out_csv)

    # send to downstream
    output_csv = SimpleTabularDataset(resource=dfs_dir, delimiter=delimiter)
    pcs.to_downstream(output_csv)

    return TaskResult(files=[dfs_dir])
