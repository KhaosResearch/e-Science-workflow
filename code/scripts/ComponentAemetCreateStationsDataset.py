import shutil
from pathlib import Path

import docker
from drama.models.task import TaskResult
from drama.process import Process
from drama.core.model import SimpleTabularDataset


def execute(pcs: Process, attribute: str, delimiter: str):
    """

    Name:
        Stations Attribute

    Description:
        Create a CSV File with data about an attribute from Aemet for differents stations

    Author:
        Khaos Research Group

    Parameters:
        attribute (str) -> Attribute name from AEMET..
        delimiter (str) -> Delimiter for CSV output file..


    Mutually Inclusive:
        None

    Inputs:
        JSONFile: A JSON file with the data downloaded per station.

    Outputs:
       SimpleTabularDataset: A CSV with the code of the stations in columns, the attribute value per date as values of
       the dataset.

    Outfiles:
        Aemet_'attribute'_stations.csv

    """

    # Inputs
    inputs = pcs.get_from_upstream()

    input_file = inputs["JSONFile"][0]
    input_file_resource = input_file["resource"]
    local_file_path = Path(pcs.storage.get_file(input_file_resource))

    local_component_path = Path(pcs.storage.local_dir)

    # Copy file if it does not exist
    in_json = Path(local_component_path, local_file_path.name)
    if not in_json.is_file():
        shutil.copyfile(local_file_path, in_json)

    # Docker
    image_name = "enbic2lab/air/aemet_create_stations_dataset"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--json-file  '{local_file_path.name}' --attribute '{attribute}' --delimiter '{delimiter}'",
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
    out_csv = Path(pcs.storage.local_dir, f"Aemet_{attribute}_stations.csv")
    # send time to remote storage
    if not out_csv.is_file():
        raise FileNotFoundError(f"{out_csv} is missing")

    dfs_dir = pcs.storage.put_file(out_csv)

    # send to downstream
    output_csv = SimpleTabularDataset(resource=dfs_dir, delimiter=delimiter)
    pcs.to_downstream(output_csv)

    return TaskResult(files=[dfs_dir])
