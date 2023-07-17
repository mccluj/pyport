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

        self.all_assets = {
            'stock': Stock('stock'),
            'option': Option('option', 'stock', 'call', '1/1/2024', 105),
            'basket': Basket('basket', pd.Series({'stock': 1, 'option': -1}))
        }
        self.assets_missing_stock = {
            'option': Option('option', 'stock', 'call', '1/1/2024', 105),
            'basket': Basket('basket', pd.Series({'stock': 1, 'option': -1}))
        }
        self.manager = AssetManager()

    def test_add_asset(self):
        _ = [self.manager.add_asset(asset) for asset in self.all_assets.values()]
        assert self.manager.assets == list(self.all_assets.values())

    def test_simple_calculate_asset_price(self):
        """Let asset price be the number of its dependencies."""
        def simple_calculate_asset_price(asset, market):
            return len(asset.dependencies) * 10

        manager = self.manager
        _ = [manager.add_asset(asset) for asset in self.all_assets.values()]
        manager.calculate_asset_price = simple_calculate_asset_price
        manager.reprice_assets(None)
        assert manager.prices == {'stock': 0, 'option': 10, 'basket': 20}

    def test_market_calculate_asset_price(self):
        """Use pyport reprice calculations for assets."""
        manager = self.manager
        _ = [manager.add_asset(asset) for asset in self.all_assets.values()]
        manager.reprice_assets(self.market)
        prices = manager.get_asset_prices()
        assert prices['basket'] == prices['stock'] - prices['option']

    def test_missing_stock_asset(self):
        """Drop stock asset from manager assets, and look for exception."""
        manager = self.manager
        _ = [manager.add_asset(asset) for asset in self.assets_missing_stock.values()]
        with pytest.raises(RuntimeError) as excinfo:
            prices_data = manager.reprice_assets(self.market)
        assert str(excinfo.value) == 'generator raised StopIteration'
