"""Tests of Market class"""
import unittest
import pytest
import os
import pandas as pd
from pandas.testing import assert_series_equal
import pyport
from pyport import Market
from pprint import pprint


class TestMarket(unittest.TestCase):
    def setUp(self):
        data_dir = os.path.join(os.path.dirname(pyport.__file__), 'tests', 'data')
        self.stocks = ['SPY', 'IEF']
        self.config = {
            'stocks': {'symbols': self.stocks,
                       'bar_directory': data_dir,
                       'drop_na': False},
            'volatilities': {'window': 65, 'price_field': 'adj_close'},
            'dividends': {},
            'div_rates': {'window': 65},
            }
        self.market = Market(self.config)
        self.bars = Market.load_stock_bars(self.config['stocks'])

    def test_load_stock_bars(self):
        assert self.bars['SPY'].shape == (7661, 6)
        assert self.bars['IEF'].shape == (5268, 6)

    def test_calculate_volatilities(self):
        volatilities = Market.calculate_volatilities(self.bars, self.config['volatilities'])
        self.assertAlmostEqual(volatilities['SPY'].mean(), 0.167, places=3)
        self.assertAlmostEqual(volatilities['IEF'].mean(), 0.065, places=3)

    def test_calculate_dividends(self):
        """Verify dividend sum = total_gain sum - price_return_gain sum"""
        ticker = 'SPY'
        dividends = Market.calculate_dividends(self.bars)[ticker]
        bars = self.bars[ticker]
        lhs = (bars.close + dividends) / bars.close.shift()
        rhs = bars.adj_close / bars.adj_close.shift()
        assert_series_equal(lhs, rhs, check_names=False)
