import pandas as pd
from strategies.base_strategy import BaseStrategy

class MovingAverageStrategy(BaseStrategy):

    def __init__(self, fast_window, slow_window):
        self.fast = fast_window
        self.slow = slow_window

    def generate_signals(self, data):
        data = data.copy()

        data["ma_fast"] = data["Close"].rolling(self.fast).mean()
        data["ma_slow"] = data["Close"].rolling(self.slow).mean()

        data["signal"] = 0
        data.loc[data["ma_fast"] > data["ma_slow"], "signal"] = 1
        data.loc[data["ma_fast"] < data["ma_slow"], "signal"] = -1

        return data
