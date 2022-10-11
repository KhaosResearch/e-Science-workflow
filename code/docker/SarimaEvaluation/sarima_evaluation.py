import math
import os
from pathlib import Path

import joblib
import pandas as pd
import typer
from numpy import ndarray, savetxt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def compute_metrics(test: ndarray, pred: ndarray) -> dict:
    """
    Provided the forecasted and test data, computes several metrics.

    Returns a dictionary of metrics
    """
    mae_lstm = mean_absolute_error(test, pred)
    rmse_lstm = math.sqrt(mean_squared_error(test, pred))
    r2_lstm = r2_score(test, pred)

    return {"MAE": mae_lstm, "RMSE": rmse_lstm, "R2 Score": r2_lstm}


def sarima_evaluation(
    filepath_X: str = typer.Option(..., help="File path of X_test csv file"),
    filepath_Y: str = typer.Option(..., help="File path of Y_test csv file"),
    filepath_model: str = typer.Option(..., help="File path of the model"),
    delimiter: str = typer.Option(
        ..., help="Delimiter of the input file and output file. Must be the same"
    ),
    validation_time: str = typer.Option(
        ..., help="Indicate from which period of time you want to make the validation"
    ),
):
    """
    Given X_test, y_test and the trained model, make predictions and evaluate the model

    Returns the model' metrics and predictions
    """
    os.chdir("data")

    # Read X,Y
    X = pd.read_csv(filepath_X, sep=delimiter)
    X["date"] = pd.to_datetime(X["date"])
    X = X.set_index("date")

    y = pd.read_csv(filepath_Y, sep=delimiter)
    y["date"] = pd.to_datetime(y["date"])
    y = y.set_index("date")

    load_model = joblib.load(filepath_model)

    # prediction = load_model.get_prediction(start=-15, dynamic=False)
    prediction = load_model.get_prediction(
        start=pd.to_datetime(validation_time), dynamic=False
    )

    prediction = prediction.predicted_mean

    # forecast = load_model.get_forecast(steps=90)

    mask = y.index >= validation_time
    y_pred = y.loc[mask]
    # y_pred = y.iloc[-15:]

    # metrics = compute_metrics(dataframe_pred["pollen"].values, prediction)
    metrics = compute_metrics(y_pred["pollen"], prediction)

    # Save metrics and predictions
    suffix = ".csv"
    dirname = ""
    outfile_metrics = "Sarima_metrics"
    # Save metrics in dataframe CSV
    df_metrics = pd.DataFrame.from_dict(metrics, orient="index", columns=["Value"])
    path = Path(dirname, outfile_metrics).with_suffix(suffix)
    df_metrics.to_csv(path, sep=delimiter)

    # Save predictions numpy array as CSV
    outfile_name_prediction = "Sarima_predictions"
    path_predictions = Path(dirname, outfile_name_prediction).with_suffix(suffix)
    savetxt(path_predictions, prediction, delimiter=delimiter)


# ============ MAIN ============
if __name__ == "__main__":
    typer.run(sarima_evaluation)
