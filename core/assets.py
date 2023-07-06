"""Assets -- Asset container class"""
import pandas as pd


class Assets:
    def __init__(self, assets=None, stocks=None):
        """
        :param assets: dict -- {symbol: Asset}
        :param stocks: list(str) -- stock symbols
        """
        if assets is None:
            assets = {}
        if stocks is not None:
            for symbol in stocks:
                assets[symbol] = Stock(symbol)
        self.assets = assets
                

    def add_asset(self, name, asset):
        self.assets[name] = asset
    
    def remove_asset(self, name):
        del self.asset[name]

    
