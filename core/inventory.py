"""Inventory management, primarily for TaxAware strategies."""


class Inventory:
    """Update tax-lots based on inventory protocol and new trades."""
    methods = ['FIFO', 'LIFO', 'MIN_TAX']
    def __init__(self, method):
        if method.upper() not in Inventory.methods:
            raise ValueError(f'method must be in {Inventory.methods}')
        self.method = method
        self.open_lots = []
        self.closed_lots = []

    def add_trades(self):
        # Add qp_builder logic here

    def get_open_lots(self):
        return open_lots
