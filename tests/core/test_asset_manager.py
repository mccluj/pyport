"""Test pricing for assets."""
import unittest
import pytest
import pandas as pd
from pandas.testing import assert_series_equal
from pyport import Stock, Option, Basket, AssetManager


class TestAssets(unittest.TestCase):
    def setUp(self):
        self.market = {'date': '1/1/2023',
                       'prices': pd.Series({'stock': 100}),
                       'volatilities': pd.Series({'stock': 0.2}),
                       'div_rates': pd.Series({'stock': 0.02}),
                       'discount_rates': 0.05}

        self.assets = {
            'stock': Stock('stock'),
            'option': Option('option', 'stock', 'call', '1/1/2024', 105),
            'basket': Basket('basket', pd.Series({'stock': 1, 'option': -1}))}
        self.manager = AssetManager()
        _ = [self.manager.add_asset(asset) for asset in self.assets.values()]

    def test_add_asset(self):
        assert self.manager.assets == list(self.assets.values())

    def test_simple_calculate_asset_price(self):
        """Let asset price be the number of its dependencies."""
        def simple_calculate_asset_price(asset, market):
            return len(asset.dependencies) * 10

        manager = self.manager
        manager.calculate_asset_price = simple_calculate_asset_price
        prices = manager.reprice_assets(None)
        assert prices == {'stock': 0, 'option': 10, 'basket': 20}

    def test_market_calculate_asset_price(self):
        """Use pyport reprice calculations for assets."""
        manager = self.manager
        prices_data = manager.reprice_assets(self.market)
        prices = pd.Series({name: data.price for name, data in prices_data.items()})
        # assert prices['basket'] == prices['stock'] - prices['option']
