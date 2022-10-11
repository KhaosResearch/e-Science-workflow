import fnmatch
import glob
import os
import re
import shutil
from pathlib import Path

import docker
from drama.core.model import SimpleTabularDataset
from drama.models.task import TaskResult
from drama.process import Process


def execute(
    pcs: Process,
):
    """

    Name:
        Data Control Selection

    Description:
    Select the best CSV by metrics comparison.

    Author:
        Khaos Research Group

    Parameters:
        None

    Mutually Inclusive:
        None

    Inputs:
        SimpleTabularDataset: A CSV file with the original dataset.
        SimpleTabularDatasetMean: A CSV file with a mean interpolation of the values of the same variables in different years of the dataset.
        SimpleTabularDatasetSpline: A CSV file with the spline interpolation method from pandas.
        SimpleTabularDatasetLinear: A CSV file with the linear interpolation method from pandas.
        SimpleTabularDatasetTest: A CSV file with the metrics of the Random Forest.

    Outputs:
        SimpleTabularDataset: A CSV file with the chosen interpolation method dataset.

    Outfiles:
        filepath_metrics.csv

    """

    # Input
    inputs = pcs.get_from_upstream()

    input_file = inputs["SimpleTabularDataset"][0]
    input_file_resource = input_file["resource"]
    input_file_delimiter = input_file["delimiter"]
    local_file_path = Path(pcs.storage.get_file(input_file_resource))

    # Input Mean Interpolation

    input_file_mean = inputs["SimpleTabularDatasetMean"][0]
    input_file_resource_mean = input_file_mean["resource"]
    input_file_delimiter_mean = input_file_mean["delimiter"]
    local_file_path_mean = Path(pcs.storage.get_file(input_file_resource_mean))

    # Input Spline Interpolation

    input_file_spline = inputs["SimpleTabularDatasetSpline"][0]
    input_file_resource_spline = input_file_spline["resource"]
    input_file_delimiter_spline = input_file_spline["delimiter"]
    local_file_path_spline = Path(pcs.storage.get_file(input_file_resource_spline))

    # Input Linear Interpolation

    input_file_linear = inputs["SimpleTabularDatasetLinear"][0]
    input_file_resource_linear = input_file_linear["resource"]
    input_file_delimiter_linear = input_file_linear["delimiter"]
    local_file_path_linear = Path(pcs.storage.get_file(input_file_resource_linear))

    # Input Metrics

    input_file_test = inputs["SimpleTabularDatasetTest"][0]
    input_file_resource_test = input_file_test["resource"]
    input_file_delimiter_test = input_file_test["delimiter"]
    local_file_path_test = Path(pcs.storage.get_file(input_file_resource_test))

    local_component_path = Path(pcs.storage.local_dir)

    # Copy file if it does not exist
    in_csv = Path(local_component_path, local_file_path.name)
    if not in_csv.is_file():
        shutil.copyfile(local_file_path, in_csv)

    in_csv_mean = Path(local_component_path, local_file_path_mean.name)
    if not in_csv_mean.is_file():
        shutil.copyfile(local_file_path_mean, in_csv_mean)

    in_csv_spline = Path(local_component_path, local_file_path_spline.name)
    if not in_csv_spline.is_file():
        shutil.copyfile(local_file_path_spline, in_csv_spline)

    in_csv_linear = Path(local_component_path, local_file_path_linear.name)
    if not in_csv_linear.is_file():
        shutil.copyfile(local_file_path_linear, in_csv_linear)

    in_csv_test = Path(local_component_path, local_file_path_test.name)
    if not in_csv_test.is_file():
        shutil.copyfile(local_file_path_test, in_csv_test)

    # Docker
    image_name = "enbic2lab/air/choose_metric_csv"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath-no-interpolation '{local_file_path.name}' --delimiter {input_file_delimiter} --filepath-metrics '{local_file_path_test.name}' --filepath-line '{local_file_path_linear.name}' --filepath-mean '{local_file_path_mean.name}' --filepath-spline '{local_file_path_spline.name}'",
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
    rootdir = str(pcs.storage.local_dir)

    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if fnmatch.fnmatch(file, "best*"):
                filtered = file
                break

    out_csv = Path(pcs.storage.local_dir, filtered)

    # send time to remote storage
    if not out_csv.is_file():
        raise FileNotFoundError(f"{out_csv} is missing")

    dfs_dir = pcs.storage.put_file(out_csv)

    # send to downstream
    output_csv = SimpleTabularDataset(resource=dfs_dir, delimiter=input_file_delimiter)
    pcs.to_downstream(output_csv)

    return TaskResult(files=[dfs_dir])
