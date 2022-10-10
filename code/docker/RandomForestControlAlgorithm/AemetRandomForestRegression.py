import math
import os
from pathlib import Path

import pandas as pd
import typer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit


# ========== METHODS ==========
def aemet_linear_regression(
    filepath: str = typer.Option(..., help="Path of csv file"),
    delimiter: str = typer.Option(..., help="Delimiter of the csv file"),
    date_column: str = typer.Option(..., help="Name of the date column"),
    dependent_variable: str = typer.Option(..., help="Name of the Pollen column"),
):
    os.chdir("data")

    df = pd.read_csv(filepath, sep=delimiter)
    df = df.set_index(date_column)
    df = df.dropna(axis=0, how="any")
    X = df.drop(dependent_variable, axis=1).to_numpy()
    y = df[dependent_variable].to_numpy()

    metrics = pd.DataFrame()
    final_df = pd.DataFrame()
    tscv = TimeSeriesSplit()
    for train_index, test_index in tscv.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        reg = RandomForestRegressor().fit(X_train, y_train)
        y_predict = reg.predict(X_test)
        r2 = r2_score(y_test, y_predict)
        mae = mean_absolute_error(y_test, y_predict)
        rmse = math.sqrt(mean_squared_error(y_test, y_predict))
        if mae != 0:
            rmse_mae = rmse / mae
        else:
            rmse_mae = rmse
        dict = {"r2": r2, "mae": mae, "rmse": rmse, "rmse_mae": rmse_mae}
        metrics = metrics.append(dict, ignore_index=True)
    final_dict = {
        "filename": Path(filepath).stem,
        "r2_mean": metrics["r2"].mean(),
        "mae_mean": metrics["mae"].mean(),
        "rmse_mean": metrics["rmse"].mean(),
        "rmse_mae_mean": metrics["rmse_mae"].mean(),
    }
    final_df = final_df.append(final_dict, ignore_index=True)

    dirname = ""
    filename = Path(filepath).stem + "_metrics"
    extension = ".csv"

    path = Path(dirname, filename).with_suffix(extension)
    final_df.to_csv(path, sep=delimiter, index=None)


# ========== MAIN ==========
if __name__ == "__main__":
    typer.run(aemet_linear_regression)
