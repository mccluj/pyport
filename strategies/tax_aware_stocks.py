"""TaxAwareStocks -- rebalance strategy that combines tax-efficiency with optimal risk
adjusted return.
"""
from pyport import Strategy


class TaxAwareStocks(Strategy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
