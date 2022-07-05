import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import docker
from drama.core.model import SimpleTabularDataset
from drama.models.task import TaskResult
from drama.process import Process


@dataclass
class SimpleTabularDatasetSeries(SimpleTabularDataset):
    pass


@dataclass
class SimpleTabularDatasetTest(SimpleTabularDataset):
    pass


@dataclass
class SimpleTabularDatasetCompleted(SimpleTabularDataset):
    pass


def execute(
    pcs: Process,
    start_date: str,
    end_date: str,
    target_station: str,
    analysis_stations: list,
    completion_criteria: str = "r2",
    tests: list = ["pettit", "snht", "buishand"],
):

    """
    Name:
        Data Series Completion

    Description:
        Completion of data time series using a linear regression.

    Author:
        Khaos Research Group

    Parameters:
        start_date (str): Time series starting date.
        end_date (str): Time series ending date.
        target_station (str): Station that is desired to be completed.
        analysis_stations (list): Stations that will be used to complete the target station.
        completion_criteria (str): Value to prioritize for the completion of the series
                    Values are 'r2','slope','intercept','pair'
        tests (list): Homogeneity tests to perform
                    Values that can be included in the list are 'pettit','snht','buishand'.

    Inputs:
        TabularDataSet (SimpleTabularDataset): Data Time series to complete

    Outputs:
        TabularDataSet (SimpleTabularDataset): Data Time series completed
        TabularDataSet (SimpleTabularDatasetSeries): Linear regression fitting between stations
        TabularDataSet (SimpleTabularDatasetTest): Homogeneity Test for the completion
        TabularDataSet (SimpleTabularDatasetCompleted): Data Time completed (only which have changed)

    Outfiles:
        StationsAnalysis.csv
        (target_station)_completed.csv
        HomogeneityTests.csv
        CompletedData.csv

    """

    # read inputs
    for key, msg in pcs.poll_from_upstream():
        if key == "SimpleTabularDataset":
            input_file = msg
        elif key == "SimpleTabularDatasetMax":
            input_file = msg
        elif key == "SimpleTabularDatasetMin":
            input_file = msg

    input_file_resource = input_file["resource"]
    input_file_delimiter = input_file["delimiter"]

    local_file_path = Path(pcs.storage.get_file(input_file_resource))
    local_component_path = Path(pcs.storage.local_dir)

    # Copy file if it does not exist
    in_csv = Path(local_component_path, local_file_path.name)
    if not in_csv.is_file():
        shutil.copyfile(local_file_path, in_csv)

    tests_argument = " ".join(f'--tests "{test}"' for test in tests)

    stations_argument = " ".join(
        f'--analysis-stations "{station}"' for station in analysis_stations
    )

    image_name = "enbic2lab/water/series_completion"

    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f'--file-path "{local_file_path.name}" --start-date "{start_date}" --end-date "{end_date}" --target-station "{target_station}" '
        f'{stations_argument} --completion-criteria "{completion_criteria}" {tests_argument} --delimiter "{input_file_delimiter}"',
        detach=True,
        tty=True,
    )

    r = container.wait()
    logs = container.logs()

    if logs:
        pcs.debug([logs.decode("utf-8")])

    container.stop()
    container.remove(v=True)

    # prepare output for the analysis between stations
    out_csv_analysis = Path(pcs.storage.local_dir, "StationsAnalysis.csv")

    # send time to remote storage
    if not out_csv_analysis.is_file():
        raise FileNotFoundError(f"{out_csv_analysis} is missing")

    dfs_dir_analysis = pcs.storage.put_file(out_csv_analysis)

    # send to downstream
    analysis_csv = SimpleTabularDatasetSeries(
        resource=dfs_dir_analysis, delimiter=input_file_delimiter, file_format=".csv"
    )
    pcs.to_downstream(analysis_csv)

    # prepare output for the series completed
    target_station = re.sub("[()]", "", target_station)
    out_csv_series = Path(
        pcs.storage.local_dir, f"{target_station.replace(' ', '_')}_completed.csv"
    )

    # send time to remote storage
    if not out_csv_series.is_file():
        raise FileNotFoundError(f"{out_csv_series} is missing")

    dfs_dir_series = pcs.storage.put_file(out_csv_series)

    # send to downstream
    series_csv = SimpleTabularDataset(
        resource=dfs_dir_series, delimiter=input_file_delimiter, file_format=".csv"
    )
    pcs.to_downstream(series_csv)

    # prepare output for the homegeneity test
    out_csv_homogeneity = Path(pcs.storage.local_dir, "HomogeneityTests.csv")

    # send time to remote storage
    if not out_csv_homogeneity.is_file():
        raise FileNotFoundError(f"{out_csv_homogeneity} is missing")

    dfs_dir_test = pcs.storage.put_file(out_csv_homogeneity)

    # send to downstream
    test_csv = SimpleTabularDatasetTest(
        resource=dfs_dir_test, delimiter=input_file_delimiter, file_format=".csv"
    )
    pcs.to_downstream(test_csv)

    # prepare output for the replaced data
    out_csv_replaced = Path(pcs.storage.local_dir, "CompletedData.csv")

    # send time to remote storage
    if not out_csv_replaced.is_file():
        raise FileNotFoundError(f"{out_csv_replaced} is missing")

    dfs_dir_replaced = pcs.storage.put_file(out_csv_replaced)

    # send to downstream
    replaced_csv = SimpleTabularDatasetCompleted(
        resource=dfs_dir_replaced, delimiter=input_file_delimiter, file_format=".csv"
    )
    pcs.to_downstream(replaced_csv)

    return TaskResult(
        files=[dfs_dir_analysis, dfs_dir_series, dfs_dir_test, dfs_dir_replaced]
    )
