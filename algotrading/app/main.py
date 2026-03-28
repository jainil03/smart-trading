from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio
import sys
import os
import logging
import yfinance as yf
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure the project root is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.connectors.binance_connector import BinanceConnector

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="algotrading/app/static"), name="static")

@app.get("/")
async def get_index():
    path = os.path.join(os.path.dirname(__file__), "static/index.html")
    # Force no-cache so browser always gets latest UI
    return FileResponse(path, headers={"Cache-Control": "no-store, no-cache, must-revalidate"})

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

manager = ConnectionManager()

@app.websocket("/ws/market-data/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await manager.connect(websocket)
    
    binance_symbol = symbol.upper()
    yf_symbol = symbol.upper().replace('USDT', '-USD')
    # if symbol.lower() == 'btcusdt':
    #     yf_symbol = 'BTC-USD'
    
    logger.info(f"New WebSocket connection for {symbol} (YF: {yf_symbol}, Binance: {binance_symbol})")
    
    connector = BinanceConnector(binance_symbol.lower())
    
    # 1. Fetch deep history with YFinance
    last_timestamp = 0
    try:
        # Fetching 1mo with 5m interval
        data = yf.Ticker(yf_symbol).history(period="1mo", interval="5m")
        
        if not data.empty:
            data = data.reset_index()
            # The column is 'Datetime' for intraday data
            date_col = 'Datetime' if 'Datetime' in data.columns else 'Date'
            
            # Ensure time is converted to epoch seconds correctly
            # Pandas Timestamps are already objects we can access
            data['time'] = data[date_col].apply(lambda x: int(x.timestamp()))
            
            historical_candles = [
                {
                    'time': int(row['time']),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close'])
                }
                for row in data.to_dict('records')
            ]
            
            if historical_candles:
                last_timestamp = historical_candles[-1]['time']
                await websocket.send_json({"type": "history", "data": historical_candles})
                logger.info(f"Sent {len(historical_candles)} candles for {yf_symbol}, last time: {last_timestamp}")
            else:
                logger.warning(f"Empty historical list for {yf_symbol}")
        else:
            logger.warning(f"No historical data returned for {yf_symbol}")
            
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
    
    # 2. Stream ticks, but ignore duplicates
    async def process_tick(data):
        nonlocal last_timestamp
        try:
            price = float(data.get('c'))
            timestamp = int(data.get('E')) / 1000
            
            # Stitching: Only send if tick is newer than history
            if timestamp > last_timestamp:
                message = {
                    "type": "tick",
                    "price": price,
                    "time": timestamp
                }
                await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error processing tick: {e}")

    
    stream_task = asyncio.create_task(connector.connect(process_tick))
    
    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        logger.error(f"WebSocket Error: {e}")
    finally:
        logger.info(f"Closing stream")
        stream_task.cancel()
        manager.disconnect(websocket)
