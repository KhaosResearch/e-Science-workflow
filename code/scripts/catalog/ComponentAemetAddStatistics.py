import shutil
from pathlib import Path

import docker
from drama.models.task import TaskResult
from drama.process import Process
from drama.core.model import SimpleTabularDataset

from typing import List


def execute(
    pcs: Process, acum_list_attr: List[str], mm_list_attr: List[str], outfile_name: str
):
    """

    Name:
        Dataset Statistics

    Description:
    Create a CSV file with extra columns based on statistics.

    Author:
        Khaos Research Group

    Parameters:
        acum_list_attr (List[str]) --> List of attributes for doing statistics with them.
        mm_list_attr (List[str]) --> List of attributes for mm statistic.
        outfile_name (str) --> Name of the output CSV file without extension.

    Mutually Inclusive:
        total_list_attr with acum_list_attr and mm_list_attr

    Inputs:
        SimpleTabularDataset: A CSV file with all the data processed.

    Outputs:
        SimpleTabularDataset: A CSV file with the new columns.

    Outfiles:
        outfile_name.csv

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

    acum_attribute_list_param = " ".join(
        f'--acum-list-attr "{attribute}"' for attribute in acum_list_attr
    )
    mm_attribute_list_param = " ".join(
        f'--mm-list-attr "{attribute}"' for attribute in mm_list_attr
    )

    # Docker
    image_name = "enbic2lab/air/aemet_add_statistics"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath '{local_file_path.name}' --delimiter {input_file_delimiter} --outfile-name '{outfile_name}' {acum_attribute_list_param} {mm_attribute_list_param}",
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
    output_csv = SimpleTabularDataset(resource=dfs_dir, delimiter=input_file_delimiter)
    pcs.to_downstream(output_csv)

    return TaskResult(files=[dfs_dir])
