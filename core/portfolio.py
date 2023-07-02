"""Portfolio class with single holding per stock, and all transactions saved."""
import pandas as pd


class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.holdings = pd.Series(dtype=float)
        self.prices = pd.Series(dtype=float)
        self.trades = pd.DataFrame()

    def rebalance(self, target, context):
        """Update holdings with new target shares. Update cash with with trade value, where
        trades assumed executed at context market prices.
        :param target: pd.Series -- target shares by asset
        :param context: dict - market data, asset definitions
        :return: None
        """
        date = context['market']['date']
        prices = context['market']['prices']
        trade_shares = target.sub(self.holdings, fill_value=0)
        Portfolio.check_for_missing_prices(trade_shares, prices)
        self.prices = prices.reindex(trade_shares.index)
        self.trades = pd.DataFrame({'shares': trade_shares, 'price': self.prices})
        self.holdings = target
        self.cash -= self.trades.shares @ self.trades.price

    def reprice(self, context):
        """Reprice all assets, update cash with dividends.
        :param context: dict
        :return None
        """
        prices = context['market']['prices']
        Portfolio.check_for_missing_prices(self.holdings, prices)
        self.prices = prices.reindex(self.holdings.index)
        dividends = context['market']['dividends']
        dividend_value = dividends.mul(self.holdings, fill_value=0).sum()
        self.cash += dividend_value

    def to_string(self):
        return f'Portfolio(cash={self.cash}, aum={self.aum}):\nholdings={self.holdings}'

    @staticmethod
    def check_for_missing_prices(series, prices):
        prices = prices.reindex(series.index)
        missing = prices[prices.isna()].index.to_list()
        if len(missing) > 0:
            raise ValueError(f'Missing prices for {missing}')
        
    @property
    def aum(self):
        return self.cash + self.holdings @ self.prices
