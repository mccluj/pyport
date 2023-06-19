"""
Holding class. Unless needed it will not be tailored to asset type.
For now it will not inherit from Asset.
For now it has no unit_reprice. I assume pricing with no market context makes no sense.
"""
import pandas as pd


class Holding:
    def __init__(self, asset, acquisition_date, acquisition_price):
        self.asset = asset
        self.acquisition_date = pd.Timestamp(acquisition_date)
        self.acquisition_price = acquisition_price

    def reprice(self, market):
        results = self.asset.reprice(market)
        results.accrued_income = self.asset.compute_accrued_income(market, self.acquisition_date)
        results.price += results.accrued_income
        # results.acquisition_date = acquisition_date
        # results.acquisition_price = acquisition_price
        return results
