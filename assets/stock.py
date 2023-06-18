"""Stock asset class"""
from pyport import Asset, PricingResult


class Stock(Asset):
    def __init__(self, name):
        super().__init__(name)
        self.price = None

    def unit_reprice(self, spot):
        return PricingResult(self.name, spot)

    def reprice(self, market):
        spot = market['spot_prices'][self.name]
        return self.unit_reprice(spot)

