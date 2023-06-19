"""
Holding class. Unless needed it will not be tailored to asset type.
For now it will not inherit from Asset.
For now it has no unit_reprice. I assume pricing with no market context makes no sense.
"""
import re
import pandas as pd


class Holding:
    def __init__(self, asset, acquisition_date, acquisition_price):
        self.asset = asset
        self.acquisition_date = pd.Timestamp(acquisition_date)
        self.acquisition_price = acquisition_price
        self.accrued_income = 0

    def reprice(self, market):
        results = self.asset.reprice(market)
        self.accrued_income = self.asset.compute_accrued_income(market, self.acquisition_date)
        results.price += self.accrued_income
        results.accrued_income = self.accrued_income
        return results

    def to_string(self):
        attributes = [f'{attr} {getattr(self, attr)}' for attr in dir(self)
                      if not callable(getattr(self, attr))
                      and re.match(r'^[A-Za-z]', attr)]
        return '\n'.join(attributes)
