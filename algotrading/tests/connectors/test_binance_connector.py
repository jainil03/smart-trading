import pytest
import asyncio
import json
import sys
import os
from unittest.mock import MagicMock, AsyncMock

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../algo-trading')))

from algotrading.src.connectors.binance_connector import BinanceConnector

@pytest.mark.asyncio
async def test_binance_connector_connect_calls_callback():
    # Mock data to simulate WebSocket message
    mock_data = {"s": "BTCUSDT", "c": "50000.00"}
    
    # Mock WebSocket implementation
    class MockWS:
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass
        async def recv(self):
            # simulate one receive then hang to test
            await asyncio.sleep(0.1)
            return json.dumps(mock_data)

    import websockets
    original_connect = websockets.connect
    websockets.connect = lambda *args, **kwargs: MockWS()
    
    try:
        connector = BinanceConnector("btcusdt")
        callback = AsyncMock()
        
        # Run the connection
        # We need to run it in a way that doesn't loop infinitely.
        # Modified the loop in connector to break or handle it differently?
        # For now, let's just let it run for one iteration and check callback
        
        # We can mock the while True loop in connector?
        # Alternatively, just use the task cancellation as before
        
        task = asyncio.create_task(connector.connect(callback))
        
        # Wait for the callback to be called at least once
        await asyncio.sleep(0.5)
        
        callback.assert_called_with(mock_data)
        
        # Cancel the task
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
            
    finally:
        # Restore original connect
        websockets.connect = original_connect

