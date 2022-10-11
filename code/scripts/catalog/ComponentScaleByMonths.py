import shutil
from pathlib import Path

import docker
from drama.core.model import SimpleTabularDataset
from drama.models.task import TaskResult
from drama.process import Process


def execute(pcs: Process, date_column: str):
    f"""

    Name:
        Scale By Months

    Description:
        Given a Pollen Dataframe by days, it is scaled to months

    Author:
        Khaos Research Group

    Parameters:
        * --date_column (str) -> Name of the date column.

    Mutually Inclusive:
        None

    Inputs:
        SimpleTabularDataset: A CSV file with AEMET, pollen and statistics data.

    Outputs:
       SimpleTabularDataset: A CSV with the scaled Dataframe in months.

    Outfiles:
        scaled_dataset.csv

    """

    # Inputs
    inputs = pcs.get_from_upstream()

    input_file = inputs["SimpleTabularDataset"][0]
    input_file_resource = input_file["resource"]
    input_file_delimiter = input_file["delimiter"]
    local_file_path = Path(pcs.storage.get_file(input_file_resource))

    local_component_path = Path(pcs.storage.local_dir)

    # Copy file if it does not exist
    in_csv = Path(local_component_path, local_file_path.name)
    if not in_csv.is_file():
        shutil.copyfile(local_file_path, in_csv)

    # Docker
    image_name = "enbic2lab/air/scale_by_months"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath  '{local_file_path.name}' --date-column '{date_column}' "
        f"--delimiter '{input_file_delimiter}'",
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
    out_csv = Path(pcs.storage.local_dir, "scaled_dataset.csv")
    # send time to remote storage
    if not out_csv.is_file():
        raise FileNotFoundError(f"{out_csv} is missing")

    dfs_dir = pcs.storage.put_file(out_csv)

    # send to downstream
    output_csv = SimpleTabularDataset(resource=dfs_dir, delimiter=input_file_delimiter)
    pcs.to_downstream(output_csv)

    return TaskResult(files=[dfs_dir])
