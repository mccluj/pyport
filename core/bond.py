import numbers
import numpy as np
import pandas as pd
from pandas.tseries.frequencies import to_offset
from pyport.core.asset import Asset, AssetPrice
from pyport.core.asset_manager import AssetManager


class Bond(Asset):
    def __init__(self, name, notional, maturity):
        super().__init__(name, dependencies=[])
        self.maturity = pd.Timestamp(maturity)
        self.notional = notional

    @classmethod
    def from_market(cls, market, name, **kwargs):
        date = pd.Timestamp(market['date'])
        if 'maturity' in kwargs:
            maturity = kwargs['maturity']
        elif 'tenor' in kwargs:
            tenor = kwargs['tenor']
            if isinstance(tenor, numbers.Number):
                maturity = date + tenor * pd.Timedelta('365 Days')
            else:
                maturity = date + to_offset(tenor)
                
        if 'notional' in kwargs:
            notional = kwargs['notional']
        elif 'target_price' in kwargs:
            price = kwargs['target_price']
            rate = market['discount_rates']
            tenor = (maturity - date) / pd.Timedelta('365 Days')
            notional = price * np.exp(rate * tenor)
        return Bond(name, notional, maturity)

    def reprice(self, market):
        rate = market['discount_rates']
        date = pd.Timestamp(market['date'])
        tenor = (self.maturity - date) / pd.Timedelta('365 Days')
        price = self.notional * np.exp(-rate * tenor)
        return AssetPrice(self.name, date, price)

    def to_string(self, indent=0):
        strings = [self.name,
                   f'{self.maturity:%Y%m%d}',
                   f'{self.notional:.4f}',
                   ]
        return ' '.join(strings)
