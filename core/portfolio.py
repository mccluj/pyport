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
        self.holdings = pd.DataFrame(columns=['symbol', 'value'])
        self.target = None
        self.trades = None

    def reprice(self, market):
        self.holdings.apply(lambda x: x.reprice(market))
        
    @property
    def aum(self):
        return self.cash + self.holdings.value.sum()
