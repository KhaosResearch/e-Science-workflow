import shutil
from pathlib import Path
import docker
from drama.core.model import SimpleTabularDataset
from drama.models.task import TaskResult
from drama.process import Process


def execute(
    pcs: Process,
    index_column_first_file: str,
    index_column_second_file: str,
    delimiter: str,
    outfile_name: str,
    join_how_parameter: str = "left",
):
    """

    Name:
        Join Dataset

    Description:
        Join two csv datasets using columns as keys

    Author:
        Khaos Research Group

    Parameters:
        index_column_first_file (str) -> Name of the column of the firs file. This will be use for merge datasets
        using index column as keys.
        index_column_second_file (str) -> Name of the column of the firs file. This will be use for merge datasets
        using index column as keys.
        outfile_name (str) -> Name without extension of the outfile. Example: for data.csv write data.
        delimiter (str) -> Delimiter of the output file.
        join_how_parameter (str) -> How to handle the operation of the two objects.
                                    * left (DEFAULT): use calling frame’s index (or column if on is specified)
                                    * right: use other’s index.
                                    * outer: form union of calling frame’s index (or column if on is specified) with
                                    other’s index, and sort it. lexicographically.
                                    * inner: form intersection of calling frame’s index (or column if on is specified)
                                    with other’s index, preserving the order of the calling’s one.


    Mutually Inclusive:
        index_column_first_file, index_column_second_file, outfile_name, delimiter

    Inputs:
        {name_file1}.csv
        {name_file2}.csv

    Outputs:
        SimpleTabularDataset: CSV file.

    Outfiles:
        {nome_file3}.csv

    """

    # read inputs
    inputs = pcs.get_from_upstream()

    input_file = inputs["SimpleTabularDataset"][0]
    input_file_resource = input_file["resource"]
    input_file_delimiter = input_file["delimiter"]
    local_file_path = Path(pcs.storage.get_file(input_file_resource))

    input_file_2 = inputs["SimpleTabularDatasetFileTwo"][0]
    input_file_2_resource = input_file_2["resource"]
    input_file_2_delimiter = input_file_2["delimiter"]
    local_file_2_path = Path(pcs.storage.get_file(input_file_2_resource))

    local_component_path = Path(pcs.storage.local_dir)

    # Copy file if it does not exist
    in_csv_1 = Path(local_component_path, local_file_path.name)
    if not in_csv_1.is_file():
        shutil.copyfile(local_file_path, in_csv_1)

    in_csv_2 = Path(local_component_path, local_file_2_path.name)
    if not in_csv_2.is_file():
        shutil.copyfile(local_file_2_path, in_csv_2)

    image_name = "enbic2lab/generic/join_dataset"

    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--first-file-path {local_file_path.name} --index-column-first-file {index_column_first_file} "
        f"--second-file-path {local_file_2_path.name} --index-column-second-file {index_column_second_file} "
        f"--outfile-name {outfile_name} --delimiter-file-1 {input_file_delimiter} "
        f"--delimiter-file-2 {input_file_2_delimiter} --delimiter {delimiter} "
        f"--join-how-parameter {join_how_parameter}",
        detach=True,
        tty=True,
    )

    r = container.wait()
    logs = container.logs()
    if logs:
        pcs.debug([logs.decode("utf-8")])

    container.stop()
    container.remove(v=True)

    # prepare output
    out_csv = Path(pcs.storage.local_dir, Path(outfile_name).with_suffix(".csv"))

    # send time to remote storage
    if not out_csv.is_file():
        raise FileNotFoundError(f"{out_csv} is missing")

    dfs_dir_csv = pcs.storage.put_file(out_csv)

    # send to downstream
    csv_output = SimpleTabularDataset(resource=dfs_dir_csv, delimiter=delimiter)
    pcs.to_downstream(csv_output)

    return TaskResult(files=[dfs_dir_csv])
