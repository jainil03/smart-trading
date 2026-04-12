import json
import asyncio
import websockets
import ccxt.async_support as ccxt
from src.connectors.base_connector import BaseConnector

class BinanceConnector(BaseConnector):

    """
    Implementation of the BaseConnector for Binance (Spot) using CCXT.
    """

    def __init__(self, symbol: str):
        self.symbol = symbol.lower()
        self.ws_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@ticker"
        self.exchange = ccxt.binance()

    async def fetch_historical_candles(self, timeframe='1m', limit=10000):
        """Fetch historical candles using CCXT with pagination."""
        all_candles = []
        # Binance OHLCV limit per request is 1000
        batch_limit = 1000
        since = None
        
        while len(all_candles) < limit:
            remaining = limit - len(all_candles)
            fetch_limit = min(remaining, batch_limit)
            
            # fetch_ohlcv returns candles in ascending order of time
            candles = await self.exchange.fetch_ohlcv(
                self.symbol.upper(), 
                timeframe, 
                since=since, 
                limit=fetch_limit
            )
            
            if not candles:
                break
            
            all_candles.extend(candles)
            # Update 'since' to the time of the last candle + 1 timeframe unit
            since = candles[-1][0] + 1
            
            # If we received fewer candles than requested, we reached the end
            if len(candles) < fetch_limit:
                break
                
        await self.exchange.close()
        
        # Convert to list of dicts for frontend compatibility
        return [
            {'time': c[0] // 1000, 'open': c[1], 'high': c[2], 'low': c[3], 'close': c[4]}
            for c in all_candles
        ]

    async def connect(self, callback):
        while True:
            try:
                async with websockets.connect(self.ws_url) as ws:
                    while True:
                        try:
                            data = await ws.recv()
                            ticker_data = json.loads(data)
                            await callback(ticker_data)
                        except websockets.exceptions.ConnectionClosedOK:
                            return  # Exit on close
                        except asyncio.CancelledError:
                            return  # Exit on cancel
                        except Exception:
                            return  # Exit on error
            except Exception:
                return  # Don't reconnect on error, just exit
