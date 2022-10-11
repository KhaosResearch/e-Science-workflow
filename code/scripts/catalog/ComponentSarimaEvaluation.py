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


def execute(pcs: Process, validation_time: str):
    f"""

    Name:
        SARIMA Evaluation

    Description:
        Given X_test, y_test and the trained model, make predictions and evaluate the model

    Author:
        Khaos Research Group

    Parameters:
        * --validation_time (str) -> Indicate from which period of time you want to make the validation

    Mutually Inclusive:
        None

    Inputs:
        SimpleTabularDataset: File path of X_test csv file.
        SimpleTabularDatasetTest: File path of Y_test csv file.
        TempFile: File path of the model with .pkl format.

    Outputs:
       SimpleTabularDataset: Model metrics.
       SimpleTabularDatasetPrediction: Model predictions.

    Outfiles:
        Sarima_metrics.csv
        Sarima_predictions.csv

    """

    # Inputs
    inputs = pcs.get_from_upstream()

    input_file_x_test = inputs["SimpleTabularDataset"][0]
    input_file_resource_x_test = input_file_x_test["resource"]
    input_file_delimiter_x_test = input_file_x_test["delimiter"]
    local_file_path_x_test = Path(pcs.storage.get_file(input_file_resource_x_test))

    input_file_y_test = inputs["SimpleTabularDatasetTest"][0]
    input_file_resource_y_test = input_file_y_test["resource"]
    input_file_delimiter_y_test = input_file_y_test["delimiter"]
    local_file_path_y_test = Path(pcs.storage.get_file(input_file_resource_y_test))

    input_file_model = inputs["TempFile"][0]
    input_file_resource_model = input_file_model["resource"]
    local_file_path_model = Path(pcs.storage.get_file(input_file_resource_model))

    local_component_path = Path(pcs.storage.local_dir)

    # Copy file if it does not exist
    in_csv_x_test = Path(local_component_path, local_file_path_x_test.name)
    if not in_csv_x_test.is_file():
        shutil.copyfile(local_file_path_x_test, in_csv_x_test)

    in_csv_y_test = Path(local_component_path, local_file_path_y_test.name)
    if not in_csv_y_test.is_file():
        shutil.copyfile(local_file_path_y_test, in_csv_y_test)

    in_pkl_model = Path(local_component_path, local_file_path_model.name)
    if not in_pkl_model.is_file():
        shutil.copyfile(local_file_path_model, in_pkl_model)

    # Docker
    image_name = "enbic2lab/air/sarima_evaluation"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath-x '{local_file_path_x_test.name}' --filepath-y '{local_file_path_y_test.name}' --filepath-model '{local_file_path_model.name}' "
        f"--validation-time '{validation_time}' --delimiter '{input_file_delimiter_x_test}' ",
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
    out_csv_metrics = Path(pcs.storage.local_dir, "Sarima_metrics.csv")
    # send time to remote storage
    if not out_csv_metrics.is_file():
        raise FileNotFoundError(f"{out_csv_metrics} is missing")

    dfs_dir_metrics = pcs.storage.put_file(out_csv_metrics)

    # send to downstream
    metrics_csv = SimpleTabularDataset(
        resource=dfs_dir_metrics, delimiter=input_file_delimiter_x_test
    )
    pcs.to_downstream(metrics_csv)

    # prepare output
    out_csv_prediction = Path(pcs.storage.local_dir, "Sarima_predictions.csv")
    # send time to remote storage
    if not out_csv_prediction.is_file():
        raise FileNotFoundError(f"{out_csv_prediction} is missing")

    dfs_dir_prediction = pcs.storage.put_file(out_csv_prediction)

    # send to downstream
    prediction_csv = SimpleTabularDatasetPrediction(
        resource=dfs_dir_prediction, delimiter=input_file_delimiter_x_test
    )
    pcs.to_downstream(prediction_csv)

    return TaskResult(files=[dfs_dir_metrics, dfs_dir_prediction])
