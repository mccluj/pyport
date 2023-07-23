"""
portfolio.py - A module implementing a Portfolio class for managing financial portfolios.

The Portfolio class represents a portfolio of assets with a single position per stock, and it keeps
track of all transactions. It provides methods for rebalancing the portfolio, adding dividends to
the cash balance, and evaluating the total assets under management (AUM).

The module relies on the pandas library for data manipulation.

Example usage:
    # Create a portfolio with an initial cash balance
    portfolio = Portfolio(100000)

    # Rebalance the portfolio based on target shares
    market_info = {'date': '2023-07-16', 'prices': {'AAPL': 150.0, 'GOOGL': 2500.0, 'MSFT': 300.0}}
    target_shares = pd.Series({'AAPL': 100, 'GOOGL': 50, 'MSFT': 75})
    portfolio.rebalance(market_info, target_shares)

    # Add dividends to the cash balance
    dividends = pd.Series({'AAPL': 500, 'GOOGL': 200, 'MSFT': 300})
    portfolio.add_dividends_to_cash(dividends)

    # Calculate the total assets under management (AUM)
    aum = portfolio.aum

Author: John McClure
Date: July 2023
"""
import pandas as pd


class Portfolio:
    """

    Class representing a portfolio of assets with one position per asset and all trades saved.

    Attributes:
        cash (float): The initial cash balance of the portfolio.
        positions (pd.Series): Series containing the positions or shares held for each asset.
        prices (pd.Series): Series containing the market prices used to evaluate the positions.
        trades (pd.DataFrame): DataFrame storing the executed trades.

    Methods:
        rebalance(market, target): Rebalance the portfolio positions and cash balance from the target shares.
        add_dividends_to_cash(dividends): Update the internal cash balance with dividends paid on asset positions.
        mark_positions(prices): Update the prices used to evaluate positions.
        to_string(): Convert the Portfolio object to a string representation.
        check_for_missing_prices(series, prices): Check for missing prices in the given series and prices.
        aum(): Calculate the total assets under management (AUM) of the portfolio.
    """

    def __init__(self, cash):
        """
        Initialize the Portfolio object.

        :param cash: float - The initial cash balance of the portfolio.
        """
        self.cash = cash
        self.positions = pd.Series(dtype=float)
        self.prices = pd.Series(dtype=float)
        self.trades = pd.DataFrame()

    def rebalance(self, market, target_shares):
        """
        Rebalance the portfolio positions based on the target shares and update the cash balance.

        :param market: dict - Contains the market information including the date and prices.
        :param target_shares: pd.Series - Target shares by asset.
        :return: None
        """
        market_prices = market['prices']
        trade_shares = target_shares.sub(self.positions, fill_value=0)
        trade_prices = Portfolio.check_for_missing_prices(trade_shares, market_prices)
        self.trades = pd.DataFrame({'shares': trade_shares, 'prices': trade_prices})
        self.positions = target_shares.copy()
        self.cash -= self.trades.shares @ self.trades.prices
        self.mark_positions(market_prices)

    def add_dividends_to_cash(self, dividends):
        """
        Update the internal cash balance with dividends paid on asset positions.

        :param dividends: pd.Series - Dividends paid on asset positions.
        :return: None
        """
        dividend_value = dividends.mul(self.positions, fill_value=0).sum()
        self.cash += dividend_value

    def mark_positions(self, prices):
        """
        Update the prices used to evaluate positions.

        :param prices: pd.Series - Market prices.
        :return: None
        """
        self.prices = Portfolio.check_for_missing_prices(self.positions, prices)

    def to_string(self):
        """
        Convert the Portfolio object to a string representation.

        Portfolio(cash=-5500.0, aum=10000.0):
        positions:
              position  price
        AAPL       100    150
        MSFT        50     90
        SPY        -10    400

        :return: str - String representation of the Portfolio object.
        """
        positions = pd.DataFrame({'position': self.positions, 'price': self.prices})
        return f'Portfolio(cash={self.cash}, aum={self.aum}):\npositions:\n{positions}'

    @staticmethod
    def check_for_missing_prices(series, prices):
        """
        Check for missing prices in the given series and prices.

        :param series: pd.Series - Series of positions or shares.
        :param prices: pd.Series - Market prices.
        :return: pd.Series - Prices with missing values filled.
        :raises ValueError: If there are missing prices for any of the assets.
        """
        prices = prices.reindex(series.index)
        missing = prices[prices.isna()].index.to_list()
        if len(missing) > 0:
            raise ValueError(f'Missing prices for {missing}')
        return prices

    @property
    def aum(self):
        """
        Calculate the total assets under management (AUM) of the portfolio.

        :return: float - Total AUM of the portfolio.
        """
        return self.cash + self.positions @ self.prices


def usage_example():
    # Initial portfolio

    portfolio = Portfolio(cash=10000)
    print(portfolio.to_string())

    # Add a target
    
    market = {
        'date': '1/1/2023',
        'prices': pd.Series({'stock': 100, 'option': 5, 'basket': 95}),
    }
    target = pd.Series(dict(stock=50, option=-25, basket=10))
    portfolio.rebalance(market, target)
    print(portfolio.to_string())

    # Remark positions
    
    market = {
        'date': '2/1/2023',
        'prices': pd.Series({'stock': 110, 'option': 7, 'basket': 90}),
    }
    portfolio.mark_positions(market['prices'])
    print(portfolio.to_string())
    
    # add dividend payments

    portfolio.add_dividends_to_cash(pd.Series({'stock': 3}))
    print(portfolio.to_string())

    
if __name__ == '__main__':
    usage_example()
