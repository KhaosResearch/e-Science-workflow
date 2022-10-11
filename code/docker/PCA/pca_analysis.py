import os
from pathlib import Path

import numpy as np
import pandas as pd
import typer
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def pca_analysis(
    filepath: str = typer.Option(..., help="File path of the csv file"),
    delimiter: str = typer.Option(
        ..., help="Delimiter of the input file and output file. Must be the same"
    ),
):
    """
    Given a pandas dataset perform a PCA analysis to select the most important features
    """
    os.chdir("data")

    # Read dataframe
    dataframe = pd.read_csv(filepath, sep=delimiter, index_col="date")

    X = dataframe.values
    sc = StandardScaler()
    X_std = sc.fit_transform(X)
    pca = PCA(n_components=0.7, svd_solver="full")
    pca.fit(X_std)

    n_pcs = pca.n_components_

    # get the index of the most important feature on EACH component
    most_important = [np.abs(pca.components_[i]).argmax() for i in range(n_pcs)]
    initial_feature_names = dataframe.columns

    # get the most important feature names
    most_important_names = [
        initial_feature_names[most_important[i]] for i in range(n_pcs)
    ]

    most_important_names.append("pollen")

    cols = sorted(list(set(most_important_names)))

    # Save Outfile
    dirname = ""
    filename = "pca_dataset"
    suffix = ".csv"
    path = Path(dirname, filename).with_suffix(suffix)

    dataframe[cols].to_csv(path, sep=delimiter)


# ============ MAIN ============
if __name__ == "__main__":
    typer.run(pca_analysis)
