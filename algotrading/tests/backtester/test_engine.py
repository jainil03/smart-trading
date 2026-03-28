import sys
import os
import pandas as pd
import pytest

# Add the project root to sys.path
sys.path.pop(0)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../algo-trading')))

from backtester.engine import BacktestEngine

# Mock classes for testing
class MockExecution:
    def __init__(self, cost):
        self.cost = cost

class MockPortfolio:
    def compute_equity(self, returns):
        return (1 + returns).cumprod()

def test_backtest_engine_missing_signal_column():
    engine = BacktestEngine(MockExecution(0.001), MockPortfolio())
    data = pd.DataFrame({"Close": [100, 101, 102]})
    
    with pytest.raises(KeyError, match="Data must contain a 'signal' column"):
        engine.run(data)
