"""Create CBOEMarket structure from data read from CBOE EOD files."""
import os
import numpy as np
import pandas as pd
from pandas.tseries.offsets import Day
from pyport.core.cboe_option import CBOEOption, OptionType, calculate_payoff


class CBOEMarket:
    def __init__(self, data):
        index_columns = ['quote_date', 'underlying_symbol', 'root', 'option_type']
        self._data = data
        self._indexed_data = data.set_index(index_columns).sort_index()
        self._quotes_cache = {}
        self._underlying_quotes_cache = {}

    @classmethod
    def from_path(cls, path):
        data = pd.read_csv(path, parse_dates=['quote_date', 'expiration'])
        return CBOEMarket(data)
        
    def find_option(self, date, spot, underlying_symbol, root, option_type, tenor_days, moneyness):
        """
        :param date: datetime object -- quote date
        :param underlying_symbol: str
        :param root: str
        :param option_type: char ('C' or 'P')
        :param tenor_days: int
        :param moneyness: float
        :return: CBOEOPtion
        """
        date = pd.Timestamp(date)
        index = pd.IndexSlice[date, underlying_symbol, root, option_type]
        frame = self._indexed_data.loc[index].reset_index()
        # expiration date
        expiration = self._find_expiry(frame, date, tenor_days)
        frame = frame.loc[frame.expiration == expiration]
        # strike
        strike = self._find_strike(frame, spot * moneyness)
        return CBOEOption(underlying_symbol, root, expiration, option_type, strike)

    def date_range(self):
        return sorted(self._data.quote_date.unique())
        
    def get_quote(self, date, option):
        """
        :param date: datetime object
        :param option: CBOEOption
        :return: tuple (bid_price, ask_price)
        """
        quotes = self._quotes_cache.get(option)
        if quotes is None:
            columns = ['bid_1545', 'ask_1545']
            quotes = (self._find_data(option).set_index('quote_date')[columns]
                      .rename(columns={'bid_1545': 'bid',
                                       'ask_1545': 'ask'}))
            quotes['mid'] = quotes.mean(axis=1)
            self._quotes_cache[option] = quotes
        return quotes.loc[date]

    def get_underlying_quote(self, date, underlying_symbol):
        """
        :param date: datetime object
        :param underlying_symbol: str
        :return: tuple (bid_price, ask_price)
        """
        quotes = self._underlying_quotes_cache.get(underlying_symbol)
        if quotes is None:
            underlying_data = self._data[['quote_date', 'underlying_bid_1545', 'underlying_ask_1545']]
            quotes = (underlying_data.groupby('quote_date').first()
                      .rename(columns={'underlying_bid_1545': 'bid',
                                       'underlying_ask_1545': 'ask'}))
            quotes['mid'] = quotes.mean(axis=1)
        return quotes.loc[date]

    def _find_data(self, cboe_option):
        mask = pd.Series(True, self._data.index)
        for attribute in ['underlying_symbol', 'root', 'expiration', 'option_type', 'strike']:
            if attribute == 'option_type':
                if cboe_option.option_type == OptionType.PUT:
                    mask &= self._data['option_type'] == 'P'
                else:
                    mask &= self._data['option_type'] == 'C'
            else:
                mask &= getattr(self._data, attribute) == getattr(cboe_option, attribute)
        return self._data.loc[mask]

    @staticmethod
    def _find_strike(frame, target_strike):
        closest_index = (frame.strike - target_strike).abs().idxmin()
        return frame.loc[closest_index, 'strike']

    @staticmethod
    def _find_expiry(frame, date, tenor_days):
        date = pd.Timestamp(date)
        target_expiration = date + tenor_days * Day()
        closest_index = (frame.expiration - target_expiration).abs().idxmin()
        return frame.loc[closest_index, 'expiration']
