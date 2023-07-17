"""AssetManager is maintains the definitions and repricing duties for all assets.
Assets are registered with AssetManager using the asset name as the key.
Pricing is lazy evaluation relying on asset dependencies.
"""
from copy import deepcopy
import pandas as pd
from pyport.core.asset import AssetPrice
from pyport.core.stock import Stock
from pyport.core.option import Option
from pyport.core.basket import Basket


class AssetManager:
    def __init__(self):
        self.assets = []
        self.prices = {}

    def add_asset(self, asset):
        self.assets.append(asset)

    def _calculate_price(self, asset, market):
        if asset.name in self.prices:
            return self.prices[asset.name]

        dependencies_satisfied = all(
            dependency in self.prices for dependency in asset.dependencies
        )

        if not dependencies_satisfied:
            for dependency in asset.dependencies:
                if dependency not in self.prices:
                    dependency_asset = next(
                        a for a in self.assets if a.name == dependency
                    )
                    self._calculate_price(dependency_asset, market)

        asset_price = self._calculate_asset_price(asset, market)
        self.prices[asset.name] = asset_price
        return asset_price

    def _calculate_asset_price(self, asset, market):
        price_data = asset.reprice(market)
        price = price_data.price
        market['prices'][asset.name] = price  # for asset.reprice(market)
        return price                          # for asset_manager.prices

    def lazy_price(self, market):
        for asset in self.assets:
            if asset.name not in self.prices:
                self._calculate_price(asset, market)
        for asset in self.assets:
            yield asset.name, self.prices[asset.name]

    def reprice_assets(self, market):
        """Update asset prices.
        :return None:
        """
        market = deepcopy(market)
        _ = list(self.lazy_price(market))

    def get_asset_prices(self):
        """Return asset prices
        :return: pd.Series
        """
        return pd.Series(self.prices)


def usage_example():
    market = {'date': '1/1/2023',
                   'prices': pd.Series({'stock': 100}),
                   'volatilities': pd.Series({'stock': 0.2}),
                   'div_rates': pd.Series({'stock': 0.02}),
                   'discount_rates': 0.05
    }
    assets = {
        'stock': Stock('stock'),
        'option': Option('option', 'stock', 'call', '1/1/2024', 105),
        'basket': Basket('basket', pd.Series({'stock': 1, 'option': -1}))
    }
    manager = AssetManager()
    _ = [manager.add_asset(asset) for asset in assets.values()]
    manager.reprice_assets(market)
    return manager.get_asset_prices()

    
if __name__ == '__main__':
    print(usage_example())
