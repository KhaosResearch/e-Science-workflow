import shutil
from dataclasses import dataclass
from pathlib import Path

import docker
from drama.core.model import SimpleTabularDataset, TempFile
from drama.models.task import TaskResult
from drama.process import Process


@dataclass
class SimpleTabularDatasetPrediction(SimpleTabularDataset):
    pass


@dataclass
class TempFileFeatures(TempFile):
    pass


@dataclass
class TempFileTarget(TempFile):
    pass


@dataclass
class TempFileScaler(TempFile):
    pass


def execute(pcs: Process):
    f"""

    Name:
        LSTM Evaluation

    Description:
        Given X_test, y_test and the trained model, make predictions and evaluate the model

    Author:
        Khaos Research Group

    Parameters:
        None

    Mutually Inclusive:
        None

    Inputs:
        TempFile: Model numpy array file.
        TempFileFeatures: X numpy array file.
        TempFileTarget: Y numpy array file.
        TempFileScaler: Scaler target numpy array file.

    Outputs:
       SimpleTabularDataset: Model metrics csv.
       SimpleTabularDatasetPrediction: Model predictions csv.

    Outfiles:
        lstm_metrics.csv
        lstm_predictions.csv

    """

    # Inputs
    inputs = pcs.get_from_upstream()

    input_file_features = inputs["TempFileFeatures"][0]
    input_file_resource_features = input_file_features["resource"]
    local_file_path_features = Path(pcs.storage.get_file(input_file_resource_features))

    input_file_target = inputs["TempFileTarget"][0]
    input_file_resource_target = input_file_target["resource"]
    local_file_path_target = Path(pcs.storage.get_file(input_file_resource_target))

    input_file_scaler = inputs["TempFileScaler"][0]
    input_file_resource_scaler = input_file_scaler["resource"]
    local_file_path_scaler = Path(pcs.storage.get_file(input_file_resource_scaler))

    input_file_model = inputs["TempFile"][0]
    input_file_resource_model = input_file_model["resource"]
    local_file_path_model = Path(pcs.storage.get_file(input_file_resource_model))

    local_component_path = Path(pcs.storage.local_dir)

    # Copy file if it does not exist
    in_npy_features = Path(local_component_path, local_file_path_features.name)
    if not in_npy_features.is_file():
        shutil.copyfile(local_file_path_features, in_npy_features)

    in_npy_target = Path(local_component_path, local_file_path_target.name)
    if not in_npy_target.is_file():
        shutil.copyfile(local_file_path_target, in_npy_target)

    in_pkl_scaler = Path(local_component_path, local_file_path_scaler.name)
    if not in_pkl_scaler.is_file():
        shutil.copyfile(local_file_path_scaler, in_pkl_scaler)

    in_hdf5_model = Path(local_component_path, local_file_path_model.name)
    if not in_hdf5_model.is_file():
        shutil.copyfile(local_file_path_model, in_hdf5_model)

    # Docker
    image_name = "enbic2lab/air/lstm_evaluation"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath-x '{local_file_path_features.name}' --filepath-y '{local_file_path_target.name}' --filepath-model '{local_file_path_model.name}' "
        f"--filepath-scaler-y '{local_file_path_scaler.name}' --delimiter ';' ",
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
    out_csv_metrics = Path(pcs.storage.local_dir, "lstm_metrics.csv")
    # send time to remote storage
    if not out_csv_metrics.is_file():
        raise FileNotFoundError(f"{out_csv_metrics} is missing")

    dfs_dir_metrics = pcs.storage.put_file(out_csv_metrics)

    # send to downstream
    metrics_csv = SimpleTabularDataset(resource=dfs_dir_metrics, delimiter=";")
    pcs.to_downstream(metrics_csv)

    # prepare output
    out_csv_prediction = Path(pcs.storage.local_dir, "lstm_predictions.csv")
    # send time to remote storage
    if not out_csv_prediction.is_file():
        raise FileNotFoundError(f"{out_csv_prediction} is missing")

    dfs_dir_prediction = pcs.storage.put_file(out_csv_prediction)

    # send to downstream
    prediction_csv = SimpleTabularDatasetPrediction(
        resource=dfs_dir_prediction, delimiter=";"
    )
    pcs.to_downstream(prediction_csv)

    return TaskResult(files=[dfs_dir_metrics, dfs_dir_prediction])
