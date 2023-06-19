"""Tests of Holding class"""
import unittest
import pytest
import pandas as pd
from pyport import Stock, Holding


class TestHolding(unittest.TestCase):
    def setUp(self):
        self.stock = Stock('IBM')
        self.market = {'spot_prices': {'IBM': 120}, 'date': '4/1/2023'}
        self.holding = Holding(self.stock, acquisition_date='1/1/2023', acquisition_price=100)

    def test_constructor(self):
        date = '6/1/2023'
        price = 100
        holding = Holding(self.stock, date, price)
        assert holding.acquisition_date == pd.Timestamp(date)
        assert holding.acquisition_price == price
        assert isinstance(holding.asset, Stock)
        assert holding.asset.name == self.stock.name

    def test_reprice_stock_no_divs(self):
        date = '6/1/2023'
        price = 100
        holding = Holding(self.stock, date, price)
        result = holding.reprice(self.market)
        assert result.accrued_income == 0

    def test_reprice_stock_divs(self):
        dividends = pd.Series(1, pd.date_range('1/1/2023', periods=4, freq='BM'))
        market = {**self.market, 'dividends': {'IBM': dividends}, 'date': '4/1/2023'}
        assert self.holding.accrued_income == 0
        _ = self.holding.reprice(market)
        assert self.holding.accrued_income == 3
