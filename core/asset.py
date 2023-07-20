"""Base class for assets"""
from abc import ABC, abstractmethod
import pandas as pd


class Asset(ABC):
    """Asset base class."""
    def __init__(self, name, dependencies):
        """For Asset, store asset name and dependencies on other assets. These
        dependencies are used by AssetManager for lazy evaluation of asset prices.
        :param name: str
        :param dependencies: list(str)
        """
        self.name = name
        self.dependencies = dependencies

    @abstractmethod
    def reprice(self, market) -> None:
        """Reprice class using data found in market object
        :param market: dict
        """

    def compute_accrued_income(self, market, initial_date):
        return 0

    def to_string(self, indent=0):
        padding = ' ' * indent
        _class = type(self).__name__
        return f'{padding}{_class}({self.name})'


class AssetPrice:
    def __init__(self, name, date, price, **kwargs):
        self.name = name
        self.date = pd.Timestamp(date)
        self.price = price

    def to_string(self, delim=None):
        return f'Asset({self.name}, {self.date:%Y-%m-%d}, {self.price})'
