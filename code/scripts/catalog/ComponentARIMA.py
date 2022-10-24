import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import docker
from drama.core.model import SimpleTabularDataset
from drama.models.task import TaskResult
from drama.process import Process
from drama_enbic2lab.model import Pdf, Png

@dataclass
class PdfSeasonality(Pdf):
    pass

def execute(pcs: Process, date_column: str, pollen: str, year: int):
    f"""
    Name:
        Stationarity and Seasonality

        Description:
        Generate differents analysis based on Dickey-Fuller and ARIMA methods.

        Author:
            Khaos Research Group

        Parameters:
        * date_column (str) -> Name of the Date column
        * pollen (str) -> Name of the Pollen column
        * year (int) -> Year for decomposition

        Mutually Inclusive:
        None

        Inputs:
            SimpleTabularDataset: A CSV file with all the data processed.

        Outputs:
            SimpleTabularDataset: A CSV file with the Statistics.
            Pdf and Png: Multiple pdf and png files seasonality and stationality analyses.

        Outfiles:
            * SARIMAX_plots.pdf
            * DickerFuller_seasonality.csv
            * decompose.pdf
            * DickeyFuller_plot.png
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
    image_name = "enbic2lab/air/arima"
    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--filepath '{local_file_path.name}' --delimiter '{input_file_delimiter}' --pollen '{pollen}' --date-column '{date_column}' --year {year}",
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
    out_csv = Path(pcs.storage.local_dir, "DickerFuller_seasonality.csv")
    # send time to remote storage
    if not out_csv.is_file():
        raise FileNotFoundError(f"{out_csv} is missing")

    dfs_dir_csv = pcs.storage.put_file(out_csv)

    # send to downstream
    output_csv = SimpleTabularDataset(resource=dfs_dir_csv, delimiter=input_file_delimiter)
    pcs.to_downstream(output_csv)

    # Outputs
    out_pdf_sarimax = Path(pcs.storage.local_dir, "SARIMAX_plots.pdf")
    # send time to remote storage
    if not out_pdf_sarimax.is_file():
        raise FileNotFoundError(f"{out_pdf_sarimax} is missing")

    dfs_dir_pdf_sarimax = pcs.storage.put_file(out_pdf_sarimax)

    # send to downstream
    output_pdf_sarimax = Pdf(dfs_dir_pdf_sarimax)
    pcs.to_downstream(output_pdf_sarimax)

    # Outputs
    out_pdf_seasonality = Path(pcs.storage.local_dir, "decompose.pdf")
    # send time to remote storage
    if not out_pdf_seasonality.is_file():
        raise FileNotFoundError(f"{out_pdf_seasonality} is missing")

    dfs_dir_pdf_seasonality = pcs.storage.put_file(out_pdf_seasonality)

    # send to downstream
    output_pdf_seasonality = PdfSeasonality(dfs_dir_pdf_seasonality)
    pcs.to_downstream(output_pdf_seasonality)

    # Outputs
    out_png_fuller = Path(pcs.storage.local_dir, "DickeyFuller_plot.png")
    # send time to remote storage
    if not out_png_fuller.is_file():
        raise FileNotFoundError(f"{out_png_fuller} is missing")

    dfs_dir_png_fuller = pcs.storage.put_file(out_png_fuller)

    # send to downstream
    output_pdf_fuller = Png(dfs_dir_png_fuller)
    pcs.to_downstream(output_pdf_fuller)

    return TaskResult(files=[dfs_dir_csv, dfs_dir_pdf_sarimax, dfs_dir_pdf_seasonality, dfs_dir_png_fuller])
