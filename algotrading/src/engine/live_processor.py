import pandas as pd
from collections import deque

class LiveProcessor:
    def __init__(self, strategy, portfolio, window_size=100):
        self.strategy = strategy
        self.portfolio = portfolio
        self.window_size = window_size
        # Keep a rolling window of prices
        self.data_window = deque(maxlen=window_size)

    def process_tick(self, ticker_data):
        """
        Processes a single ticker tick, updates the window, 
        and generates a signal.
        """
        price = float(ticker_data.get('c'))
        timestamp = pd.to_datetime(ticker_data.get('E'), unit='ms')
        
        self.data_window.append({'Close': price, 'Timestamp': timestamp})
        
        # We need at least enough data to compute indicators
        if len(self.data_window) < self.strategy.slow:
            return None, None
            
        # Convert window to DataFrame for strategy
        df = pd.DataFrame(list(self.data_window))
        
        # Generate signals
        # Note: Strategy expects 'Close' column
        signals = self.strategy.generate_signals(df)
        
        latest_signal = signals['signal'].iloc[-1]
        
        return price, latest_signal
