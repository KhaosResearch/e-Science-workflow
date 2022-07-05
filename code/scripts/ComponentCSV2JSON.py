import shutil
from dataclasses import dataclass
from pathlib import Path

import docker
from drama.models.task import TaskResult
from drama.process import Process
from drama_enbic2lab.model import JSONFile


def execute(pcs: Process, outfile_name: str):
    """

    Name:
        CSV to JSON

    Description:
    Convert a CSV file into JSON file.

    Author:
        Khaos Research Group

    Parameters:
        outfile_name (str) --> Name without extension of the Output JSON File.

    Mutually Inclusive:
        None

    Inputs:
        {name_file}.csv

    Outputs:
        JSONFile: JSON file with the CSV input file data.

    Outfiles:
        {output_filename}.json

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

    image_name = "enbic2lab/generic/csv2json"

    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--input-filepath {local_file_path.name} --delimiter '{input_file_delimiter}' "
        f"--outfile-name {outfile_name}",
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
    out_json = Path(pcs.storage.local_dir, Path(local_file_path.name).stem).with_suffix(
        ".json"
    )

    # send time to remote storage
    if not out_json.is_file():
        raise FileNotFoundError(f"{out_json} is missing")

    dfs_dir_json = pcs.storage.put_file(out_json)

    # send to downstream
    json_output = JSONFile(resource=dfs_dir_json)
    pcs.to_downstream(json_output)

    return TaskResult(files=[dfs_dir_json])
