import shutil
from dataclasses import dataclass
from pathlib import Path

import docker
from drama.core.model import SimpleTabularDataset
from drama.models.task import TaskResult
from drama.process import Process


@dataclass
class SimpleTabularDatasetFileTwo(SimpleTabularDataset):
    pass


def execute(
    pcs: Process,
    col_first_file: str,
    col_second_file: str,
    index_column_first_file: str,
    index_column_second_file: str,
    outfile_name: str,
):
    """

    Name:
        Update Dataset

    Description:
        Update a CSV main file using data from another CSV aux file.

    Author:
        Khaos Research Group

    Parameters:
        col_first_file (str) --> Column of the main file to be updated.
        col_second_file (str) --> Column of the aux file used to update de main file.
        index_column_first_file (str) --> Column of the main file used to join with the aux file as key.
        index_column_second_file (str) --> Column of the aux file used to join with te main file as key.
        outfile_name (str) --> Name of the output file without extension.

    Mutually Inclusive:
        col_first_file/col_second_file and index_column_first_file/index_column_second_file

    Inputs:
        SimpleTabularDataset: A CSV file that will be updated.
        SimpleTabularDatasetFileTwo: A CSV file used to update the main file.

    Outputs:
       SimpleTabularDataset: Main file update.

    Outfiles:
        'outfile_name'.csv

    """

    # read inputs
    inputs = pcs.get_from_upstream()

    input_file = inputs["SimpleTabularDataset"][0]
    input_file_resource = input_file["resource"]
    input_file_delimiter = input_file["delimiter"]
    local_file_path = Path(pcs.storage.get_file(input_file_resource))

    input_file_aux = inputs["SimpleTabularDatasetFileTwo"][0]
    input_file_resource_aux = input_file_aux["resource"]
    input_file_delimiter_aux = input_file_aux["delimiter"]
    local_file_path_aux = Path(pcs.storage.get_file(input_file_resource_aux))

    local_component_path = Path(pcs.storage.local_dir)

    # Copy file if it does not exist
    in_csv = Path(local_component_path, local_file_path.name)
    if not in_csv.is_file():
        shutil.copyfile(local_file_path, in_csv)

    in_csv_aux = Path(local_component_path, local_file_path_aux.name)
    if not in_csv_aux.is_file():
        shutil.copyfile(local_file_path_aux, in_csv_aux)

    # Docker
    image_name = "enbic2lab/generic/update_dataset"

    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--first-file  {local_file_path.name} --second-file {local_file_path_aux.name} "
        f"--col-first-file {col_first_file} --col-second-file {col_second_file} --index-column-first-file {index_column_first_file} "
        f"--index-column-second-file {index_column_second_file} --delimiter-first-file {input_file_delimiter} "
        f"--delimiter-second-file {input_file_delimiter_aux} --outfile-name {outfile_name}",
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
    out_csv = Path(pcs.storage.local_dir, outfile_name + ".csv")
    # send time to remote storage
    if not out_csv.is_file():
        raise FileNotFoundError(f"{out_csv} is missing")

    dfs_dir = pcs.storage.put_file(out_csv)

    # send to downstream
    output_csv = SimpleTabularDataset(
        resource=dfs_dir, delimiter=input_file_delimiter, file_format=".csv"
    )
    pcs.to_downstream(output_csv)

    return TaskResult(files=[dfs_dir])
