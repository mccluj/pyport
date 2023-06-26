"""Test of Portfolio class."""
import unittest
from pyport import Portfolio


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        pass

    def test_aum(self):
        initial_cash = 10000
        portfolio = Portfolio(initial_cash=initial_cash)
        assert portfolio.aum == initial_cash
