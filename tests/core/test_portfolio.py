"""Portfolio unittests"""
import unittest
import pytest
import pandas as pd
from pyport import Portfolio, Stock


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.cash = 10000
        self.prices = pd.Series({'SPY': 400, 'AGG': 50})
        self.context = {'assets': {'SPY': Stock('SPY'),
                                   'AGG': Stock('AGG')},
                        'market': {'date': '1/1/2023',
                                   'prices': self.prices},
                        }
        self.target = pd.Series({'SPY': 10, 'AGG': 50})
        self.initial_portfolio = Portfolio(cash=self.cash)
        self.rebalanced_portfolio = Portfolio(cash=self.cash)
        self.rebalanced_portfolio.rebalance(self.target, self.context)

    def test_initial_portfolio(self):
        portfolio = self.initial_portfolio
        assert portfolio.cash == self.cash
        assert portfolio.aum == self.cash
        assert portfolio.holdings.empty
        assert portfolio.trades.empty

    def test_rebalance(self):
        portfolio = self.rebalanced_portfolio
        # portfolio.rebalance(self.target, self.context)
        target_value = self.prices @ self.target
        assert portfolio.aum == self.cash
        assert portfolio.cash == self.cash - target_value

    def test_apply_dividends(self):
        portfolio = self.rebalanced_portfolio
        aum_0 = portfolio.aum
        div_amount = 5
        dividends = pd.Series({'SPY': div_amount})
        portfolio.apply_dividends(dividends)
        assert portfolio.aum - aum_0 == portfolio.holdings['SPY'] * div_amount
        # Note cash from dividends accumulate.
        portfolio.apply_dividends(dividends)
        assert portfolio.aum - aum_0 == portfolio.holdings['SPY'] * 2 * div_amount



        div_change = 10
        dividends['SPY'] += div_change
        portfolio.apply_dividends(dividends)

    def test_reprice_prices(self):
        portfolio = self.rebalanced_portfolio
        prices = self.context['market']['prices']
        price_change = 100
        portfolio.reprice(self.context)
        aum_0 = portfolio.aum
        prices['SPY'] += price_change
        portfolio.reprice(self.context)
        aum_1 = portfolio.aum
        assert aum_1 - aum_0 == portfolio.holdings['SPY'] * price_change
