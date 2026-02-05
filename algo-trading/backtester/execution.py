class ExecutionEngine:

    def __init__(self, transaction_cost):
        self.cost = transaction_cost

    def apply_costs(self, returns):
        return returns - self.cost
