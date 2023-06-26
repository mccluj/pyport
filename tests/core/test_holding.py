"""Tests of Holding class"""
import unittest
import pytest
import pandas as pd
from pandas.testing import assert_series_equal
from pyport import Stock, Holding, HoldingValuation

SHOW = False


class TestHolding(unittest.TestCase):
    def setUp(self):
        self.stock = 'IBM'
        self.date = '4/1/2023'
        dividends = pd.Series(1, pd.date_range('1/1/2023', periods=4, freq='BM'))
        self.context = dict(assets={'IBM': Stock('IBM')},
                            market={'spot_prices': {'IBM': 120},
                                    'date': self.date,
                                    'dividends': {'IBM': dividends}})
        self.holding = Holding(self.stock, acquisition_date='1/1/2023', acquisition_price=100,
                               quantity=20)

    def test_constructor(self):
        assert self.holding.asset == 'IBM'
        assert self.holding.acquisition_date == pd.Timestamp('1/1/2023')
        assert self.holding.acquisition_price == 100
        assert self.holding.quantity == 20

    def test_reprices_with_no_divs(self):
        del self.context['market']['dividends']
        self.holding.reprice(self.context)
        valuation = self.holding.valuation
        expected = HoldingValuation(self.date, 120, 0, 20)
        self.assertEqual(expected, valuation)
        if SHOW:
            print(valuation.to_string())

    def test_reprices_with_divs(self):
        self.holding.reprice(self.context)
        valuation = self.holding.valuation
        expected = HoldingValuation(self.date, 120, 3, 20)
        self.assertEqual(expected, valuation)
        if SHOW:
            print(valuation.to_string())

    def test_reprices_not_inplace(self):
        result = self.holding.reprice(self.context, inplace=False)
        expected = HoldingValuation(self.date, 120, 3, 20)
        self.assertEqual(expected, result.valuation)

    def test_reprices_inplace(self):
        result = self.holding.reprice(self.context, inplace=True)
        self.assertEqual(result, None)

    def test_attributes(self):
        expected = pd.Series({'symbol': 'IBM',
                              'acquisition_date': pd.Timestamp('1/1/2023'),
                              'acquisition_price': 100,
                              'quantity': 20})
        assert_series_equal(self.holding.attributes, expected)

    def test_to_series(self):
        attributes = pd.Series({'symbol': 'IBM',
                                'acquisition_date': pd.Timestamp('1/1/2023'),
                                'acquisition_price': 100,
                                'quantity': 20})
        # Without valuation.
        expected = attributes
        assert_series_equal(self.holding.to_series(), expected)
        self.holding.reprice(self.context, inplace=True)
        # With valuation.
        valuation = HoldingValuation(self.date, 120, 3, 20).to_series()
        expected = pd.concat([attributes, valuation])
        assert_series_equal(self.holding.to_series(), expected)

