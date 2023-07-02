"""Portfolio unittests"""
import unittest
import pytest
import pandas as pd
from pyport import Portfolio, Stock


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.cash = 10000
        self.prices = pd.Series({'SPY': 400, 'AGG': 50})
        self.dividends = pd.Series({'SPY': 1})
        self.context = {'assets': {'SPY': Stock('SPY'),
                                   'AGG': Stock('AGG')},
                        'market': {'date': '1/1/2023',
                                   'spot_prices': self.prices,
                                   'dividends': self.dividends},
                        }
        self.target = pd.Series({'SPY': 10, 'AGG': 50})
        self.portfolio = Portfolio(cash=self.cash)

    def test_initial_portfolio(self):
        assert self.portfolio.cash == self.cash
        assert self.portfolio.aum == self.cash
        assert self.portfolio.holdings.empty
        assert self.portfolio.trades.empty

    def test_rebalance(self):
        self.portfolio.rebalance(self.target, self.context)
        target_value = self.prices @ self.target
        assert self.portfolio.aum == self.cash
        assert self.portfolio.cash == self.cash - target_value
