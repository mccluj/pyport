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
        self.holdings = pd.DataFrame()
        self.target = None
        self.trades = None

    def reprice(self, market):
        if self.holdings is not None:
            self.holdings.apply(lambda x: x.reprice(market))
        
    @property
    def aum(self):
        if self.holdings.empty:
            return self.cash
        else:
            return self.cash + self.holdings.value.sum()

    def add_holding(self, holding):
        self.cash -= holding.quantity * holding.acquisition_price
        holding_series = holding.to_series()
        if self.holdings.empty:
            self.holdings = holding_series.to_frame().T
        else:
            self.holdings = pd.concat([self.holdings, holding_series], axis=0)

    def to_string(self):
        strings = [f'cash: {self.cash}',
                   self.holdings.to_string(),
                   ]
        return '\n'.join(strings)
