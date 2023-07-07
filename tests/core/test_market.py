"""Tests of Market class"""
import unittest
import pytest
import os
import pandas as pd
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
            }
        # pprint(config)
        # self.market = Market(self.config)

    def test_load_stock_bars(self):
        bars = Market.load_stock_bars(self.config['stocks'])
        assert bars['SPY'].shape == (7661, 6)
        assert bars['IEF'].shape == (5268, 6)
