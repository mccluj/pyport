"""Tests of Holdings container class"""
import unittest
import pytest
import pandas as pd
from pyport import Stock, Holding, Holdings


class TestHoldings(unittest.TestCase):
    def setUp(self):
        self.stock = Stock('IBM')
        self.market = {'spot_prices': {'IBM': 120}, 'date': '4/1/2023'}
        self.holding = Holding(self.stock, acquisition_date='1/1/2023', acquisition_price=100, quantity=20)
        self.second_holding = Holding(self.stock, acquisition_date='1/1/2023', acquisition_price=100, quantity=30)

    def test_constructor(self):
        holdings = Holdings()
        assert len(holdings.get_holdings()) == 0

    def test_add_holding(self):
        holdings = Holdings()
        holdings.add_holding(self.holding)
        assert len(holdings.holdings) == 1
        holdings.add_holding(self.holding)
        assert len(holdings.holdings) == 2

    def test_remove_holding_one_in_one_out(self):
        holdings = Holdings()
        holdings.add_holding(self.holding)
        assert len(holdings.holdings) == 1
        holdings.remove_holding(self.holding)
        assert len(holdings.holdings) == 0

    def test_remove_holding_two_identical_in_one_out(self):
        holdings = Holdings()
        holdings.add_holding(self.holding)
        assert len(holdings.holdings) == 1
        holdings.add_holding(self.holding)
        assert len(holdings.holdings) == 2
        holdings.remove_holding(self.holding)
        assert len(holdings.holdings) == 1

    def test_remove_holding_two_different_in_one_out(self):
        holdings = Holdings()
        holdings.add_holding(self.holding)
        assert len(holdings.holdings) == 1
        holdings.add_holding(self.second_holding)
        assert len(holdings.holdings) == 2
        holdings.remove_holding(self.holding)
        assert len(holdings.holdings) == 1
        self.assertEqual(holdings.get_holdings()[0], self.second_holding)
