# common python libs
import datetime
import itertools
import os
import warnings
from time import time

import matplotlib
import matplotlib.dates as mdates
# matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import pyplot

plt.style.use("fivethirtyeight")
# statsmodels
import statsmodels.api as sm
import statsmodels.api as sma
# Typer
import typer
from pylab import rcParams
from scipy.signal import find_peaks
# scikit learn
from sklearn.metrics import mean_squared_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller

warnings.filterwarnings("ignore")


def test_stationarity(timeseries):
    # Determine rolling statistics
    rolmean = timeseries.rolling(window=12, center=True).mean()
    rolstd = timeseries.rolling(window=12, center=True).std()
    # rolling statistics plot
    pyplot.figure(figsize=(40, 20))
    ax = plt.gca()
    # ### formatter of the date
    ax.xaxis.set_major_locator(mdates.YearLocator())
    plt.xlabel("Date", fontsize=20)
    plt.ylabel("Count", labelpad=5, fontsize=20)
    orig = plt.plot(timeseries, color="black", label="Time Series")
    mean = plt.plot(rolmean, color="red", label="Mean rolling")
    std = plt.plot(rolstd, color="blue", label="Std. rolling")
    plt.legend(loc="best", prop={"size": 15})
    plt.title("Time series with rolling mean and std")
    ax.patch.set_alpha(0.0)
    plt.title("Time series with rolling mean and std")
    plt.savefig("DickeyFuller_plot.png")

    # Dicket-Fuller test
    test_dataframe = pd.DataFrame()
    dftest = adfuller(timeseries.values, autolag="AIC")
    tstat = dftest[0]
    pvalue = dftest[1]
    cvalues = dftest[4]
    print(cvalues)
    print("Dickey-Fuller Results")
    print("------------------")
    print("Test statistic\t", tstat)
    print("p-value\t\t\t", pvalue)
    print("------------------")
    print("Critical values (The test statistic should be lower)")
    test_dataframe.loc["Test statistic", "value"] = tstat
    test_dataframe.loc["p-value", "value"] = pvalue

    for clevel in [10, 5, 1]:
        conf = 100 - clevel
        cval = cvalues["%i%%" % clevel]
        if tstat < cval:
            comp = ">"
            verdict = "Pass"
        else:
            comp = "<"
            verdict = "Fails"

        test_dataframe.loc["Confidence " + str(conf) + " %", "value"] = (
            str(cval) + " " + str(comp) + " " + str(tstat) + " ... " + str(verdict)
        )
        print("Confidence %i%%\t\t%f %s %f ... %s" % (conf, cval, comp, tstat, verdict))

    return test_dataframe


def decompose(data, year, dfuller):
    rcParams["figure.figsize"] = 18, 8
    pyplot.figure(figsize=(150, 120))
    data.index = pd.DatetimeIndex(data.index)
    decomposition = sm.tsa.seasonal_decompose(data, model="additive")
    fig = decomposition.plot()
    fig.set_size_inches((16, 9))
    # Tight layout to realign things
    fig.tight_layout()
    plt.savefig("decompose.pdf")

    dates = pd.Series(
        pd.to_datetime(decomposition.seasonal.index), index=decomposition.seasonal.index
    )
    dates_filter = dates[dates.dt.year == int(year)]
    seasonal_dataframe = pd.DataFrame(decomposition.seasonal.loc[dates_filter])
    seasonal_dataframe.seasonal = seasonal_dataframe.seasonal.astype(int)
    picks = find_peaks(seasonal_dataframe.seasonal)

    end_df = dfuller
    if len(picks[0]) == 1:
        end_df.loc["Seasonal", "value"] = True
    else:
        end_df.loc["Seasonal", "value"] = False

    end_df.to_csv("DickerFuller_seasonality.csv", sep=";")


def arimax(data):
    p = q = range(0, 3)
    d = range(0, 1)
    P = Q = range(0, 3)
    D = range(0, 1)

    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(P, D, Q))]
    warnings.filterwarnings("ignore")
    min_aic = 9999999
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sma.tsa.statespace.SARIMAX(
                    data,
                    order=param,
                    seasonal_order=param_seasonal,
                    enforce_stationarity=False,
                    enforce_invertibility=False,
                )
                results = mod.fit(disp=False)
                if results.aic < min_aic:
                    min_aic = results.aic
                    parameter = param
                    parameter_seasonal = param_seasonal

            except:
                continue

    mod = sma.tsa.statespace.SARIMAX(
        data,
        order=parameter,
        seasonal_order=parameter_seasonal,
        enforce_stationarity=True,
        enforce_invertibility=False,
    )
    results = mod.fit(disp=False)
    results.plot_diagnostics(figsize=(16, 8))
    plt.savefig("SARIMAX_plots.pdf")


def arima(
    filepath: str = typer.Option(..., help="File path of the csv file"),
    delimiter: str = typer.Option(..., help="Delimiter of the csv file"),
    date_column: str = typer.Option(..., help="Name of the Date column"),
    pollen: str = typer.Option(..., help="Name of the Pollen column"),
    year: int = typer.Option(..., help="Year for decomposition"),
):
    os.chdir("data")
    dataframe = pd.read_csv(filepath, sep=delimiter)

    df = pd.DataFrame()
    df[date_column] = dataframe[date_column]
    df[pollen] = dataframe[pollen]
    df[date_column] = pd.to_datetime(df[date_column]).dt.strftime("%m-%Y")

    dates = df[date_column].unique()
    data = pd.DataFrame()
    data[date_column] = dates
    data = data.set_index(date_column)

    for date in dates:
        data.loc[date, pollen] = df.loc[df[date_column] == date, pollen].sum()

    dfuller = test_stationarity(data[pollen])

    # Decompose
    decompose(data, year, dfuller)

    # SARIMAX
    arimax(data)


if __name__ == "__main__":
    typer.run(arima)
