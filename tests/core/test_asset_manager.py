"""Test pricing for assets."""
import unittest
import pytest
import pandas as pd
from pandas.testing import assert_series_equal
from pyport import Stock, Option, Basket, AssetManager


class TestAssetManager(unittest.TestCase):
    def setUp(self):
        self.asset_manager = AssetManager()

    def tearDown(self):
        self.asset_manager.reset()

    def test_add_and_get_asset(self):
        # Create some assets
        option1 = Option('option', 'stock', 'call', '1/1/2024', 105),
        option2 = Option('option', 'stock', 'put', '1/1/2024', 105),

        # Add assets to the asset_manager
        self.asset_manager.add_asset("option1", option1)
        self.asset_manager.add_asset("option2", option2)

        # Retrieve the assets and check if they are correct
        self.assertEqual(self.asset_manager.get_asset("option1"), option1)
        self.assertEqual(self.asset_manager.get_asset("option2"), option2)

    def test_remove_asset(self):
        # Create an asset
        option = Option('option', 'stock', 'call', '1/1/2024', 105),

        # Add the asset to the asset_manager
        self.asset_manager.add_asset("option", option)

        # Check if the asset is present before removal
        self.assertEqual(self.asset_manager.get_asset("option"), option)

        # Remove the asset from the asset_manager
        self.asset_manager.remove_asset("option")

        # Check if the asset is removed
        self.assertIsNone(self.asset_manager.get_asset("option"))

    def test_singleton_instance(self):
        # Ensure that the same instance is returned every time
        asset_manager1 = AssetManager()
        asset_manager2 = AssetManager()

        self.assertIs(asset_manager1, asset_manager2)


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
        self.asset_manager = AssetManager()
        _ = [self.asset_manager.add_asset(name, asset) for name, asset in self.assets.items()]

    def tearDown(self):
        self.asset_manager.reset()

    def test_simple_calculate_asset_price(self):
        """Let asset price be the number of its dependencies."""
        def simple_calculate_asset_price(asset, market):
            return len(asset.dependencies) * 10

        manager = self.asset_manager
        manager._calculate_leaf_node_asset_price = simple_calculate_asset_price
        manager.reprice_assets(None)
        assert manager.prices == {'stock': 0, 'option': 10, 'basket': 20}

    def test_market_calculate_asset_price(self):
        """Use pyport reprice calculations for assets."""
        manager = self.asset_manager
        manager.reprice_assets(self.market)
        prices = manager.get_asset_prices()
        assert prices['basket'] == prices['stock'] - prices['option']

    def test_missing_stock_asset(self):
        """Drop stock asset from manager assets, and look for exception."""
        manager = self.asset_manager
        manager.remove_asset('stock')
        with pytest.raises(RuntimeError) as excinfo:
            manager.reprice_assets(self.market)
        assert str(excinfo.value) == "Cannot find asset 'stock'"
