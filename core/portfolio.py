"""Portfolio class"""
import pandas as pd


class Portfolio:
    """Portfolio maintains its holdings by updating with current market,
    adds and removes holdings. Checks for rebalance are performed here as
    instructed by a strategy class instance, as is a new portfolio target.
    From the new target and current holdings, a trade list is generated (that
    may incorporate tax inventory management) and new holdings are generated.
    Methods for evaluating trading (turnover, cost per share, etc) are available here.
    """
    def __init__(self, initial_cash=0):
        self.cash = initial_cash
        self.holdings = []
        self.target = None
        self.trades = None

    def reprice(self, context):
        _ = [holding.reprice(context) for holding in self.holdings]
        
    @property
    def aum(self):
        if self.holdings:
            return self.cash + self.to_frame().value.sum()
        else:
            return self.cash

    def add_holding(self, holding):
        self.cash -= holding.quantity * holding.acquisition_price
        self.holdings.append(holding)

    def to_frame(self):
        """DataFrame representation of the holdings."""
        if self.holdings:
            frame = pd.concat([holding.to_series() for holding in self.holdings], axis=1).T
        else:
            frame = pd.DataFrame()
        return frame

    def to_string(self):
        strings = [f'cash: {self.cash}',
                   self.to_frame().to_string(),
                   ]
        return '\n'.join(strings)
