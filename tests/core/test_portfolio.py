"""Test of Portfolio class."""
import unittest
from pyport import Portfolio, Holding


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.initial_portfolio = Portfolio(initial_cash=10000)
        self.holding = Holding('IBM', '1/1/2023', 100, 20)
        
    def test_aum(self):
        assert self.initial_portfolio.aum == 10000

    def test_add_holding(self):
        portfolio = self.initial_portfolio
        assert portfolio.aum == 10000
        assert portfolio.cash == 10000
        assert portfolio.holdings.shape[0] == 0
        portfolio.add_holding(self.holding)
        assert portfolio.aum == 10000
        assert portfolio.cash == 8000
        assert portfolio.holdings.shape[0] == 1

    def test_to_string(self):
        _ = self.initial_portfolio.to_string()
