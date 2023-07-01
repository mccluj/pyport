"""Tests of fixed weight strategy (e.g. 60/40), reblance periodically (e.g. monthly)"""
import unittest
import pandas as pd
from pyport.strategies import FixedWeightStrategy as Strategy
from pyport import HoldingsPortfolio, Stock


class TestStrategy(unittest.TestCase):
    def setUp(self):
        self.assets = {ticker: Stock(ticker) for ticker in ['SPY', 'AGG']}
        self.market = {'spot_prices': pd.Series({'SPY': 400, 'AGG': 50})}
        self.weights = pd.Series({'SPY': 0.6, 'AGG': 0.4})
        self.strategy = Strategy(weights=self.weights, frequency='BM', maximum_deviation=0.05)

    def test_initial_rebalance(self):
        portfolio = HoldingsPortfolio(initial_cash=10000)
        context = {'market': self.market, 'portfolio': portfolio, 'assets': self.assets}
        holdings = self.strategy.generate_portfolio_holdings(context)
        print(holdings)

