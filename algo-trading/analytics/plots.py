import matplotlib.pyplot as plt

def plot_equity_curve(data,results):
    fig, (ax1, ax2, ax3) = plt.subplots(
        3, 1,
        figsize=(14, 10),
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1, 2]}
    )

    # ======================
    # 1️⃣ PRICE + MOVING AVERAGES
    # ======================
    ax1.plot(data.index, data["Close"], label="Close Price", alpha=0.6)
    ax1.plot(data.index, data["ma_fast"], label="Fast MA (20)", linewidth=2)
    ax1.plot(data.index, data["ma_slow"], label="Slow MA (50)", linewidth=2)

    ax1.set_title("Price & Moving Averages")
    ax1.set_ylabel("Price")
    ax1.legend()
    ax1.grid(True)

    # ======================
    # 2️⃣ SIGNAL
    # ======================
    ax2.step(
        data.index,
        data["signal"],
        where="post",
        color="purple",
        linewidth=2
    )

    ax2.set_yticks([-1, 0, 1])
    ax2.set_yticklabels(["SELL", "HOLD", "BUY"])
    ax2.set_title("Trading Signal")
    ax2.set_ylabel("Signal")
    ax2.grid(True)

    # ======================
    # 3️⃣ EQUITY CURVE
    # ======================
    ax3.plot(
        results.index,
        results["equity"],
        label="Equity Curve",
        color="green",
        linewidth=2
    )

    ax3.set_title("Portfolio Equity")
    ax3.set_ylabel("Capital")
    ax3.set_xlabel("Date")
    ax3.legend()
    ax3.grid(True)

    plt.tight_layout()
    plt.show()
    
