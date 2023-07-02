"""Portfolio unittests"""
import unittest
import pytest
import pandas as pd
from pyport import Portfolio, Stock


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.cash = 10000
        self.prices = pd.Series({'SPY': 400, 'AGG': 50})
        self.dividends = pd.Series({'SPY': 0})
        self.context = {'assets': {'SPY': Stock('SPY'),
                                   'AGG': Stock('AGG')},
                        'market': {'date': '1/1/2023',
                                   'prices': self.prices,
                                   'dividends': self.dividends},
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

    def test_reprice_dividends(self):
        portfolio = self.rebalanced_portfolio
        dividends = self.context['market']['dividends']
        div_change = 10
        portfolio.reprice(self.context)
        aum_0 = portfolio.aum
        dividends['SPY'] += div_change
        portfolio.reprice(self.context)
        aum_1 = portfolio.aum
        assert aum_1 - aum_0 == portfolio.holdings['SPY'] * div_change

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
