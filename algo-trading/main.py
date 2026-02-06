import yaml
import yfinance as yf
import mplfinance as mpf
import pandas as pd

from strategies.moving_average import MovingAverageStrategy
from backtester.execution import ExecutionEngine
from backtester.portfolio import Portfolio
from backtester.engine import BacktestEngine
from analytics.metrics import sharpe_ratio, max_drawdown
from analytics.plots import plot


with open("./algo-trading/config/params.yaml") as f:
    config = yaml.safe_load(f)


# Download data
# data = yf.download(
#     config["symbol"],
#     start=config["start_date"],
#     end=config["end_date"]
# )

data = yf.Ticker(config["symbol"]).history(period=config["period"], interval=config["interval"])

# Strategy
strategy = MovingAverageStrategy(
    config["strategy"]["fast_window"],
    config["strategy"]["slow_window"]
)

data = strategy.generate_signals(data)

# Backtest
execution = ExecutionEngine(config["transaction_cost"])
portfolio = Portfolio(config["capital"])
engine = BacktestEngine(execution, portfolio)

results = engine.run(data)

# Metrics
sr = sharpe_ratio(results["strategy_returns"])
dd = max_drawdown(results["equity"])
final_capital = results["equity"].iloc[-1]

initial_capital = config["capital"]
pnl = final_capital - initial_capital
pnl_pct = (pnl / initial_capital) * 100

print(f"Initial Capital: ₹{initial_capital:,.2f}")
print(f"Final Capital:   ₹{final_capital:,.2f}")
print(f"P&L:             ₹{pnl:,.2f} ({pnl_pct:.2f}%)")
print(f"Sharpe Ratio: {sr:.2f}")
print(f"Max Drawdown: {dd:.2%}")

# Plot
plot(data, results,True,False)
