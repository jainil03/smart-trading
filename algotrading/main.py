import sys; sys.path.insert(0, "/Users/jainilraval/smart-trading"); 
import yaml
import yfinance as yf
import pandas as pd
import argparse
import asyncio
import sys
import os
import logging

# Set up project root
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.strategies.moving_average import MovingAverageStrategy
from src.engine.execution import ExecutionEngine
from src.engine.portfolio import Portfolio
from src.engine.engine import BacktestEngine
from src.engine.live_processor import LiveProcessor
from src.analytics.metrics import sharpe_ratio, max_drawdown
from src.analytics.plots import plot
from src.connectors.binance_connector import BinanceConnector

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_backtest(config):
    # Download data
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
    plot(data, config["symbol"], config["interval"])

async def run_live(config):
    # This mode is now handled by the FastAPI app in app/main.py
    logger.info("Live mode is now served via FastAPI. Please start the app using 'uvicorn app.main:app'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart Trading System")
    parser.add_argument("--mode", choices=["backtest", "live"], default="backtest", help="Execution mode")
    args = parser.parse_args()

    with open("config/params.yaml") as f:
        config = yaml.safe_load(f)

    if args.mode == "backtest":
        run_backtest(config)
    else:
        asyncio.run(run_live(config))
