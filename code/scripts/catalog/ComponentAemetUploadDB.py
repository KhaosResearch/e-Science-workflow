import shutil
from pathlib import Path

import docker
from drama.process import Process


def execute(pcs: Process, user: str, password: str, path: str, collection: str):

    """
    Name:
        Upload to DB

    Description:
        Upload an Aemet JSON file into MongoDB

    Author:
        Khaos Research Group

    Parameters:
        collection (str): Name of collection on MongoDB
        user (str): Host of MongoDB
        password (str): Password of MongoDB
        path (str): Url of MongoDB

    Inputs:
        InputFile (JSONFile)

    Mutual Inclusive:
    username, password, mongopath and collection

    Outputs:
    None

    Outfiles:
    None

    """

    # read inputs
    inputs = pcs.get_from_upstream()
    input_file = inputs["JSONFile"][0]
    input_file_resource = input_file["resource"]
    local_file_path = Path(pcs.storage.get_file(input_file_resource))
    local_component_path = Path(pcs.storage.local_dir)

    # Copy file if it does not exist
    in_json = Path(local_component_path, local_file_path.name)
    if not in_json.is_file():
        shutil.copyfile(local_file_path, in_json)

    image_name = "enbic2lab/air/aemet_upload_database"

    # get docker image
    client = docker.from_env()
    container = client.containers.run(
        image=image_name,
        volumes={local_component_path: {"bind": "/usr/local/src/data", "mode": "rw"}},
        command=f"--input-filepath {local_file_path.name} --collection '{collection}' --user '{user}' "
        f"--password '{password}' --path {path}",
        detach=True,
        tty=True,
    )

    r = container.wait()
    logs = container.logs()
    if logs:
        pcs.debug([logs.decode("utf-8")])

    container.stop()
    container.remove(v=True)
