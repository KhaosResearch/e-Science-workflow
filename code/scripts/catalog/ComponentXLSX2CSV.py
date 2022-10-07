import shutil
from dataclasses import dataclass
from pathlib import Path

import docker
from drama.core.model import SimpleTabularDataset
from drama.models.task import TaskResult
from drama.process import Process


def execute(pcs: Process, delimiter: str = ";", header: bool = True):
    """

    Name:
        Component XLSX to CSV

    Description:
        Convert a xlsx file into a csv outfile.

    Author:
        Khaos Research Group

    Parameters:
        delimiter (str) -> Delimiter of the csv outfile.
        header/no-header ->  Has header or not.

    Mutually Inclusive:
        None

    Inputs:
        {name_file}.xlsx

    Outputs:
        SimpleTabularDataset: CSV file converted.

    Outfiles:
        {nome_file}.csv

    """

    # read inputs
    inputs = pcs.get_from_upstream()
    input_file = inputs["ExcelDataset"][0]
    input_file_resource = input_file["resource"]

    local_file_path = Path(pcs.storage.get_file(input_file_resource))
    local_component_path = Path(pcs.storage.local_dir)

    # Copy file if it does not exist
    in_xlsx = Path(local_component_path, local_file_path.name)
    if not in_xlsx.is_file():
        shutil.copyfile(local_file_path, in_xlsx)

    image_name = "enbic2lab/generic/xlsx2csv"

    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath {local_file_path.name} --delimiter '{delimiter}' "
        f"{'--header' if header else '--no-header'}",
        detach=True,
        tty=True,
    )

    r = container.wait()
    logs = container.logs()
    if logs:
        pcs.debug([logs.decode("utf-8")])

    container.stop()
    container.remove(v=True)

    # prepare output
    out_csv = Path(pcs.storage.local_dir, Path(local_file_path.name).stem).with_suffix(
        ".csv"
    )

    # send time to remote storage
    if not out_csv.is_file():
        raise FileNotFoundError(f"{out_csv} is missing")

    dfs_dir_csv = pcs.storage.put_file(out_csv)

    # send to downstream
    csv_output = SimpleTabularDataset(resource=dfs_dir_csv, delimiter=delimiter)
    pcs.to_downstream(csv_output)

    return TaskResult(files=[dfs_dir_csv])
