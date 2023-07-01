"""Strategy Class."""
from abc import ABC, abstractmethod
from pyport import HoldingsPortfolio, Holdings


class Strategy:
    """Abstract base class for strategies. Basic methods:
    test_for_rebalance(portfolio, context) -> bool
    generate_portfolio_target(context) -> Holdings
    """
    @abstractmethod
    def test_for_rebalance(portfolio, context) -> bool:
        pass

    @abstractmethod
    def generate_portfolio_holdings(context) -> Holdings:
        pass
