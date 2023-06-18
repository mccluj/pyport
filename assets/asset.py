"""Base class for assets"""
from abc import ABC, abstractmethod
import pandas as pd


class Asset(ABC):
    """Asset base class."""
    def __init__(self, name):
        """Core initialization"""
        self.name = name

    @abstractmethod
    def unit_reprice(self, *_args, **_kwargs):
        """Reprice class using kwargs calling parameters"""
        pass

    @abstractmethod
    def reprice(self, market):
        """Reprice class using data found in market object
        :param market: dict
        """

    def initialize(self, market, **_kwargs):
        """Use the market and other parameters to initialize class
        :param market: dict
        """
        self.reprice(market)
        return self

    def compute_accrued_income(self, market, initial_date):
        return 0

    def to_string(self, indent=0):
        padding = ' ' * indent
        _class = type(self).__name__
        return f'{padding}{_class}({self.name}): price={self.price}'


class PricingResult:
    def __init__(self, name, price, date=None, **kwargs):
        self.name = name
        self.price = price
        self.date = date
