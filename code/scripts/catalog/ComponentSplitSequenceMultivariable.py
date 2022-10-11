import shutil
from dataclasses import dataclass
from pathlib import Path

import docker
from drama.core.model import SimpleTabularDataset, TempFile
from drama.models.task import TaskResult
from drama.process import Process


def execute(pcs: Process, n_steps_in: int, n_steps_out: int):
    f"""

    Name:
        Split Sequence Multivariable

    Description:
        Generates supervised data from a multidimensional array. Returns both data and its target for supervised learning.

    Author:
        Khaos Research Group

    Parameters:
        * --n_steps_in (int) -> Select time window to train the model
        * --n_steps_out (int) -> Select period of time to predict

    Mutually Inclusive:
        None

    Inputs:
        SimpleTabularDataset: Features csv file.
        SimpleTabularDatasetTarget: Target csv file.

    Outputs:
       TempFile: Sequence features (numpy array).
       SimpleTabularDataset: Sequence target.

    Outfiles:
        sequence_X.npy
        sequence_Y.csv

    """

    # Inputs
    inputs = pcs.get_from_upstream()

    input_file_features = inputs["SimpleTabularDataset"][0]
    input_file_resource_features = input_file_features["resource"]
    input_file_delimiter_features = input_file_features["delimiter"]
    local_file_path_features = Path(pcs.storage.get_file(input_file_resource_features))

    input_file_target = inputs["SimpleTabularDatasetTarget"][0]
    input_file_resource_target = input_file_target["resource"]
    input_file_delimiter_target = input_file_target["delimiter"]
    local_file_path_target = Path(pcs.storage.get_file(input_file_resource_target))

    local_component_path = Path(pcs.storage.local_dir)

    # Copy file if it does not exist
    in_csv_features = Path(local_component_path, local_file_path_features.name)
    if not in_csv_features.is_file():
        shutil.copyfile(local_file_path_features, in_csv_features)

    in_csv_target = Path(local_component_path, local_file_path_target.name)
    if not in_csv_target.is_file():
        shutil.copyfile(local_file_path_target, in_csv_target)

    # Docker
    image_name = "enbic2lab/air/split_sequences_multivariable"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath-features '{local_file_path_features.name}' --filepath-target '{local_file_path_target.name}' "
        f"--n-steps-in {n_steps_in} --n-steps-out {n_steps_out} --delimiter '{input_file_delimiter_features}' ",
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
    # prepare output
    out_csv_features = Path(pcs.storage.local_dir, "sequences_X.npy")
    # send time to remote storage
    if not out_csv_features.is_file():
        raise FileNotFoundError(f"{out_csv_features} is missing")

    dfs_dir_features = pcs.storage.put_file(out_csv_features)

    # send to downstream
    features_csv = TempFile(resource=dfs_dir_features)
    pcs.to_downstream(features_csv)

    # prepare output
    out_csv_target = Path(pcs.storage.local_dir, "sequences_Y.csv")
    # send time to remote storage
    if not out_csv_target.is_file():
        raise FileNotFoundError(f"{out_csv_target} is missing")

    dfs_dir_target = pcs.storage.put_file(out_csv_target)

    # send to downstream
    target_csv = SimpleTabularDataset(
        resource=dfs_dir_target, delimiter=input_file_delimiter_features
    )
    pcs.to_downstream(target_csv)

    return TaskResult(files=[dfs_dir_features, dfs_dir_target])
