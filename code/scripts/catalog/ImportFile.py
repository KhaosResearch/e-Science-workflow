import urllib.request
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from drama.core.model import TempFile, CompressedFile, SimpleTabularDataset
from drama_enbic2lab.model import XMLFile, ExcelDataset, SavFile
from drama.models.task import TaskResult
from drama.process import Process
from drama.storage.base import NotValidScheme


def execute(
    pcs: Process,
    url: str,
    delimiter: str = ";",
    parameters: Optional[str] = None,
    **kwargs
) -> TaskResult:
    """
    Name:
        Import File
    
    Description:
    Imports a file from an online resource given its url.
    
    Args:
        pcs (Process)
    
    Parameters:
        url (str): Public accessible resource. It can be a URI or a url.
        parameters (str): GET parameters to append to url.
        delimiter (str): Delimiter required for some files.

    """
    try:
        filepath = pcs.storage.get_file(url)
    except (NotValidScheme, FileNotFoundError):
        pcs.warn("No valid scheme was provided")
        filename = Path(urlparse(url).path).name
        filepath = Path(pcs.storage.local_dir, filename)
        if parameters:
            url = url + parameters
        urllib.request.urlretrieve(url, filepath)

    # send to remote storage
    dfs_dir = pcs.storage.put_file(filepath)

    # send to downstream
    output_suffix = Path(filepath).suffix
    if output_suffix == ".csv":
        output_file = SimpleTabularDataset(resource=dfs_dir, delimiter=delimiter)
    elif output_suffix == ".xlsx":
        output_file = ExcelDataset(resource=dfs_dir, file_format=".xlsx")
    elif output_suffix == ".xml":
        output_file = XMLFile(resource=dfs_dir)
    elif output_suffix == ".zip":
        output_file = CompressedFile(resource=dfs_dir)
    elif output_suffix == ".json":
        output_file = JSONFile(resource=dfs_dir)
    elif output_suffix == ".sav":
        output_file = SavFile(resource=dfs_dir)
    else:
        output_file = TempFile(resource=dfs_dir)
    print(output_suffix)

    pcs.to_downstream(output_file)

    return TaskResult(files=[dfs_dir])
