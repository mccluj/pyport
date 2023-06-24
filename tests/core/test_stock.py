"""Test Asset class Stock"""
import pandas as pd
import unittest
import pytest
from pyport import Stock, PricingResult


class TestStock(unittest.TestCase):
    def setUp(self):
        self.market = {'date': '2023-01-01', 'spot_prices': {'SPY': 100, 'DEF': 50}}
        self.stock = Stock('SPY')

    def test_reprice(self):
        result = self.stock.reprice(self.market)
        self.assertAlmostEqual(result.price, self.market['spot_prices']['SPY'])

    def test_unit_reprice(self):
        spot = 40
        result = self.stock.unit_reprice(spot)
        self.assertAlmostEqual(result, spot)

    def test_accrued_income(self):
        dividends = pd.Series(1, pd.date_range('1/1/2023', periods=4, freq='BM'))
        market = {**self.market, 'dividends': {'SPY': dividends}, 'date': '4/1/2023'}
        income = self.stock.compute_accrued_income(market, acquisition_date='1/1/2023')
        assert income == 3

    def test_accrued_income_no_dividends(self):
        dividends = None
        market = {**self.market, 'dividends': {'SPY': dividends}, 'date': '4/1/2023'}
        income = self.stock.compute_accrued_income(market, acquisition_date='1/1/2023')
        assert income == 0
