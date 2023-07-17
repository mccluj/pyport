"""Test of Basket class"""
import unittest
import pandas as pd
from pandas.testing import assert_series_equal, assert_frame_equal
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
        self.target_value = 10000

    def test_constructor(self):
        basket = Basket('basket', self.shares)
        assert_series_equal(basket.shares, self.shares)

    def test_instantiate_from_weights(self):
        basket = Basket.instantiate_from_market(self.market, 'basket',
                                                weights=self.weights, target_value=self.target_value)
        expected_shares = self.weights * self.target_value / pd.Series(self.market['prices'])
        assert_series_equal(basket.shares, expected_shares)

    def test_instantiate_from_shares(self):
        basket = Basket.instantiate_from_market(self.market, 'basket', shares=self.shares)
        expected_shares = self.shares
        assert_series_equal(basket.shares, expected_shares)

    def test_instantiate_from_shares_and_weights(self):
        """Verify shares take precendence"""
        basket = Basket.instantiate_from_market(self.market, 'basket', shares=self.shares,
                                                weights=self.weights, target_value=self.target_value)
        expected_shares = self.shares
        assert_series_equal(basket.shares, expected_shares)

    def test_reprice(self):
        basket = Basket('test', self.shares)
        data = basket.reprice(self.market)
        expected_price = 1800
        expected_frame = pd.DataFrame([[10, 100], [20, 40]], index=['SPY', 'XYZ'], columns=['shares', 'price'])
        self.assertAlmostEqual(data.price, expected_price)
        assert_frame_equal(data.asset_data, expected_frame)
