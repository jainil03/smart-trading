class Portfolio:

    def __init__(self, capital):
        self.initial_capital = capital

    def compute_equity(self, returns):
        equity_curve = (1 + returns).cumprod() * self.initial_capital
        
        return equity_curve
