# Smart Trading

A real-time algorithmic trading platform with live market data streaming, backtesting engine, and interactive charting with drawing tools.

## Features

### Real-Time Data Streaming
- Live WebSocket connection to Binance exchange
- Historical data from Yahoo Finance for deep context
- Data stitching: seamless handover from historical to live data
- 10,000+ historical candles with pagination

### Interactive Charting
- Real-time candlestick chart (powered by TradingView `lightweight-charts`)
- Timeframe switching: 1m, 5m, 15m, 1h, 4h, 1d (client-side aggregation, no re-fetch)
- Phantom time axis: future time labels visible on x-axis
- Night mode toggle
- Custom candle colors (up/down)

### Drawing Tools
- **Trendline**: Draw lines anchored to price/time coordinates
- **Rectangle**: Filled zones for support/resistance
- **Fibonacci Retracement**: 7 levels (0%, 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%)
- **Long Position**: 1:3 Risk/Reward visualization with entry, stop-loss, take-profit
- **Short Position**: 1:3 Risk/Reward visualization with entry, stop-loss, take-profit
- **Selection**: Click any drawn tool to select it (cyan highlight)
- **Resize**: Drag handle dots to resize selected tools
- **Delete**: Click the red X button on selected tools to remove them

### Backtesting Engine
- Moving Average Crossover strategy
- Performance metrics: Sharpe Ratio, Max Drawdown, P&L
- Configurable via `config/params.yaml`

### Architecture
- **Backend**: FastAPI (Python) with WebSocket support
- **Frontend**: Vanilla JS with `lightweight-charts` and SVG overlay for drawing tools
- **Data Flow**: Binance WebSocket (live) + Yahoo Finance (history) via data stitching
- **Performance**: SVG overlay with `pointer-events: none` for zero-lag chart interactions

## Project Structure

```
smart-trading/
├── algotrading/
│   ├── app/
│   │   ├── main.py          # FastAPI server with WebSocket endpoints
│   │   └── static/
│   │       └── index.html   # Frontend chart + drawing tools
│   ├── src/
│   │   ├── connectors/      # Binance WebSocket connector
│   │   ├── engine/          # Backtest engine, portfolio, execution
│   │   ├── strategies/      # Moving average strategy
│   │   └── analytics/       # Metrics (Sharpe, drawdown)
│   ├── config/
│   │   └── params.yaml      # Configuration
│   ├── tests/               # Unit tests
│   └── main.py              # Backtest entry point
└── venv/
```

## Requirements

- Python 3.13+
- Virtual environment recommended

## Installation

```bash
git clone <repo-url> smart-trading
cd smart-trading
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn websockets yfinance ccxt pandas numpy pyyaml matplotlib
```

## Usage

### Backtesting
```bash
python algotrading/main.py --mode backtest
```

### Live Trading Dashboard
```bash
uvicorn algotrading.app.main:app --port 8001 --reload
```
Then open `http://127.0.0.1:8001` in your browser.

### Configuration
Edit `algotrading/config/params.yaml`:
```yaml
symbol: GC=F
capital: 100000
transaction_cost: 0.001
strategy:
  fast_window: 9
  slow_window: 15
live_symbol: btcusdt
```

## How Drawing Tools Work

1. **Click a tool button** (Trendline, Rectangle, Fibonacci, Long, Short)
2. **Click and drag** on the chart to draw
3. **Click on a drawn tool** to select it (turns cyan with handles)
4. **Drag the cyan dots** to resize
5. **Click the red X** to delete

All tools are anchored to price/time coordinates and move with chart zoom/scroll.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend Framework | FastAPI |
| Data Streaming | Binance WebSocket |
| Historical Data | Yahoo Finance (via yfinance) |
| Exchange API | CCXT |
| Charting | TradingView Lightweight Charts |
| Drawing Tools | SVG Overlay |
| Frontend | Vanilla JavaScript |
