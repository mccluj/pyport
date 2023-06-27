"""Test of Portfolio class."""
import unittest
import pytest
import pandas as pd
from pyport import Portfolio, Holding, Stock


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.initial_portfolio = Portfolio(initial_cash=10000)
        self.holding = Holding('IBM', '1/1/2023', 100, 20)
        dividends = pd.Series(1, pd.date_range('1/1/2023', periods=4, freq='BM'))
        self.context = dict(assets={'IBM': Stock('IBM')},
                            market={'spot_prices': {'IBM': 120},
                                    'date': '2/1/2023',
                                    'dividends': {'IBM': dividends}})
        
    def test_aum(self):
        assert self.initial_portfolio.aum == 10000

    @pytest.mark.skip
    def test_reprice(self):
        portfolio = self.initial_portfolio
        portfolio.add_holding(self.holding)
        portfolio.reprice(self.context)
        print(portfolio.to_string())

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
