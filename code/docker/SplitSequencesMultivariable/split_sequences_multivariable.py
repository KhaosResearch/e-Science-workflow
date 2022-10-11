import os
from pathlib import Path

import numpy as np
import typer
from numpy import loadtxt, save, savetxt


def split_sequences_multivariable(
    filepath_features: str = typer.Option(
        ..., help="File path of the features csv file"
    ),
    filepath_target: str = typer.Option(..., help="File path of the target csv file"),
    n_steps_in: int = typer.Option(..., help="Select time window to train the model"),
    n_steps_out: int = typer.Option(..., help="Select period of time to predict"),
    delimiter: str = typer.Option(
        ..., help="Delimiter of the input file and output file. Must be the same"
    ),
):
    """
    Generates supervised data from a multidimensional array.

    Returns both data and its target for supervised learning
    """

    os.chdir("data")

    # Load array from CSV
    sequences_x = loadtxt(filepath_features, delimiter=delimiter)
    sequences_y = loadtxt(filepath_target, delimiter=delimiter)

    X, y = list(), list()
    for i in range(len(sequences_x)):
        # find the end of this pattern
        end_ix = i + n_steps_in
        out_end_ix = end_ix + n_steps_out - 1
        # check if we are beyond the dataset
        if out_end_ix > len(sequences_x):
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequences_x[i:end_ix, :-1], sequences_y[end_ix - 1 : out_end_ix]
        X.append(seq_x)
        y.append(seq_y)

    X = np.array(X)
    y = np.array(y)

    # Save numpy array
    dirname = ""
    filename = "sequences_X"
    filename_target = "sequences_Y"
    suffix = ".csv"
    path = Path(dirname, filename)
    path_target = Path(dirname, filename_target).with_suffix(suffix)

    # savetxt(path, X, delimiter=delimiter)
    save(path, X)
    savetxt(path_target, y, delimiter=delimiter)


# ============ MAIN ============
if __name__ == "__main__":
    typer.run(split_sequences_multivariable)
