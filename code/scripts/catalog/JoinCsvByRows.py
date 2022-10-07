import shutil
from pathlib import Path

import docker
from drama.core.model import SimpleTabularDataset
from drama.models.task import TaskResult
from drama.process import Process


def execute(pcs: Process, outfile_name: str):

    """
    Name:
        Merge Dataset

    Description:
        Join CSV files by rows if their columns names are equal.

    Author:
        Khaos Research Group

    Parameters:

    Inputs:
        CSV file (SimpleTabularDataset): First input file to be joined.
        CSV file (SimpleTabularDatasetFileTwo): Second input file to be joined.

    Outputs:
        CSV file (SimpleTabularDataset): CSV file with joined data .

    Outfiles:
        {outfile_name}.pdf
    """

    # read inputs
    inputs = pcs.get_from_upstream()

    input_file_first = inputs["SimpleTabularDataset"][0]
    input_file_resource_first = input_file_first["resource"]
    input_file_delimiter_first = input_file_first["delimiter"]

    local_file_path_first = Path(pcs.storage.get_file(input_file_resource_first))

    input_file_second = inputs["SimpleTabularDatasetFileTwo"][0]
    input_file_resource_second = input_file_second["resource"]
    input_file_delimiter_second = input_file_second["delimiter"]

    local_file_path_second = Path(pcs.storage.get_file(input_file_resource_second))

    local_component_path = Path(pcs.storage.local_dir)

    # Copy files if they do not exist
    in_csv_first = Path(local_component_path, local_file_path_first.name)
    if not in_csv_first.is_file():
        shutil.copyfile(local_file_path_first, in_csv_first)

    in_csv_second = Path(local_component_path, local_file_path_second.name)
    if not in_csv_second.is_file():
        shutil.copyfile(local_file_path_second, in_csv_second)

    image_name = "enbic2lab/generic_components/join_csv_by_rows"

    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f'--filepath-first "{local_file_path_first.name}" --delimiter-first "{input_file_delimiter_first}" --filepath-second "{local_file_path_second.name}" '
        f'--delimiter-second "{input_file_delimiter_second}" --outfile-name "{outfile_name}"',
        detach=True,
        tty=True,
    )

    r = container.wait()
    logs = container.logs()

    if logs:
        pcs.debug([logs.decode("utf-8")])

    container.stop()
    container.remove(v=True)

    out_csv = Path(local_component_path, outfile_name + ".csv")

    # send time to remote storage
    if not out_csv.is_file():
        raise FileNotFoundError(f"{out_csv} is missing")

    dfs_dir_output = pcs.storage.put_file(out_csv)

    # send to downstream
    out_csv = SimpleTabularDataset(
        resource=dfs_dir_output,
        delimiter=input_file_delimiter_first,
        file_format=".csv",
    )
    pcs.to_downstream(out_csv)

    return TaskResult(files=[dfs_dir_output])
