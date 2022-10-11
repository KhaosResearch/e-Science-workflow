import shutil
from dataclasses import dataclass
from pathlib import Path

import docker
from drama.core.model import SimpleTabularDataset, TempFile
from drama.models.task import TaskResult
from drama.process import Process


@dataclass
class SimpleTabularDatasetTest(SimpleTabularDataset):
    pass


def execute(pcs: Process, seasonality: int):
    f"""

    Name:
        Data Normalization

    Description:
        Given a pandas dataframe, it is normalized with MinMaxScaler

    Author:
        Khaos Research Group

    Parameters:
        * --seasonality (int) -> Seasonality of the pollen type of the dataset

    Mutually Inclusive:
        None

    Inputs:
        SimpleTabularDataset: A CSV with the PCA analysis.

    Outputs:
       SimpleTabularDataset: Sarima X_test.
       SimpleTabularDatasetTest: Sarima Y_test.
       TempFile: Sarima model with .pkl format.

    Outfiles:
        Sarima_X_test.csv
        Sarima_Y_test.csv
        Sarima_model.pkl

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
    image_name = "enbic2lab/air/sarima_model"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath  '{local_file_path.name}' --seasonality {seasonality} --delimiter '{input_file_delimiter}' ",
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
    out_csv_x_test = Path(pcs.storage.local_dir, "Sarima_X_test.csv")
    # send time to remote storage
    if not out_csv_x_test.is_file():
        raise FileNotFoundError(f"{out_csv_x_test} is missing")

    dfs_dir_x_test = pcs.storage.put_file(out_csv_x_test)

    # send to downstream
    x_test_csv = SimpleTabularDataset(
        resource=dfs_dir_x_test, delimiter=input_file_delimiter
    )
    pcs.to_downstream(x_test_csv)

    # prepare output
    out_csv_y_test = Path(pcs.storage.local_dir, "Sarima_Y_test.csv")
    # send time to remote storage
    if not out_csv_y_test.is_file():
        raise FileNotFoundError(f"{out_csv_y_test} is missing")

    dfs_dir_y_test = pcs.storage.put_file(out_csv_y_test)

    # send to downstream
    y_test_csv = SimpleTabularDatasetTest(
        resource=dfs_dir_y_test, delimiter=input_file_delimiter
    )
    pcs.to_downstream(y_test_csv)

    # prepare output
    out_pkl_model = Path(pcs.storage.local_dir, "Sarima_model.pkl")
    # send time to remote storage
    if not out_pkl_model.is_file():
        raise FileNotFoundError(f"{out_pkl_model} is missing")

    dfs_dir_pkl_model = pcs.storage.put_file(out_pkl_model)

    # send to downstream
    model_pkl = TempFile(resource=dfs_dir_pkl_model)
    pcs.to_downstream(model_pkl)

    return TaskResult(files=[dfs_dir_x_test, dfs_dir_y_test, dfs_dir_pkl_model])
