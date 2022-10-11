import math
import os
from pathlib import Path

import keras
import pandas as pd
import typer
from numpy import load, ndarray, savetxt
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


def lstm_evaluation(
    filepath_X: str = typer.Option(..., help="File path of X_test csv file"),
    filepath_Y: str = typer.Option(..., help="File path of Y_test csv file"),
    filepath_model: str = typer.Option(..., help="File path of the model"),
    filepath_scaler_y: str = typer.Option(
        ..., help="File path of the Scaler target object used for data normalization"
    ),
    delimiter: str = typer.Option(
        ..., help="Delimiter of the input file and output file. Must be the same"
    ),
):
    """
    Given X_test, y_test and the trained model, make predictions and evaluate the model

    Returns the model' metrics and predictions
    """
    os.chdir("data")

    # Load X_test and y_test array from CSV
    X_test = load(filepath_X)
    y_test = load(filepath_Y)

    # Load Best model
    best_model = keras.models.load_model(filepath_model)

    # load the scaler .pkl
    scaler_target = load(open(filepath_scaler_y, "rb"), allow_pickle=True)

    # MAKE PREDICTIONS
    y_hat = best_model.predict(X_test)
    test = pd.DataFrame(y_test[:, -1]).values
    pred = pd.DataFrame(y_hat[:, -1, 0]).values

    test_inv = scaler_target.inverse_transform(test)
    # test_inv = np.squeeze(test_inv)

    pred_inv = scaler_target.inverse_transform(pred)
    # pred_inv = np.squeeze(pred_inv)

    # CALCULATE METRICS
    metrics = compute_metrics(test_inv, pred_inv)

    # Save metrics and predictions
    suffix = ".csv"
    dirname = ""

    # Save metrics in dataframe CSV
    df_metrics = pd.DataFrame.from_dict(metrics, orient="index", columns=["Value"])
    path = Path(dirname, "lstm_metrics").with_suffix(suffix)
    df_metrics.to_csv(path, sep=delimiter)

    # Save predictions numpy array as CSV
    dirname = ""
    suffix = ".csv"
    path_predictions = Path(dirname, "lstm_predictions").with_suffix(suffix)
    savetxt(path_predictions, pred_inv, delimiter=delimiter)


# ============ MAIN ============
if __name__ == "__main__":
    typer.run(lstm_evaluation)
