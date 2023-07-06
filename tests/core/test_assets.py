"""Test pricing for assets."""
import unittest
import pandas as pd
from pandas.testing import assert_series_equal
from pyport import Stock, Assets


class TestAssets(unittest.TestCase):
    def setUp(self):
        self.market = {'date': '1/1/2023', 'spot_prices': {'SPY': 400, 'AGG': 50}}

    def test_null_constructor(self):
        assets = Assets()
        assert not assets.assets
    
    def test_constructor_with_assets(self):
        stock_assets = {'xyz': Stock('XYZ')}
        assets = Assets(assets=stock_assets)
        assert assets.assets == stock_assets
        
    def test_constructor_with_stocks(self):
        stocks = ['SPY', 'AGG']
        assets = Assets(stocks=stocks)
        assert sorted(assets.assets.keys()) == sorted(stocks)

    def test_constructor_with_assets_and_stocks(self):
        stocks = ['SPY', 'AGG']
        stock_assets = {'xyz': Stock('XYZ')}
        assets = Assets(assets=stock_assets, stocks=stocks)
        assert sorted(assets.assets.keys()) == sorted(stocks + list(stock_assets))

    def test_add_asset(self):
        pass
