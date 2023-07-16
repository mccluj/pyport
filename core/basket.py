"""Basket of assets (possibly nested)"""
import pandas as pd
from pyport.core.asset import Asset, AssetPrice


class Basket(Asset):
    def __init__(self, name, shares):
        """
        :param name: str
        :param shares: pd.Series
        """
        super().__init__(name)
        self.shares = shares

    @classmethod
    def instantiate_from_market(cls, market, name, **kwargs):
        """Instantiate a basket from either weights or shares using market data.
        If weights are used, a basket target value must be provided. Note if both
        weights and shares are provided, shares takes precedence.
        :param market: dict
        :param name: str
        :param shares: pd.Series (Optional)
        :param weights: pd.Series (Optional)
        :param target_value: float (Optional)
        :return: Option instance
        """
        if kwargs.get('shares') is not None:
            shares = kwargs['shares']
        elif kwargs.get('weights') is not None:
            weights = kwargs['weights']
            if 'target_value' not in kwargs:
                raise ValueError("If 'weights' is specified, a 'target_value' is required")
            target_value = kwargs['target_value']
            prices = market['prices']
            shares = target_value * weights / prices
        else:
            raise ValueError("Either 'shares' or 'weights' must be provided")
        return Basket(name, shares)

    def reprice(self, market):
        assets = market.assets.reindex(allocations.index)
        asset_prices = assets.apply(lambda asset: asset.reprice(market).price)
        price = self.shares @ assets_prices
        return BasketPrice(self.name, market['date'], price)



class BasketPrice(AssetPrice):
    def __init__(self, name, date, price, asset_prices, shares):
        pass
