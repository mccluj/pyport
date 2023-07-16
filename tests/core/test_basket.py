"""Test of Basket class"""
import unittest
import pandas as pd
from pandas.testing import assert_series_equal
from pyport import Stock, Basket
from argparse import Namespace


class TestBasket(unittest.TestCase):
    def setUp(self):
        assets = pd.Series({name: Stock(name) for name in ['SPY', 'XYZ']})
        self.market = dict(assets=assets,
                           prices=pd.Series({'SPY': 100, 'XYZ': 40}),
                           date='1/1/2023')
        self.shares = pd.Series({'SPY': 10, 'XYZ': 20})
        self.weights = pd.Series({'SPY': 0.8, 'XYZ': 0.2})
        self.aum = 10000

    def test_shares_constructor(self):
        basket = Basket('shares', shares=self.shares)
        assert_series_equal(basket.shares, self.shares)

    def test_weights_constructor(self):
        basket = Basket('weights', weights=self.weights, aum=self.aum)
        assert basket.shares is None
        expected_shares = self.weights * self.aum / pd.Series(self.market['prices'])
        basket = Basket('weights', weights=self.weights, aum=self.aum).instantiate(self.market)
        assert_series_equal(basket.shares, expected_shares)
