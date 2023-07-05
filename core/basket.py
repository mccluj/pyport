"""Basket of assets (possibly nested)"""
import pandas as pd
from pyport.core.asset import Asset, AssetPrice


class Basket(Asset):
    def __init__(self, name, shares=None, weights=None, aum=None):
        super().__init__(name)
        self.shares = shares
        self.weights = weights
        self.aum = aum

    def instantiate(self, market):
        if self.shares is None:
            if (self.aum is not None) and (self.weights is not None):
                allocations = self.aum * self.weights
                assets = market['assets'].reindex(allocations.index)
                prices = assets.apply(lambda asset: asset.reprice(market).price)
                self.shares = allocations / prices
        return self

    def reprice(self, market):
        assets = market.assets.reindex(allocations.index)
        asset_prices = assets.apply(lambda asset: asset.reprice(market).price)
        price = self.shares @ assets_prices
        return AssetPrice(self.name, market['date'], price)

