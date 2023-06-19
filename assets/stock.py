"""Stock asset class"""
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


