"""Portfolio class with single position per stock, and all transactions saved."""
import pandas as pd


class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.positions = pd.Series(dtype=float)
        self.prices = pd.Series(dtype=float)
        self.trades = pd.DataFrame()

    def rebalance(self, target, context):
        """Update positions with new target shares. Update cash with with trade value, where
        trades assumed executed at context market prices.
        :param target: pd.Series -- target shares by asset
        :param context: dict - market data, asset definitions
        :return: None
        """
        date = context['market']['date']
        prices = context['market']['prices']
        trade_shares = target.sub(self.positions, fill_value=0)
        Portfolio.check_for_missing_prices(trade_shares, prices)
        self.prices = prices.reindex(trade_shares.index)
        self.trades = pd.DataFrame({'shares': trade_shares, 'price': self.prices})
        self.positions = target
        self.cash -= self.trades.shares @ self.trades.price

    def apply_dividends(self, dividends):
        """Update internal cash with dividends paid on asset positions.
        :param dividends: pd.Series
        """
        dividend_value = dividends.mul(self.positions, fill_value=0).sum()
        self.cash += dividend_value

    def reprice(self, context):
        """Reprice all assets.
        :param context: dict
        :return None
        """
        prices = context['market']['prices']
        Portfolio.check_for_missing_prices(self.positions, prices)
        self.prices = prices

    def to_string(self):
        return f'Portfolio(cash={self.cash}, aum={self.aum}):\npositions={self.positions}'

    @staticmethod
    def check_for_missing_prices(series, prices):
        prices = prices.reindex(series.index)
        missing = prices[prices.isna()].index.to_list()
        if len(missing) > 0:
            raise ValueError(f'Missing prices for {missing}')
        
    @property
    def aum(self):
        return self.cash + self.positions @ self.prices
