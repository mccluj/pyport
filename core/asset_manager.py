"""
This module implements an AssetManager class that manages a collection of assets
and calculates their prices based on market data. It provides methods to add assets,
calculate prices, and retrieve asset prices. The AssetManager class supports assets
with dependencies, where the price of an asset depends on the prices of its dependencies.

Usage Example:
--------------
market = {
    'date': '1/1/2023',
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
asset_prices = manager.get_asset_prices()

"""

from copy import deepcopy
import pandas as pd
from pyport.core.asset import AssetPrice
from pyport.core.stock import Stock
from pyport.core.option import Option
from pyport.core.basket import Basket


from copy import deepcopy
import pandas as pd
from pyport.core.asset import AssetPrice
from pyport.core.stock import Stock
from pyport.core.option import Option
from pyport.core.basket import Basket


class AssetManager:
    def __init__(self):
        """Initialize the AssetManager class."""
        self.assets = {}  # Dictionary to store assets
        self.prices = {}  # Dictionary to store asset prices

    def add_asset(self, asset):
        """Add an asset to the AssetManager.

        Args:
            asset: An instance of the Asset class.

        """
        self.assets[asset.name] = asset

    def _calculate_recursive_asset_price(self, asset, market):
        """Calculate the price of an asset.

        This is a recursive function that calculates the price of an asset by
        considering its dependencies. It checks if the asset price is already
        calculated in the 'prices' dictionary. If not, it recursively calculates
        the prices of its dependencies before calculating the asset price.

        Args:
            asset: An instance of the Asset class.
            market: Dictionary containing market data.

        Returns:
            The calculated price of the asset.

        """
        if asset.name in self.prices:
            return self.prices[asset.name]

        dependencies_satisfied = all(
            dependency in self.prices for dependency in asset.dependencies
        )

        if not dependencies_satisfied:
            for dependency in asset.dependencies:
                if dependency not in self.prices:
                    dependency_asset = self.assets.get(dependency)
                    if dependency_asset is not None:
                        self._calculate_recursive_asset_price(dependency_asset, market)
                    else:
                        raise RuntimeError(f"Cannot find asset '{dependency}'")

        asset_price = self._calculate_leaf_node_asset_price(asset, market)
        self.prices[asset.name] = asset_price
        return asset_price

    def _calculate_leaf_node_asset_price(self, asset, market):
        """Calculate the price of an individual asset.

        Args:
            asset: An instance of the Asset class.
            market: Dictionary containing market data.

        Returns:
            The calculated price of the asset.

        """
        price_data = asset.reprice(market)
        price = price_data.price
        market['prices'][asset.name] = price
        return price

    def lazy_price(self, market):
        """Calculate prices for all assets.

        This method calculates the prices of all assets that haven't been
        calculated yet.

        Args:
            market: Dictionary containing market data.

        Yields:
            A tuple containing the asset name and its price.

        """
        for name, asset in self.assets.items():
            if name not in self.prices:
                self._calculate_recursive_asset_price(asset, market)
        for asset in self.assets:
            yield name, self.prices[name]

    def reprice_assets(self, market):
        """Update asset prices.

        This method updates the prices of all assets in the AssetManager.

        Args:
            market: Dictionary containing market data.

        """
        market = deepcopy(market)
        _ = list(self.lazy_price(market))

    def get_asset_prices(self):
        """Return asset prices.

        Returns:
            A pd.Series object containing the asset prices.

        """
        return pd.Series(self.prices)
