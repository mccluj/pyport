"""Test of holding valuation structure"""
import pandas as pd
from pyport import HoldingValuation

SHOW = False


def test_holding_valuation():
    asset_income = 3
    asset_price = 120
    date = '4/1/2023'
    quantity = 20
    expected_dict = {'asset_income': asset_income,
                     'asset_price': asset_price,
                     'date': pd.Timestamp(date),
                     'holding_income': quantity * asset_income,
                     'holding_value': quantity * (asset_income + asset_price)}
    valuation = HoldingValuation(date, asset_price, asset_income, quantity)
    assert valuation.__dict__ == expected_dict
    if SHOW:
        print(valuation.to_string())
