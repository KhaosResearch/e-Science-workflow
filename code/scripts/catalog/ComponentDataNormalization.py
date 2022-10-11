import shutil
from dataclasses import dataclass
from pathlib import Path

import docker
from drama.core.model import SimpleTabularDataset, TempFile
from drama.models.task import TaskResult
from drama.process import Process


@dataclass
class SimpleTabularDatasetTarget(SimpleTabularDataset):
    pass


@dataclass
class TempFileTarget(TempFile):
    pass


def execute(pcs: Process):
    f"""

    Name:
        Data Normalization

    Description:
        Given a pandas dataframe, it's split in two dataframes (features and target) and then they are normalized with MinMaxScaler

    Author:
        Khaos Research Group

    Parameters:
        None

    Mutually Inclusive:
        None

    Inputs:
        SimpleTabularDataset: A CSV with the PCA analysis.

    Outputs:
       SimpleTabularDataset: Features normalized dataset.
       SimpleTabularDatasetTarget: Target normalized dataset.
       TempFile: Features scaler with .pkl format.
       TempFileTarget: Target scaler with .pkl format.

    Outfiles:
        dataset_norm_features.csv
        dataset_norm_target.csv
        scaler_features.pkl
        scaler_target.pkl

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
    image_name = "enbic2lab/air/data_normalization"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath '{local_file_path.name}' --delimiter '{input_file_delimiter}' ",
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
    out_csv_features = Path(pcs.storage.local_dir, "dataset_norm_features.csv")
    # send time to remote storage
    if not out_csv_features.is_file():
        raise FileNotFoundError(f"{out_csv_features} is missing")

    dfs_dir_features = pcs.storage.put_file(out_csv_features)

    # send to downstream
    features_csv = SimpleTabularDataset(
        resource=dfs_dir_features, delimiter=input_file_delimiter
    )
    pcs.to_downstream(features_csv)

    # prepare output
    out_csv_target = Path(pcs.storage.local_dir, "dataset_norm_target.csv")
    # send time to remote storage
    if not out_csv_target.is_file():
        raise FileNotFoundError(f"{out_csv_target} is missing")

    dfs_dir_target = pcs.storage.put_file(out_csv_target)

    # send to downstream
    target_csv = SimpleTabularDatasetTarget(
        resource=dfs_dir_target, delimiter=input_file_delimiter
    )
    pcs.to_downstream(target_csv)

    # prepare output
    out_pkl_features = Path(pcs.storage.local_dir, "scaler_features.pkl")
    # send time to remote storage
    if not out_pkl_features.is_file():
        raise FileNotFoundError(f"{out_pkl_features} is missing")

    dfs_dir_pkl_features = pcs.storage.put_file(out_pkl_features)

    # send to downstream
    features_pkl = TempFile(resource=dfs_dir_pkl_features)
    pcs.to_downstream(features_pkl)

    # prepare output
    out_pkl_target = Path(pcs.storage.local_dir, "scaler_target.pkl")
    # send time to remote storage
    if not out_pkl_target.is_file():
        raise FileNotFoundError(f"{out_pkl_target} is missing")

    dfs_dir_pkl_target = pcs.storage.put_file(out_pkl_target)

    # send to downstream
    target_pkl = TempFileTarget(resource=dfs_dir_pkl_target)
    pcs.to_downstream(target_pkl)

    return TaskResult(
        files=[
            dfs_dir_features,
            dfs_dir_target,
            dfs_dir_pkl_features,
            dfs_dir_pkl_target,
        ]
    )
