import shutil
import typer
from scripts.config import settings
from minio import Minio
from pathlib import Path
from typing import Annotated
from pymongo import MongoClient

def downloadFromMinio(
    component_name: str = typer.Option(..., help="Name of component to test"),
    filename: str = typer.Option(..., help="Name of file to download"),
    dest_dir: Annotated[str, typer.Option(..., help='Destination folder')] = "./"
):

    client = Minio(
        settings.MINIO_HOST,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
    )

    path = Path("data-set", component_name, filename)

    client.fget_object(settings.MINIO_BUCKET, str(path), filename)
        
    shutil.move(filename, f"{dest_dir}/{filename}")


if __name__ == "__main__":
    typer.run(downloadFromMinio)


def findOneFromMongo():
    client = MongoClient(host=settings.MONGO_HOST, username=settings.MONGO_USERNAME, password=settings.MONGO_ACCESS_KEY)
    db = client[settings.MONGO_DATABASE]
    collection = db[settings.MONGO_COLLECTION]
    return collection.find_one()
