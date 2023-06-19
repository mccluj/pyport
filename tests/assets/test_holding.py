"""Tests of Holding class"""
import pandas as pd
from pyport import Stock, Holding

def test_constructor():
    stock = Stock('IBM')
    date = '6/1/2023'
    price = 100
    holding = Holding(stock, date, price)
    assert holding.acquisition_date == pd.Timestamp(date)
    assert holding.acquisition_price == price
    assert isinstance(holding.asset, Stock)

def test_reprice():
    stock = Stock('IBM')
    date = '6/1/2023'
    price = 100
    holding = Holding(stock, date, price)
    market = {'spot_prices': {'IBM': 120},
              'date': date}
    result = holding.reprice(market)
    assert result.accrued_income == 0
