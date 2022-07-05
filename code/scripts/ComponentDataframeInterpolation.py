import shutil
import os
from pathlib import Path

import docker
from drama.models.task import TaskResult
from drama.process import Process
from drama.core.model import SimpleTabularDataset

from typing import List


def execute(pcs: Process, interpolation_method: str = "linear"):
    """

    Name:
        Interpolation

    Description:
    Fill Nan values using pandas interpolation.

    Author:
        Khaos Research Group

    Parameters:
        interpolation_method (str) --> Interpolation technique to use. For mor info see https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.interpolate.html

    Mutually Inclusive:
        None

    Inputs:
        SimpleTabularDataset: A CSV file with all the data processed.

    Outputs:
        SimpleTabularDataset: A CSV file with the data interpolated.

    Outfiles:
        filename.csv

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
    image_name = "enbic2lab/generic/dataframe_interpolation"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath '{local_file_path.name}' --delimiter '{input_file_delimiter}' --interpolation-method '{interpolation_method}'",
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
    outfile_name = (
        os.path.splitext(local_file_path.name)[0] + "_" + interpolation_method
    )
    out_csv = Path(pcs.storage.local_dir, outfile_name).with_suffix(".csv")
    # send time to remote storage
    if not out_csv.is_file():
        raise FileNotFoundError(f"{out_csv} is missing")

    dfs_dir = pcs.storage.put_file(out_csv)

    # send to downstream
    output_csv = SimpleTabularDataset(resource=dfs_dir, delimiter=input_file_delimiter)
    pcs.to_downstream(output_csv)

    return TaskResult(files=[dfs_dir])
