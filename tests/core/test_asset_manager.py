"""Test pricing for assets."""
import unittest
import pytest
import pandas as pd
from pandas.testing import assert_series_equal
from pyport import Stock, Option, Basket, AssetManager


class TestAssets(unittest.TestCase):
    def setUp(self):
        self.market = {'date': '1/1/2023', 'prices': {'SPY': 100}}
        self.assets = {
            'stock': Stock('stock'),
            'option': Option('option', 'stock', 'call', '1/1/2023', 105),
            'basket': Basket('basket', pd.Series({'stock': 1, 'option': -1}))}
        self.manager = AssetManager()
        _ = [self.manager.add_asset(asset) for asset in self.assets.values()]

    def test_add_asset(self):
        assert self.manager.assets == list(self.assets.values())

    def test_lazy_price(self):
        manager = self.manager
        manager.lazy_price(None)
        print(manager.prices)
