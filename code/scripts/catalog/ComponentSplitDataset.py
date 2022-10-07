import shutil
from pathlib import Path

import docker
from drama.models.task import TaskResult
from drama.process import Process
from typing import List
from drama.core.model import SimpleTabularDataset


def execute(pcs: Process, outfile_name: str, attribute_list: List[str]):
    f"""

    Name:
        Split Dataset

    Description:
        Split the dataset and return another with the columns that you want to keep.

    Author:
        Khaos Research Group

    Parameters:
        outfile_name (str) --> Name of the output file without extensions.
        attribute_list (str) --> List of attributes that you want to keep.

    Mutually Inclusive:
        None

    Inputs:
        SimpleTabularDataset: A CSV file.

    Outputs:
       SimpleTabularDataset: A CSV file with the columns attributes selected.

    Outfiles:
        'outfile_name'.csv

    """

    # read inputs
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

    attribute_params = " ".join(
        f'--attribute-list "{attribute}"' for attribute in attribute_list
    )

    # Docker
    image_name = "enbic2lab/generic/split_dataset"

    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath  {local_file_path.name} --delimiter {input_file_delimiter} "
        f"--outfile-name {outfile_name} {attribute_params} ",
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
