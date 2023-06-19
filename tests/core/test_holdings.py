"""Tests of Holdings container class"""
import unittest
import pytest
import pandas as pd
from pyport import Stock, Holding


class TestHoldings(unittest.TestCase):
    def setUp(self):
        self.stock = Stock('IBM')
        self.market = {'spot_prices': {'IBM': 120}, 'date': '4/1/2023'}
        self.holding = Holding(self.stock, acquisition_date='1/1/2023', acquisition_price=100)

    def test_constructor(self):
        holdings = Holdings()
        assert len(holdings.get_holdings()) == 0

    def test_add_holding(self):
        holdings = Holdings()
        holdings.add_holding(self.holding)
        assert len(holdings.holdings) == 1
        holdings.add_holding(self.holding)
        assert len(holdings.holdings) == 2

    def test_remove_holding(self):
        holdings = Holdings()
        holdings.add_holding(self.holding)
        assert len(holdings.holdings) == 1
        holdings.add_holding(self.holding)
        assert len(holdings.holdings) == 1
