"""Tests of Holding class"""
import unittest
import pytest
import pandas as pd
from pyport import Stock, Holding, HoldingValuation

SHOW = False


class TestHolding(unittest.TestCase):
    def setUp(self):
        self.stock = Stock('IBM')
        self.date = '4/1/2023'
        dividends = pd.Series(1, pd.date_range('1/1/2023', periods=4, freq='BM'))
        self.market = {'spot_prices': {'IBM': 120},
                       'date': self.date,
                       'dividends': {'IBM': dividends}}
        self.holding = Holding(self.stock, acquisition_date='1/1/2023', acquisition_price=100,
                               quantity=20)

    def test_constructor(self):
        date = '6/1/2023'
        price = 100
        quantity = 20
        holding = Holding(self.stock, date, price, quantity=quantity)
        assert holding.acquisition_date == pd.Timestamp(date)
        assert holding.acquisition_price == price
        assert holding.asset.name == self.stock.name
        assert holding.quantity == quantity

    def test_reprices_with_no_divs(self):
        market = self.market
        del market['dividends']
        self.holding.reprice(market)
        valuation = self.holding.valuation
        expected = HoldingValuation(self.date, 120, 0, 20)
        self.assertEqual(expected, valuation)
        if SHOW:
            print(valuation.to_string())

    def test_reprices_with_divs(self):
        self.holding.reprice(self.market)
        valuation = self.holding.valuation
        expected = HoldingValuation(self.date, 120, 3, 20)
        self.assertEqual(expected, valuation)
        if SHOW:
            print(valuation.to_string())

    def test_reprices_not_inplace(self):
        result = self.holding.reprice(self.market, inplace=False)
        expected = HoldingValuation(self.date, 120, 3, 20)
        self.assertEqual(expected, result.valuation)

    def test_reprices_inplace(self):
        result = self.holding.reprice(self.market, inplace=True)
        self.assertEqual(result, None)
