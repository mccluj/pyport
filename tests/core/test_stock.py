"""Test Asset class Stock"""
import unittest
import pytest
from pyport import Stock, PricingResult


class TestStock(unittest.TestCase):
    def setUp(self):
        self.market = {'date': '2023-01-01', 'spot_prices': {'SPY': 100, 'DEF': 50}}

    def test_reprice(self):
        stock = Stock('SPY')
        result = stock.reprice(self.market)
        self.assertAlmostEqual(result.price, self.market['spot_prices']['SPY'])

    def test_unit_reprice(self):
        stock = Stock('SPY')
        spot = 40
        result = stock.unit_reprice(spot)
        self.assertAlmostEqual(result, spot)

    
