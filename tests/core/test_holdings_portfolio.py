"""Test of HoldingsPortfolio class."""
import unittest
import pytest
import pandas as pd
from pyport import HoldingsPortfolio, Holding, Stock


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.initial_portfolio = HoldingsPortfolio(initial_cash=10000)
        self.holding = Holding('IBM', '1/1/2023', 100, 20)
        dividends = pd.Series(1, pd.date_range('1/1/2023', periods=4, freq='BM'))
        self.context = dict(assets={symbol: Stock(symbol) for symbol in ['IBM', 'SPY', 'AGG']},
                            market={'spot_prices': {'IBM': 120,
                                                    'SPY': 400,
                                                    'AGG': 50},
                                    'date': '2/1/2023',
                                    'dividends': {'IBM': dividends}})
        self.target = pd.Series([100, 200, 300], index=['IBM', 'SPY', 'AGG'])
        
    def test_aum(self):
        assert self.initial_portfolio.aum == 10000

    def test_reprice(self):
        portfolio = self.initial_portfolio
        portfolio.add_holding(self.holding)
        assert portfolio.aum == 10000  # 8000(cash) + 2000(holdings)
        portfolio.reprice(self.context)
        assert portfolio.aum == 10420  # 8000 + 2000 * 120%

    def test_add_holding(self):
        portfolio = self.initial_portfolio
        assert portfolio.aum == 10000
        assert portfolio.cash == 10000
        assert len(portfolio.holdings) == 0
        portfolio.add_holding(self.holding)
        assert portfolio.aum == 10000
        assert portfolio.cash == 8000
        assert len(portfolio.holdings) == 1

    def test_to_string(self):
        _ = self.initial_portfolio.to_string()

    def test_rebalance(self):
        portfolio = self.initial_portfolio
        portfolio.rebalance(self.target, self.context)
        