"""Test pricing for assets."""
import unittest
import pytest
import pandas as pd
from pandas.testing import assert_series_equal
from pyport import Stock, AssetManager


class TestAssets(unittest.TestCase):
    def setUp(self):
        self.market = {'date': '1/1/2023', 'prices': {'SPY': 400, 'AGG': 50}}

    def test_null_constructor(self):
        assets = AssetManager()
        assert not assets.assets
    
    def test_constructor_with_assets(self):
        stock_assets = {'xyz': Stock('XYZ')}
        assets = AssetManager(assets=stock_assets)
        assert assets.assets == stock_assets
        
    def test_constructor_with_stocks(self):
        stocks = ['SPY', 'AGG']
        assets = AssetManager(stocks=stocks)
        assert sorted(assets.assets.keys()) == sorted(stocks)

    def test_constructor_with_assets_and_stocks(self):
        stocks = ['SPY', 'AGG']
        stock_assets = {'xyz': Stock('XYZ')}
        assets = AssetManager(assets=stock_assets, stocks=stocks)
        assert sorted(assets.assets.keys()) == sorted(stocks + list(stock_assets))

    def test_add_asset(self):
        stocks = ['SPY', 'AGG']
        assets = AssetManager(stocks=stocks)
        assets.add_asset('xyz', Stock('XYZ'))
        assert sorted(assets.assets.keys()) == sorted(stocks + ['xyz'])

    def test_remove_asset_fail(self):
        stocks = ['SPY', 'AGG']
        assets = AssetManager(stocks=stocks)
        with pytest.raises(KeyError):
            assets.remove_asset('xyz')

    def test_remove_asset_success(self):
        stocks = ['SPY', 'AGG']
        assets = AssetManager(stocks=stocks)
        assets.remove_asset('AGG')
        assert list(assets.assets) == ['SPY']
