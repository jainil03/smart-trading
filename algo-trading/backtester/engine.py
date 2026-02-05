import numpy as np
import pandas as pd

class BacktestEngine:

    def __init__(self, execution_engine, portfolio):
        self.execution = execution_engine
        self.portfolio = portfolio

    def run(self, data):
        data = data.copy()

        # Market returns
        data["returns"] = data["Close"].pct_change().fillna(0)

        # Position logic
        data["position"] = (
            data["signal"]
            .replace(0, pd.NA)
            .ffill()
            .shift(1)
            .fillna(0)
        )

        # Strategy returns (capital changes only when in position)
        data["strategy_returns"] = data["position"] * data["returns"]

        # Transaction costs (only when trade happens)
        trade = data["position"].diff().abs().fillna(0)
        data["strategy_returns"] -= trade * self.execution.cost

        # Equity curve
        data["equity"] = self.portfolio.compute_equity(
            data["strategy_returns"]
        )

        print(data.columns)

        return data
