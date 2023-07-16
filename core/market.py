"""
market.py - A module implementing the Market class for managing market data and calculations.

The Market class provides methods to load stock bars, calculate volatilities, calculate dividends, and calculate dividend rates.
It also allows accessing current market data, such as prices, volatilities, dividends, and discount rates.

The module relies on the pandas and numpy libraries for data manipulation and calculations.

Author: John McClure
Date: July 2023
"""

import os
import numpy as np
import pandas as pd


class Market:
    """
    The Market class represents a market containing stock data and calculations.

    Attributes:
        bars (None): Placeholder for stock bars.
        volatilities (None): Placeholder for stock volatilities.
        dividends (None): Placeholder for stock dividends.
        div_rates (None): Placeholder for stock dividend rates.

    Methods:
        __init__(config): Initialize the Market object with the given configuration.
        _initialize(config): Internal method to initialize the market object based on the configuration.
        load_stock_bars(config): Load daily bars file for each symbol in the configuration.
        calculate_volatilities(bars, config): Calculate historical annualized volatilities.
        calculate_dividends(bars): Calculate implied dividends from adjusted and unadjusted closes.
        calculate_div_rates(bars, config): Calculate rolling dividend rates.
        get_data(data_type, attribute, date, symbols): Get current attribute values for a given date and symbols.
        get_current(date, symbols): Get current market data for a given date and symbols.
    """

    def __init__(self, config):
        """
        Initialize the Market object.

        :param config: dict - Configuration containing data sources, etc.
        """
        self.bars = None
        self.volatilities = None
        self.dividends = None
        self.div_rates = None
        self._initialize(config)

    def _initialize(self, config):
        """
        Initialize the market object based on the configuration.

        :param config: dict - Configuration containing data sources, etc.
        :return: None
        """
        bars = Market.load_stock_bars(config['stocks'])
        self.stock_vols = Market.calculate_volatilities(bars, config['volatilities'])
        self.dividends = Market.calculate_dividends(bars)
        self.stock_div_rates = Market.calculate_div_rates(bars, config.get('div_rates', {}))
        self.stock_bars = bars

    @staticmethod
    def load_stock_bars(config):
        """
        Read daily bars file for each symbol in the configuration.

        Format:
        Date,open,high,low,close,adj_close,volume
        1993-01-29,43.96875,43.96875,43.75,43.9375,25.029373,1003200

        :param config: dict - Configuration containing bar directory and symbols.
        :return: dict - Dictionary of symbol dataframes {symbol: pd.DataFrame}.
        """
        bar_directory = config['bar_directory']
        bars = {}
        for symbol in config['symbols']:
            path = os.path.join(bar_directory, f'{symbol}.csv')
            bars[symbol] = pd.read_csv(path, index_col=[0], parse_dates=[0])
        return bars

    @staticmethod
    def calculate_volatilities(bars, config):
        """
        Calculate historical annualized volatilities.

        :param bars: dict - Dictionary of symbol dataframes {symbol: pd.DataFrame}.
        :param config: dict - Configuration containing window size and price field.
        :return: pd.Series - Annual volatilities by symbol.
        """
        span = config['window']
        field = config.get('price_field', 'Adj Close')
        results = {}
        for symbol, frame in bars.items():
            prices = frame[field]
            daily_vols = prices.pct_change().ewm(span=span).std()
            results[symbol] = daily_vols * np.sqrt(252)
        return pd.Series(results)

    @staticmethod
    def calculate_dividends(bars):
        """
        Calculate implied dividends from adjusted and unadjusted closes.

        :param bars: dict - Dictionary of symbol dataframes {symbol: pd.DataFrame}.
        :return: dict - Dictionary of symbol dividend series {symbol: pd.Series}.
        """
        dividends = {}
        for symbol, _bars in bars.items():
            tr_prices = _bars.adj_close
            pr_prices = _bars.close
            dividends[symbol] = ((tr_prices.pct_change() - pr_prices.pct_change())
                                 .mul(pr_prices.shift())
                                 .fillna(0))
        return dividends

    @staticmethod
    def calculate_div_rates(bars, config):
        """
        Calculate rolling dividend rates.

        :param bars: dict - Dictionary of symbol dataframes {symbol: pd.DataFrame}.
        :param config: dict - Configuration containing window size and minimum periods.
        :return: dict - Dictionary of symbol dividend rate series {symbol: pd.Series}.
        """
        window = config['window']
        min_periods = config.get('min_periods', 50)
        div_rates = {}
        for symbol, _bars in bars.items():
            price_returns = _bars.close.pct_change()
            total_returns = _bars.adj_close.pct_change()
            pr_mean = price_returns.rolling(window, min_periods=min_periods).mean()
            tr_mean = total_returns.rolling(window, min_periods=min_periods).mean()
            div_rates[symbol] = 252 * (tr_mean - pr_mean).fillna(0)
        return div_rates

    def get_data(self, data_type, attribute, date, symbols=None):
        """
        Get current attribute values.

        :param data_type: str - 'spot' or 'historical'.
        :param attribute: str - Attribute to retrieve (e.g., 'prices', 'dividends').
        :param date: date object - As-of date.
        :param symbols: list(str) - Optional list of symbols.
        :return: pd.Series - Attribute values.
        """
        data = getattr(self, attribute).loc[:date, symbols]
        if data_type == 'spot':
            return data.iloc[-1]
        else:
            return data

    def get_current(self, date, symbols=None):
        """
        Get current market data.

        :param date: date object - As-of date.
        :param symbols: list(str) - Optional list of symbols.
        :return: dict - Dictionary of current market data.
        """
        return {
            'prices': self.get_data('spot', 'prices', date, symbols),
            'volatilities': self.get_data('spot', 'volatilities', date, symbols),
            'dividends': self.get_data('spot', 'dividends', date, symbols),
            'date': date,
            'discount_rates': 0.05
        }
