import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd



def plot(data, results, show_price=True, show_equity=True):
    if show_price:
        plot_price_with_signals(data)
    if show_equity:
        plot_equity_curve(results)


def plot_price_with_signals(data, title="Price with Buy/Sell Signals"):
    # --- Clean data ---
    if isinstance(data.columns, pd.MultiIndex):
        data = data.copy()
        data.columns = data.columns.droplevel(1)

    ohlc_cols = ["Open", "High", "Low", "Close", "Volume"]
    data = data.dropna(subset=ohlc_cols)
    data[ohlc_cols] = data[ohlc_cols].astype(float)
    data.index = pd.to_datetime(data.index).tz_localize(None)

    # --- Moving averages ---
    apds = [
        mpf.make_addplot(data["ma_fast"], color="black", width=1),
        mpf.make_addplot(data["ma_slow"], color="blue", width=1),
    ]

    # --- BUY signals ---
    buy_prices = np.where(data["signal"] == 1, data["Low"] * 0.998, np.nan)
    apds.append(
        mpf.make_addplot(
            buy_prices,
            type="scatter",
            marker="$B$",
            markersize=40,
            color="green"
        )
    )

    # --- SELL signals ---
    sell_prices = np.where(data["signal"] == -1, data["High"] * 1.002, np.nan)
    apds.append(
        mpf.make_addplot(
            sell_prices,
            type="scatter",
            marker="$S$",
            markersize=40,
            color="red"
        )
    )

    mpf.plot(
        data,
        type="candle",
        addplot=apds,
        volume=False,
        style="yahoo",
        show_nontrading=False,
        figsize=(14, 7),
        title=title
    )


def plot_equity_curve(results):
    plt.figure(figsize=(14, 4))
    plt.plot(results.index, results["equity"], color="green", linewidth=2)
    plt.title("Portfolio Equity Curve")
    plt.ylabel("Capital")
    plt.xlabel("Date")
    plt.grid(True)
    plt.show()
