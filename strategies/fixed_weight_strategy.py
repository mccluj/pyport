"""
FixedWeightStrategy class. Rebalance to fixed weight portfolio at regular intervals.
"""
import pandas as pd


class FixedWeightStrategy:
    def __init__(self, weights: pd.Series, frequency: float, maximum_deviation: float):
        """
        :param weights: pd.Series -- target portfolio weights
        :param frequency: str or float -- pandas.tseries.offsets(str) or years(float)
        :param maximum_deviation: float -- maximum cumulative portfolio percent deviation from target
        """
        self.weights = weights
        self.frequency = frequency
        self.maximum_deviation = maximum_deviation

    def test_for_rebalance(self, portfolio, context):
        """Test for deviation from target weights."""
        actual = portfolio.holding_weights()
        index = set(self.weights.index).union(actual.index)
        target = self.weights.reindex(index).fillna(0)
        actual = actual.reindex(index).fillna(0)
        deviation = actual.sub(target).abs().sum()
        return deviation > self.maximum_deviation

    def generate_portfolio_holdings(self, context):
        portfolio = context['portfolio']
        assets = context['assets']
        symbols = assets.keys()
        market = context['market']
        aum = portfolio.aum
        prices = market['spot_prices'].reindex(symbols)
        weights = self.weights.reindex(symbols)
        target_values = aum * weights
        target_shares = target_values / prices
        
