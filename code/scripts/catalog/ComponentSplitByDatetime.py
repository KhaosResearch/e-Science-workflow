import shutil
from pathlib import Path

import docker
from drama.core.model import SimpleTabularDataset
from drama.models.task import TaskResult
from drama.process import Process
from drama_enbic2lab.model import Pdf


def execute(pcs: Process, start_date: str, end_date: str, pollen_column: str):
    f"""

    Name:
        Split By Datetime

    Description:
        Given a pandas dataset and start date/end date, select a portion of this dataset

    Author:
        Khaos Research Group

    Parameters:
        * --start_date (str) -> Select start date to split the dataset
        * --end_date (str) -> Select end date to split the dataset
        * --pollen_column (str) -> Name of the date column

    Mutually Inclusive:
        None

    Inputs:
        SimpleTabularDataset: A CSV file with the dataset scaled by months.

    Outputs:
       SimpleTabularDataset: A CSV with a portion of the original dataset.
       Pdf: A pdf file that plots the pollen data.

    Outfiles:
        split_dataset.csv

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
    image_name = "enbic2lab/air/split_by_datetime"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath  '{local_file_path.name}' --start-date '{start_date}' --end-date '{end_date}' "
        f"--pollen-column '{pollen_column}' --delimiter '{input_file_delimiter}'",
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
    out_csv = Path(pcs.storage.local_dir, "split_dataset.csv")
    # send time to remote storage
    if not out_csv.is_file():
        raise FileNotFoundError(f"{out_csv} is missing")

    dfs_dir_csv = pcs.storage.put_file(out_csv)

    # send to downstream
    output_csv = SimpleTabularDataset(
        resource=dfs_dir_csv, delimiter=input_file_delimiter
    )
    pcs.to_downstream(output_csv)

    out_pdf = Path(pcs.storage.local_dir, "seasonal_plot.pdf")
    # send time to remote storage
    if not out_pdf.is_file():
        raise FileNotFoundError(f"{out_pdf} is missing")

    dfs_dir_pdf = pcs.storage.put_file(out_pdf)

    # send to downstream
    output_pdf = Pdf(resource=dfs_dir_pdf)
    pcs.to_downstream(output_pdf)

    return TaskResult(files=[dfs_dir_csv, dfs_dir_pdf])
