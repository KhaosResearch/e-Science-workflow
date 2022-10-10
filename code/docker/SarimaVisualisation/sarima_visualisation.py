#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 15:46:33 2022

@author: sandro
"""
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import typer
from numpy import loadtxt


def sarima_visualisation(
    filepath: str = typer.Option(..., help="File path of Y_test csv file"),
    filepath_prediction: str = typer.Option(
        ..., help="File path of the sarima predictions"
    ),
    delimiter: str = typer.Option(
        ..., help="Delimiter of the input file and output file. Must be the same"
    ),
    validation_time: str = typer.Option(
        ..., help="Indicate from which period of time you want to make the validation"
    ),
):
    """
    Given the prediction array, pollen type and the start date for validation

    Returns the R2 visualisation
    """

    os.chdir("data")

    dataset = pd.read_csv(filepath, sep=delimiter, index_col="date")
    mask = dataset.index >= validation_time
    dataset_pred = dataset.loc[mask]

    prediction = loadtxt(filepath_prediction, delimiter=delimiter)
    pred = pd.DataFrame()
    pred["pred"] = prediction
    pred["date"] = dataset_pred.index
    pred = pred.set_index("date")
    ax = dataset[validation_time:].plot(label="observed", figsize=(14, 7))
    pred.plot(ax=ax, label="Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Pollen / m3")
    plt.legend(["Actual Data", "Pollen Prediction"])

    # Save plot in png
    suffix = ".png"
    dirname = ""
    outfile_sarima_plot = "Sarima_visualisation"
    path = Path(dirname, outfile_sarima_plot).with_suffix(suffix)
    plt.savefig(path)
    # plt.show()


if __name__ == "__main__":
    typer.run(sarima_visualisation)
