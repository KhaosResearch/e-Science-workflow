import json
import os
from datetime import datetime

import typer
from pymongo import MongoClient


# ============ METHODS ============
def aemet_upload_db(
    input_filepath: str = typer.Option(..., help="File path of the JSON file"),
    user: str = typer.Option(..., help="Username of MongoDB"),
    password: str = typer.Option(..., help="Password of MongoDB"),
    path: str = typer.Option(..., help="Mongo Path of MongoDB"),
    database: str = typer.Option(..., help="Mongo Database"),
    collection: str = typer.Option(..., help="Mongo Collection of MongoDB"),
):
    # Switch Working Dir
    os.chdir("data")

    # Connect to MongoDB
    c = MongoClient(path, username=user, password=password)
    db = c[database]
    collection = db[collection]

    # Read File
    f = open(input_filepath)
    json_data = json.load(f)

    # Upload File
    for data in json_data:
        data["fecha"] = datetime.strptime(data["fecha"], "%Y-%m-%d")
        collection.update_one({"fecha": data["fecha"]}, {"$set": data}, upsert=True)


# ============ MAIN ============
if __name__ == "__main__":
    typer.run(aemet_upload_db)
