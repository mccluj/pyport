from typing import NamedTuple
import pandas as pd

class AssetPricing:
    """Represents the pricing information for a generic asset.

    Attributes:
        name: The name of the asset.
        price: The price of the asset.
        date: The date for which the price is applicable.
    """
    name: str
    price: float
    date: pd.Timestamp

    def __init__(self, name: str, price: float, date: pd.Timestamp) -> None:
        self.name = name
        self.price = price
        self.date = date

class BondPricing(AssetPricing):
    """Represents the pricing information for a bond asset, including bond-specific metrics.

    Attributes:
        metrics: A named tuple containing bond-specific metrics such as duration and convexity.
    """
    metrics: NamedTuple

    def __init__(self, name: str, price: float, date: pd.Timestamp, metrics: NamedTuple) -> None:
        super().__init__(name, price, date)
        self.metrics = metrics

class OptionPricing(AssetPricing):
    """Represents the pricing information for an option asset, including option greeks.

    Attributes:
        greeks: A named tuple containing the option's greeks such as delta and gamma.
    """
    greeks: NamedTuple

    def __init__(self, name: str, price: float, date: pd.Timestamp, greeks: NamedTuple) -> None:
        super().__init__(name, price, date)
        self.greeks = greeks
