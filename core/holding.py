"""
Holding class. Unless needed it will not be tailored to asset type.
For now it will not inherit from Asset.
For now it has no unit_reprice. I assume pricing with no market context makes no sense.
"""
import re
import pandas as pd
# from pprint import pprint
import pprint


class Holding:
    def __init__(self, asset, acquisition_date, acquisition_price, quantity):
        self.asset = asset
        self.acquisition_date = pd.Timestamp(acquisition_date)
        self.acquisition_price = acquisition_price
        self.quantity = quantity

    def get_current_valuation(self, market):
        accrued_income = self.asset.compute_accrued_income(market, self.acquisition_date)
        price = self.asset.reprice(market).price
        return HoldingValuation(market['date'], price, accrued_income, self.quantity)

    def to_string(self):
        attributes = [f'{attr} {getattr(self, attr)}' for attr in dir(self)
                      if not callable(getattr(self, attr))
                      and re.match(r'^[A-Za-z]', attr)]
        return '\n'.join(attributes)

        
class HoldingValuation:
    def __init__(self, date, asset_price, asset_income, quantity):
        self.date = pd.Timestamp(date)
        self.asset_price = asset_price
        self.asset_income = asset_income
        self.holding_income = quantity * asset_income
        self.holding_value = quantity * (asset_price + asset_income)
                                     
    def __eq__(self, other):
        return ((self.date == other.date) &
                (self.asset_price == other.asset_price) &
                (self.asset_income == other.asset_income) &
                (self.holding_income == other.holding_income) &
                (self.holding_value == other.holding_value))

    def to_string(self):
        return pprint.pformat(self.__dict__)
