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
        self.missing_assets = {
            'option': Option('option', 'stock', 'call', '1/1/2024', 105),
            'basket': Basket('basket', pd.Series({'stock': 1, 'option': -1}))
        }
        self.all_asset_manager = AssetManager()
        _ = [self.all_asset_manager.add_asset(asset) for asset in self.all_assets.values()]
        self.missing_asset_manager = AssetManager()
        _ = [self.missing_asset_manager.add_asset(asset) for asset in self.missing_assets.values()]

    def test_add_asset(self):
        self.all_asset_manager.assets == list(self.all_assets.values())

    def test_simple_calculate_asset_price(self):
        """Let asset price be the number of its dependencies."""
        def simple_calculate_asset_price(asset, market):
            return len(asset.dependencies) * 10

        manager = self.all_asset_manager
        manager.calculate_asset_price = simple_calculate_asset_price
        manager.reprice_assets(None)
        assert manager.prices == {'stock': 0, 'option': 10, 'basket': 20}

    def test_market_calculate_asset_price(self):
        """Use pyport reprice calculations for assets."""
        manager = self.all_asset_manager
        manager.reprice_assets(self.market)
        prices = manager.get_asset_prices()
        assert prices['basket'] == prices['stock'] - prices['option']

    def test_missing_stock_asset(self):
        """Drop stock asset from manager assets, and look for exception."""
        manager = self.missing_asset_manager
        with pytest.raises(RuntimeError) as excinfo:
            prices_data = manager.reprice_assets(self.market)
        assert str(excinfo.value) == 'generator raised StopIteration'

    def test_add_missing_stock_prices(self):
        manager = self.missing_asset_manager
        manager.set_asset_price('stock', 100)
        manager.reprice_assets(self.market)
        prices = manager.get_asset_prices()
        assert prices['basket'] == prices['stock'] - prices['option']
