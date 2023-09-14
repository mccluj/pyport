"""Initialize with CBOE price files and provide interface to data consumers."""
import os
import numpy as np
import pandas as pd
from pandas.tseries.offsets import Day
from pyport.core.cboe_option import CBOEOption, OptionType


class CBOEMarket:
    def __init__(self, data):
        self._data = data
    
    def find_data(self, cboe_option):
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
        
    def find_option(self, date, underlying_symbol, root, option_type, tenor_days, strike):
        """
        :param date: datetime object -- quote date
        :param underlying_symbol: str
        :param root: str
        :param option_type: char ('C' or 'P')
        :param tenor_days: int
        :param strike: float
        :return: CBOEOPtion
        """
        date = pd.Timestamp(date)
        frame = self._data
        # date
        mask = (frame.quote_date == date)
        mask &= (frame.underlying_symbol == underlying_symbol)
        mask &= (frame.root == root)
        mask &= (frame.option_type == option_type)
        frame = frame.loc[mask]
        # expiration date
        expiration = self.find_expiry(frame, date, tenor_days)
        mask &= frame.expiration == expiration
        frame = frame.loc[mask]
        # strike
        strike = self.find_strike(frame, strike)
        mask = (frame.strike == strike)
        frame = frame.loc[mask]
        # option
        n_options = frame.shape[0]
        if n_options == 1:
            return CBOEOption(underlying_symbol, root, expiration, option_type, strike)
        elif n_options == 0:
            raise RuntimeError(f'find_option: No options found')
        else:
            raise RuntimeError(f'find_option: More than one option found')

    @staticmethod
    def find_strike(frame, target_strike):
        closest_index = (frame.strike - target_strike).abs().idxmin()
        return frame.loc[closest_index, 'strike']

    @staticmethod
    def find_expiry(frame, date, tenor_days):
        date = pd.Timestamp(date)
        target_expiration = date + tenor_days * Day()
        closest_index = (frame.expiration - target_expiration).abs().idxmin()
        return frame.loc[closest_index, 'expiration']

    def date_range(self):
        return sorted(self._data.quote_date.unique())


def calculate_payoff(option, underlying_price):
    if option.option_type == OptionType.CALL:
        payoff = np.maximum(0.0, underlying_price - option.strike)
    else:
        payoff = np.maximum(0.0, option.strike - underlying_price)
    return payoff

path = '~/data/cboe/UnderlyingOptionsEODCalcs_2022-08.csv'
option_data = pd.read_csv(path, parse_dates=['quote_date', 'expiration'])
path = os.path.join('~/data/yahoo/spx_bars.csv')
stock_data = pd.read_csv(path, parse_dates=['Date'], index_col=['Date'])
spot_prices = stock_data['close'].round(2)
underlying_symbol='^SPX'
root = 'SPXW'
moneyness = 1.0
option_type = 'C'
tenor_days = 7
market = CBOEMarket(option_data)
contract = None
options = {}
aum = 10000
daily_pnls = pd.Series(0.0, index=market.date_range())
aums = pd.Series(0.0, index=market.date_range())
underlying_data = option_data[['quote_date', 'underlying_bid_1545', 'underlying_ask_1545']]
underlying_prices = underlying_data.groupby('quote_date').first()
underlying_prices['mid_1545'] = underlying_prices.mean(axis=1)
daily_pnl = 0                   # only needed until the first contract is created.
for date in market.date_range():
    if contract is not None:
        if date >= contract.expiration:
            underlying_price = underlying_prices.loc[date, 'mid_1545']
            contract_payoff = calculate_payoff(contract, underlying_price)
            daily_pnl = n_contracts * (contract_payoff - previous_price)
            contract = None
        else:
            current_price = prices.loc[date, 'ask_1545']
            daily_pnl = n_contracts * (current_price - previous_price)
    if contract is None:
        spot = spot_prices[date]
        strike = spot * moneyness
        contract = market.find_option(date=date, underlying_symbol=underlying_symbol, root=root,
                                      option_type=option_type, tenor_days=7, strike=strike)
        prices = market.find_data(contract).set_index('quote_date')[['bid_1545', 'ask_1545', 'underlying_bid_1545', 'underlying_ask_1545']]
        current_price = prices.loc[date, 'bid_1545']
        n_contracts = aum / current_price
        options[date] = contract
        # print(pd.Timestamp(date).date(), contract.as_tuple())
        # print(prices)
    daily_pnls[date] = daily_pnl
    aum += daily_pnl
    aums[date] = aum
    previous_price = current_price
results = pd.concat([underlying_prices.mid_1545, daily_pnls, aums], axis=1, keys=['SPX', 'pnl', 'aum'])

print(results)
