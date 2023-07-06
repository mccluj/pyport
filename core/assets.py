"""Assets -- Asset container class"""
import pandas as pd
from pyport.core.stock import Stock


class Assets:
    def __init__(self, assets=None, stocks=None):
        """
        :param assets: dict -- {symbol: Asset}
        :param stocks: list(str) -- stock symbols
        """
        if assets is None:
            assets = {}
        if stocks is not None:
            stock_assets = {name: Stock(name) for name in stocks}
            assets = {**assets, **stock_assets}
        self.assets = assets
                

    def add_asset(self, name, asset):
        self.assets[name] = asset
    
    def remove_asset(self, name):
        del self.assets[name]

    
