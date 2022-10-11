#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 14:35:30 2022

@author: sandro
"""
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import typer
from numpy import loadtxt


def lstm_visualisation(
    filepath: str = typer.Option(
        ..., help="File path of the complete dataset csv file"
    ),
    filepath_prediction: str = typer.Option(
        ..., help="File path of the prediction csv file"
    ),
    delimiter: str = typer.Option(
        ..., help="Delimiter of the input file and output file. Must be the same"
    ),
    start_date: str = typer.Option(
        "2015-01-01", help="start date to visualise the plot"
    ),
    n_steps_out: int = typer.Option(..., help="Number of steps we want to predict"),
):
    """
    Given the complete dataset, the prediction array, pollen type and the start date

    Returns the R2 visualisation
    """
    os.chdir("data")

    # Load predictions array from CSV
    prediction = loadtxt(filepath_prediction, delimiter=delimiter)
    pred = pd.DataFrame()
    pred["pred"] = prediction

    # Load the complete dataset from CSV
    dataset = pd.read_csv(filepath, sep=delimiter, index_col="date")
    dataset.index = pd.to_datetime(dataset.index)
    dates = dataset.index[-n_steps_out:]

    pred["date"] = dates
    pred = pred.set_index("date")

    ax = dataset[start_date:]["pollen"].plot(label="observed", figsize=(14, 7))
    pred.plot(ax=ax, label="Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Pollen / m3")
    plt.legend(["Actual Data", "Pollen Prediction"])

    # Save plot in png
    suffix = ".png"
    dirname = ""
    path = Path(dirname, "lstm_visualisation").with_suffix(suffix)
    plt.savefig(path)
    # plt.show()


# ============ MAIN ============
if __name__ == "__main__":
    typer.run(lstm_visualisation)
