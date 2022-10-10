#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 15:47:03 2022
@author: sandro
"""

import os
from itertools import product
from pathlib import Path

import joblib
import pandas as pd
import statsmodels.api as sm
import typer
from numpy import savetxt


def parameter_configuration():
    ps = [0, 1, 2]
    d = [0, 1]
    qs = [0, 1, 2, 3]
    Ps = [0, 1, 2]
    D = [0, 1]
    Qs = [0, 1, 2, 3]

    parameters = product(ps, d, qs, Ps, D, Qs)
    parameters_list = list(parameters)
    len(parameters_list)
    return parameters_list


def optimizeSARIMA(df, parameters_list, s):
    """Return dataframe with parameters and corresponding AIC

    parameters_list - list with (p, q, P, Q) tuples
    d - integration order in ARIMA model
    D - seasonal integration order
    s - length of season
    """

    results = []
    best_aic = float("inf")

    for param in parameters_list:
        # we need try-except because on some combinations model fails to converge
        try:
            model = sm.tsa.statespace.SARIMAX(
                endog=df["pollen"],
                exog=df.drop(["pollen"], axis=1),
                order=(param[0], param[1], param[2]),
                seasonal_order=(param[3], param[4], param[5], s),
                enforce_stationarity=False,
                enforce_invertibility=False,
            ).fit(disp=False)
        except:
            continue
        aic = model.aic
        # saving best model, AIC and parameters
        if aic < best_aic:
            best_model = model
            best_aic = aic
            best_param = param
        results.append([best_param, best_model.aic])

    result_table = pd.DataFrame(results)
    result_table.columns = ["parameters", "aic"]
    # sorting in ascending order, the lower AIC is - the better
    result_table = result_table.sort_values(by="aic", ascending=True).reset_index(
        drop=True
    )

    return result_table


def sarima_model(
    filepath: str = typer.Option(..., help="File path of the pollen csv file"),
    delimiter: str = typer.Option(
        ..., help="Delimiter of the input file and output file. Must be the same"
    ),
    seasonality: int = typer.Option(..., help="Indicate seasonality"),
):

    """
    Train SARIMA model with a specific scaled dataset
    Return a trained SARIMA model and X_test, y_test for evaluation metrics
    """
    os.chdir("data")

    # Read dataframe
    dataframe = pd.read_csv(filepath, sep=delimiter)
    dataframe["date"] = pd.to_datetime(dataframe["date"])
    dataframe = dataframe.set_index("date")

    # Split dataframe in features/target
    Y = dataframe[["pollen"]]
    X = dataframe.drop(["pollen"], axis=1)

    # Set configuration parameters for SARIMA hyperparameter optimization
    # parameters_list = parameter_configuration()
    # result_table = optimizeSARIMA(dataframe, parameters_list, seasonality, pollen)

    # set the best parameters that give the lowest AIC
    # p,d, q, P, D, Q = result_table.parameters[0]
    p, d, q, P, D, Q = 1, 0, 0, 0, 1, 0

    # With the best parameters we will train de the best model
    best_model = sm.tsa.statespace.SARIMAX(
        endog=Y,
        exog=X,
        order=(p, d, q),
        seasonal_order=(P, D, Q, seasonality),
        enforce_stationarity=False,
        enforce_invertibility=False,
    ).fit(disp=False)
    # Outfile
    dirname = ""
    filename = "Sarima_model"
    suffix = ".pkl"
    path = Path(dirname, filename).with_suffix(suffix)

    ### Save Model ###
    joblib.dump(best_model, path)

    # Save numpy array as CSV
    dirname = ""
    filename = "Sarima" + "_X_test"
    filename_target = "Sarima" + "_Y_test"
    suffix = ".csv"
    path_x_test = Path(dirname, filename).with_suffix(suffix)
    path_y_test = Path(dirname, filename_target).with_suffix(suffix)

    X.to_csv(path_x_test, sep=delimiter)
    Y.to_csv(path_y_test, sep=delimiter)


# ============ MAIN ============
if __name__ == "__main__":
    typer.run(sarima_model)
