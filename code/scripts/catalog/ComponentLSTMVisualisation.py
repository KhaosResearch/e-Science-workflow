import shutil
from dataclasses import dataclass
from pathlib import Path

import docker
from drama.core.model import SimpleTabularDataset
from drama.models.task import TaskResult
from drama.process import Process
from drama_enbic2lab.model import Png


@dataclass
class SimpleTabularDatasetPrediction(SimpleTabularDataset):
    pass


def execute(pcs: Process, start_date: str, n_steps_out: int):
    f"""

    Name:
        LSTM Visualisation

    Description:
        Given the complete dataset, the prediction array, pollen type and the start date
        Returns the R2 visualisation

    Author:
        Khaos Research Group

    Parameters:
        * --start_date (str) -> Start date to visualise the plot
        * --n_steps_out (int) -> Number of steps to predict

    Mutually Inclusive:
        None

    Inputs:
        SimpleTabularDataset: Complete dataset csv.
        SimpleTabularDatasetPrediction: Model predictions csv.

    Outputs:
       Png: Visualisation plot.

    Outfiles:
        lstm_visualisation.png

    """

    # Inputs
    inputs = pcs.get_from_upstream()

    input_file = inputs["SimpleTabularDataset"][0]
    input_file_resource = input_file["resource"]
    input_file_delimiter = input_file["delimiter"]
    local_file_path = Path(pcs.storage.get_file(input_file_resource))

    input_file_prediction = inputs["SimpleTabularDatasetPrediction"][0]
    input_file_resource_prediction = input_file_prediction["resource"]
    input_file_delimiter_prediction = input_file_prediction["delimiter"]
    local_file_path_prediction = Path(
        pcs.storage.get_file(input_file_resource_prediction)
    )

    local_component_path = Path(pcs.storage.local_dir)

    # Copy file if it does not exist
    in_csv = Path(local_component_path, local_file_path.name)
    if not in_csv.is_file():
        shutil.copyfile(local_file_path, in_csv)

    in_csv_prediction = Path(local_component_path, local_file_path_prediction.name)
    if not in_csv_prediction.is_file():
        shutil.copyfile(local_file_path_prediction, in_csv_prediction)

    # Docker
    image_name = "enbic2lab/air/lstm_visualisation"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath '{local_file_path.name}' --filepath-prediction '{local_file_path_prediction.name}' "
        f"--start-date '{start_date}' --n-steps-out {n_steps_out} --delimiter '{input_file_delimiter}' ",
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
    out_png = Path(pcs.storage.local_dir, "lstm_visualisation.png")
    # send time to remote storage
    if not out_png.is_file():
        raise FileNotFoundError(f"{out_png} is missing")

    dfs_dir = pcs.storage.put_file(out_png)

    # send to downstream
    output_png = Png(resource=dfs_dir)
    pcs.to_downstream(output_png)

    return TaskResult(files=[dfs_dir])
