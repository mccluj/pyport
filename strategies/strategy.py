"""Strategy Class."""
import pandas as pd
from abc import ABC, abstractmethod
from pyport import Portfolio


class Strategy:
    """Abstract base class for strategies. Basic methods:
    test_for_rebalance(portfolio, context) -> bool
    generate_portfolio_target(context) -> pd.Series
    """
    @abstractmethod
    def test_for_rebalance(portfolio, context) -> bool:
        pass

    @abstractmethod
    def generate_portfolio_target(context) -> pd.Series:
        pass

    @staticmethod
    def target_from_weights(weights, aum, market, assets):
        aum = portfolio.aum
        allocations = aum * weights
        assets = assets.reindex(weights.index)
        prices = assets.apply(lambda asset: asset.reprice(market).price)
        target = allocations.div(prices)
        return target
