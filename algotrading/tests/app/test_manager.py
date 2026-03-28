import pytest
import asyncio
import sys
import os
from unittest.mock import AsyncMock

# Add project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../algo-trading')))

from algotrading.app.main import ConnectionManager

@pytest.mark.asyncio
async def test_connection_manager_broadcast():
    manager = ConnectionManager()
    
    # Mock WebSocket
    mock_ws = AsyncMock()
    
    # Connect (mock accept)
    mock_ws.accept = AsyncMock()
    await manager.connect(mock_ws)
    assert len(manager.active_connections) == 1
    
    # Broadcast
    message = {"price": 100}
    await manager.broadcast(message)
    
    # Verify send_json was called with message
    mock_ws.send_json.assert_called_once_with(message)
    
    # Disconnect
    manager.disconnect(mock_ws)
    assert len(manager.active_connections) == 0
