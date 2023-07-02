"""Test pricing for assets."""
import unittest
import pandas as pd
from pyport import Stock


class TestAssets(unittest.TestCase):
    def setUp(self):
        self.assets = pd.Series({'SPY': Stock('SPY'), 'AGG': Stock('AGG')})
        self.market = {'date': '1/1/2023', 'spot_prices': {'SPY': 400, 'AGG': 50}}
        
    def test_reprice_assets(self):
        prices = self.assets.apply(lambda asset: asset.reprice(self.market).price)
        print(prices)
