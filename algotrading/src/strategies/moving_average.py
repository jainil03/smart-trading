import pandas as pd
from algotrading.src.strategies.base_strategy import BaseStrategy

class MovingAverageStrategy(BaseStrategy):

    def __init__(self, fast_window, slow_window):
        self.fast = fast_window
        self.slow = slow_window

    def generate_signals(self, data):
        data = data.copy()

        data["ma_fast"] = data["Close"].ewm(span=self.fast, adjust=False).mean()
        data["ma_slow"] = data["Close"].ewm(span=self.slow, adjust=False).mean()
        
        data["signal"] = 0

        # only signal on actual crossover
        buy_cross = (data["ma_fast"] > data["ma_slow"]) & (data["ma_fast"].shift(1) <= data["ma_slow"].shift(1))
        sell_cross = (data["ma_fast"] < data["ma_slow"]) & (data["ma_fast"].shift(1) >= data["ma_slow"].shift(1))
        
        data.loc[buy_cross, "signal"] = 1
        data.loc[sell_cross, "signal"] = -1

        return data
