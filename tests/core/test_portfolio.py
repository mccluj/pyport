"""Portfolio unittests"""
import unittest
import pytest
import pandas as pd
from pyport import Portfolio, Stock


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.context = {'assets': {'SPY': Stock('SPY'),
                                   'AGG': Stock('AGG')},
                        'market': {'date': '1/1/2023',
                                   'spot_prices': {'SPY': 400, 'AGG': 50},
                                   'dividends': {'SPY': 1}},
                        }
        self.target = pd.Series({'SPY': 10, 'AGG': 50})
        self.portfolio = Portfolio(cash=10000)

    def test_initial_portfolio(self):
        assert self.portfolio.cash == 10000
        assert self.portfolio.holdings.empty
        assert self.portfolio.trades.empty
