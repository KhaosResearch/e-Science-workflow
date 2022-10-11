import os
from pathlib import Path
from typing import Tuple

import keras
import keras.metrics as metric
import typer
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from keras.layers import (LSTM, Conv1D, Dense, Flatten, MaxPooling1D,
                          RepeatVector, TimeDistributed)
from keras.models import Sequential
from numpy import load, loadtxt, ndarray, save


def split_train_test(
    X: ndarray, y: ndarray, n_steps_out
) -> Tuple[ndarray, ndarray, ndarray, ndarray]:

    X_train = X[:-n_steps_out, :, :]
    y_train = y[:-n_steps_out, :]
    X_test = X[-n_steps_out:, :, :]
    y_test = y[-n_steps_out:, :]

    return X_train, y_train, X_test, y_test


def train_model(
    X_train: ndarray,
    y_train: ndarray,
    X_test: ndarray,
    y_test: ndarray,
    model: Sequential,
    saved_model: str,
) -> Sequential:

    checkpointer = ModelCheckpoint(filepath=saved_model, verbose=1, save_best_only=True)

    early_stop = keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=20, restore_best_weights=True
    )
    sch = ReduceLROnPlateau(
        monitor="val_loss", factor=0.01, patience=5, min_lr=1e-8, verbose=1
    )

    model.fit(
        X_train,
        y_train,
        epochs=1000,
        validation_data=(X_test, y_test),
        callbacks=[checkpointer, sch, early_stop],
    )

    return model


def lstm_build_model(
    filepath_X: str = typer.Option(..., help="File path of X csv file"),
    filepath_Y: str = typer.Option(..., help="File path of Y csv file"),
    n_neurons: int = typer.Option(
        200, help="Select number of neurons for model building"
    ),
    n_steps_in: int = typer.Option(..., help="Select time window to train the model"),
    n_steps_out: int = typer.Option(..., help="Select period of time to predict"),
    delimiter: str = typer.Option(
        ..., help="Delimiter of the input file and output file. Must be the same"
    ),
):
    """
    Given some parameters, builds a ConvLSTM model for timeseries analysis.

    Returns the built Keras model and X_test, y_test to make predictions
    """
    os.chdir("data")

    # Load array
    X = load(filepath_X)
    y = loadtxt(filepath_Y, delimiter=delimiter)

    # Split train and test
    X_train, y_train, X_test, y_test = split_train_test(X, y, n_steps_out)

    # extract the number of features
    n_features = X_train.shape[2]

    # Build LSTM MODEL
    model = Sequential()
    model.add(
        Conv1D(
            filters=64,
            kernel_size=3,
            activation="relu",
            input_shape=(n_steps_in, n_features),
        )
    )
    model.add(Conv1D(filters=64, kernel_size=3, activation="relu"))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())

    model.add(RepeatVector(n_steps_out))
    model.add(LSTM(n_neurons, activation="relu", return_sequences=True))
    model.add(TimeDistributed(Dense(n_neurons, activation="relu")))
    model.add(TimeDistributed(Dense(1)))

    model.compile(loss="mse", optimizer="adam", metrics=[metric.RootMeanSquaredError()])
    model.summary()

    # Train and Save the model
    dirname = ""
    saved_model = dirname + "lstm_model.h5"
    train_model(X_train, y_train, X_test, y_test, model, saved_model)

    # Save numpy array
    dirname = ""
    filename = "lstm" + "_X_test"
    filename_target = "lstm" + "_Y_test"
    path_x_test = Path(dirname, filename)
    path_y_test = Path(dirname, filename_target)

    save(path_x_test, X_test)
    save(path_y_test, y_test)


# ============ MAIN ============
if __name__ == "__main__":
    typer.run(lstm_build_model)
