"""Portfolio unittests"""
import unittest
import pytest
import textwrap
import pandas as pd
from pyport import Portfolio, Stock


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.cash = 10000
        self.prices = pd.Series({'SPY': 400, 'AGG': 50})
        self.market = {'date': '1/1/2023', 'prices': self.prices}
        self.target = pd.Series({'SPY': 10, 'AGG': 50})
        self.initial_portfolio = Portfolio(cash=self.cash)
        self.rebalanced_portfolio = Portfolio(cash=self.cash)
        self.rebalanced_portfolio.rebalance(self.market, self.target)

    def test_initial_portfolio(self):
        portfolio = self.initial_portfolio
        assert portfolio.cash == self.cash
        assert portfolio.aum == self.cash
        assert portfolio.positions.empty
        assert portfolio.trades.empty

    def test_rebalance(self):
        portfolio = self.rebalanced_portfolio
        target_value = self.prices @ self.target
        assert portfolio.aum == self.cash
        assert portfolio.cash == self.cash - target_value

    def test_add_dividends_to_cash(self):
        portfolio = self.rebalanced_portfolio
        aum_0 = portfolio.aum
        div_amount = 5
        dividends = pd.Series({'SPY': div_amount})
        portfolio.add_dividends_to_cash(dividends)
        assert portfolio.aum - aum_0 == portfolio.positions['SPY'] * div_amount
        # Note to users: cash from dividends accumulate.
        portfolio.add_dividends_to_cash(dividends)
        assert portfolio.aum - aum_0 == portfolio.positions['SPY'] * 2 * div_amount

    def test_mark_positions(self):
        portfolio = self.rebalanced_portfolio
        prices = self.prices
        price_change = 100
        portfolio.mark_positions(prices)
        aum_0 = portfolio.aum
        prices['SPY'] += price_change
        portfolio.mark_positions(prices)
        aum_1 = portfolio.aum
        assert aum_1 - aum_0 == portfolio.positions['SPY'] * price_change

    def test_to_string(self):
        expected = textwrap.dedent("""
        Portfolio(cash=3500.0, aum=10000.0):
        positions:
             position  price
        SPY        10    400
        AGG        50     50
        """).strip()
        assert expected == self.rebalanced_portfolio.to_string()
