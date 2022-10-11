import shutil
from dataclasses import dataclass
from pathlib import Path

import docker
from drama.core.model import TempFile
from drama.models.task import TaskResult
from drama.process import Process


@dataclass
class TempFileFeatures(TempFile):
    pass


@dataclass
class TempFileTarget(TempFile):
    pass


def execute(pcs: Process, n_neurons: int, n_steps_in: int, n_steps_out: int):
    f"""

    Name:
        LSTM Model

    Description:
        Given some parameters, builds a ConvLSTM model for timeseries analysis.
        Returns the built Keras model and X_test, y_test to make predictions

    Author:
        Khaos Research Group

    Parameters:
        * --n_neurons (int) -> Number of neurons for model building
        * --n_steps_in (int) -> Time window to train the model
        * --n_steps_out (int) -> Period of time to predict

    Mutually Inclusive:
        None

    Inputs:
        TempFile: X numpy array file.
        SimpleTabularDataset: Y csv file.

    Outputs:
       TempFile: LSTM model.
       TempFileFeatures: Numpy file of features (X).
       TempFileTarget: Numpy file of target (y)

    Outfiles:
        lstm_X_test.npy
        lstm_Y_test.npy
        lstm_model.hdf5

    """

    # Inputs
    inputs = pcs.get_from_upstream()

    input_file_features = inputs["TempFile"][0]
    input_file_resource_features = input_file_features["resource"]
    local_file_path_features = Path(pcs.storage.get_file(input_file_resource_features))

    input_file_target = inputs["SimpleTabularDataset"][0]
    input_file_resource_target = input_file_target["resource"]
    input_file_delimiter_target = input_file_target["delimiter"]
    local_file_path_target = Path(pcs.storage.get_file(input_file_resource_target))

    local_component_path = Path(pcs.storage.local_dir)

    # Copy file if it does not exist
    in_npy_features = Path(local_component_path, local_file_path_features.name)
    if not in_npy_features.is_file():
        shutil.copyfile(local_file_path_features, in_npy_features)

    in_csv_target = Path(local_component_path, local_file_path_target.name)
    if not in_csv_target.is_file():
        shutil.copyfile(local_file_path_target, in_csv_target)

    # Docker
    image_name = "enbic2lab/air/lstm_model"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath-x '{local_file_path_features.name}' --filepath-y '{local_file_path_target.name}' "
        f"--n-neurons {n_neurons} --n-steps-in {n_steps_in} --n-steps-out {n_steps_out} --delimiter '{input_file_delimiter_target}' ",
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
    out_npy_features = Path(pcs.storage.local_dir, "lstm_X_test.npy")
    # send time to remote storage
    if not out_npy_features.is_file():
        raise FileNotFoundError(f"{out_npy_features} is missing")

    dfs_dir_features = pcs.storage.put_file(out_npy_features)

    # send to downstream
    features_npy = TempFileFeatures(resource=dfs_dir_features)
    pcs.to_downstream(features_npy)

    # prepare output
    out_npy_target = Path(pcs.storage.local_dir, "lstm_Y_test.npy")
    # send time to remote storage
    if not out_npy_target.is_file():
        raise FileNotFoundError(f"{out_npy_target} is missing")

    dfs_dir_target = pcs.storage.put_file(out_npy_target)

    # send to downstream
    target_npy = TempFileTarget(resource=dfs_dir_target)
    pcs.to_downstream(target_npy)

    # prepare output
    out_hdf5_model = Path(pcs.storage.local_dir, "lstm_model.h5")
    # send time to remote storage
    if not out_hdf5_model.is_file():
        raise FileNotFoundError(f"{out_hdf5_model} is missing")

    dfs_dir_model = pcs.storage.put_file(out_hdf5_model)

    # send to downstream
    model_hdf5 = TempFile(resource=dfs_dir_model)
    pcs.to_downstream(model_hdf5)

    return TaskResult(files=[dfs_dir_features, dfs_dir_target, dfs_dir_model])
