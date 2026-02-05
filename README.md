# Smart Trading

A lightweight, modular toolkit for algorithmic trading: backtesting, strategy development, data ingestion, indicators, risk management, and optional live execution.

## Features
- Backtesting engine with performance metrics
- Strategy framework (signals, execution, and position sizing)
- Connectors for CSV / OHLCV APIs / websocket feeds
- Common technical indicators included
- Risk management modules (stop-loss, take-profit, max exposure)
- CI-friendly tests and examples

## Requirements
- Python 3.9+
- Recommended: virtualenv 

## Installation
Clone and install dependencies:
```bash
git clone <repo-url> smart-trading
cd smart-trading
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration
Create a `.env` or `config.yml` with keys (examples):
```env
DATA_API_KEY=your_data_api_key
BROKER_API_KEY=your_broker_api_key
DEFAULT_SYMBOL=XAUUSD
```

## Usage
Run backtest:
```bash
python -m smart_trading.backtest --strategy strategies/simple_mean_reversion --data data/sample.csv
```
Run a strategy in paper/live mode:
```bash
python -m smart_trading.runner --strategy strategies/my_strategy --mode paper
```

## Project Layout
- smart_trading/         — core library (engine, data, strategies, utils)
- strategies/            — example strategies
- data/                  — sample datasets
- tests/                 — unit and integration tests
- README.md


## Contributing
- Fork, create a feature branch, add tests, open a PR.
- Follow style: black + isort + flake8.
