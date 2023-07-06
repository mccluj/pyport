"""Test pricing for assets."""
import unittest
import pandas as pd
from pandas.testing import assert_series_equal
from pyport import Stock, Assets


class TestAssets(unittest.TestCase):
    def setUp(self):
        self.market = {'date': '1/1/2023', 'spot_prices': {'SPY': 400, 'AGG': 50}}

    def test_constructor(self):
        assets = Assets()
        assert not assets.assets
        stock_assets = {'xyz': Stock('XYZ')}
        assets = Assets(assets=stock_assets)
        assert assets.assets == stock_assets

    def test_add_asset(self):
        pass
