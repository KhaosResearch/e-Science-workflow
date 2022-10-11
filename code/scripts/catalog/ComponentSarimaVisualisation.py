import shutil
from dataclasses import dataclass
from pathlib import Path

import docker
from drama.core.model import SimpleTabularDataset
from drama.models.task import TaskResult
from drama.process import Process
from drama_enbic2lab.model import Png


@dataclass
class SimpleTabularDatasetTest(SimpleTabularDataset):
    pass


@dataclass
class SimpleTabularDatasetPrediction(SimpleTabularDataset):
    pass


def execute(pcs: Process, validation_time: str):
    f"""

    Name:
        SARIMA Visualisation

    Description:
        Given the prediction array and the start date for validation, it returns the R2 visualisation

    Author:
        Khaos Research Group

    Parameters:
        * --validation_time (str) -> Indicate from which period of time you want to make the visualisation

    Mutually Inclusive:
        None

    Inputs:
        SimpleTabularDatasetTest: Y_test csv file.
        SimpleTabularDatasetPrediction: Sarima predictions csv file.

    Outputs:
       Png: R2 visualisation plot.

    Outfiles:
        Sarima_visualisation.png

    """

    # Inputs
    inputs = pcs.get_from_upstream()

    input_file_y_test = inputs["SimpleTabularDatasetTest"][0]
    input_file_resource_y_test = input_file_y_test["resource"]
    input_file_delimiter_y_test = input_file_y_test["delimiter"]
    local_file_path_y_test = Path(pcs.storage.get_file(input_file_resource_y_test))

    input_file_prediction = inputs["SimpleTabularDatasetPrediction"][0]
    input_file_resource_prediction = input_file_prediction["resource"]
    input_file_delimiter_prediction = input_file_prediction["delimiter"]
    local_file_path_prediction = Path(
        pcs.storage.get_file(input_file_resource_prediction)
    )

    local_component_path = Path(pcs.storage.local_dir)

    # Copy file if it does not exist
    in_csv_y_test = Path(local_component_path, local_file_path_y_test.name)
    if not in_csv_y_test.is_file():
        shutil.copyfile(local_file_path_y_test, in_csv_y_test)

    in_csv_prediction = Path(local_component_path, local_file_path_prediction.name)
    if not in_csv_prediction.is_file():
        shutil.copyfile(local_file_path_prediction, in_csv_prediction)

    # Docker
    image_name = "enbic2lab/air/sarima_visualisation"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath '{local_file_path_y_test.name}' --filepath-prediction '{local_file_path_prediction.name}' "
        f"--validation-time '{validation_time}' --delimiter '{input_file_delimiter_y_test}' ",
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
    out_png = Path(pcs.storage.local_dir, "Sarima_visualisation.png")
    # send time to remote storage
    if not out_png.is_file():
        raise FileNotFoundError(f"{out_png} is missing")

    dfs_dir = pcs.storage.put_file(out_png)

    # send to downstream
    output_png = Png(resource=dfs_dir)
    pcs.to_downstream(output_png)

    return TaskResult(files=[dfs_dir])
