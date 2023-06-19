"""Stock asset class"""
import pandas as pd
from pyport import Asset, PricingResult


class Stock(Asset):
    def __init__(self, name):
        super().__init__(name)
        self.price = None

    def unit_reprice(self, spot):
        return spot

    def reprice(self, market):
        spot = market['spot_prices'][self.name]
        price = self.unit_reprice(spot)
        return PricingResult(self.name, price, market['date'])

    def compute_accrued_income(self, market, acquisition_date):
        """Accrue dividends after acquisition date and on or before market date."""
        dividends = market.get('dividends', {}).get(self.name, pd.Series(dtype=float))
        mask = (dividends.index > acquisition_date) & (dividends.index <= market['date'])
        return dividends.loc[mask].sum()
