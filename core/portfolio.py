"""Portfolio class with single holding per stock, and all transactions saved."""
import pandas as pd


class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.holdings = pd.Series(dtype=float)
        self.trades = pd.DataFrame()
        self.aum = cash

    def rebalance(self, target, context):
        """Update holdings with new target shares
        :param target: pd.Series -- target shares by asset
        :param context: dict - market data, asset definitions
        :return: None
        """
        date = context['market']['date']
        target = pd.Series(target)
        prices = pd.Series(context['market']['spot_prices']).reindex(target.index)
        # compute trades
        # return trade_summary object
        
    def reprice(self, context):
        """Reprice all assets, update cash with dividends, and return performance_summary object"""
        

