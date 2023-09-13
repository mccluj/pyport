from abc import ABC, abstractmethod

class Asset(ABC):
    """
    Abstract base class for different types of core.
    """

    def __init__(self, symbol):
        """
        Initialize the asset with the given symbol.

        :param symbol: str -- The symbol or identifier of the asset.
        """
        self.symbol = symbol

    @abstractmethod
    def reprice(self, market):
        """
        Calculate and return the asset's calculated values based on the market data.

        :param market: dict -- A dictionary with market pricing elements for a given date.
        :return: CalcValues -- The calculated values of the asset.
        """
        pass

    def unit_reprice(self, **kwargs):
        """
        Calculate and return the asset's calculated values based on the provided parameters.

        :param kwargs: Additional parameters for unit reprice.
        :return: CalcValues -- The calculated values of the asset.
        """
        pass

    def to_string(self):
        """
        Convert the asset to a string representation.

        :return: str -- A one-line summary of the asset.
        """
        return f"{self.symbol}"

class PriceResults:
    """
    Class to store calculated values of an asset.
    """

    def __init__(self):
        pass


