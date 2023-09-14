"""Simulate cash-secured pub strategy at different leverages."""
import os
import numpy as np
import pandas as pd
from pyport.core.cboe_option import CBOEOption, OptionType, calculate_payoff
from pyport.market.cboe import CBOEMarket


path = '~/data/cboe/UnderlyingOptionsEODCalcs_2022-08.csv'
option_data = pd.read_csv(path, parse_dates=['quote_date', 'expiration'])
path = os.path.join('~/data/yahoo/spx_bars.csv')
underlying_symbol='^SPX'
root = 'SPXW'
moneyness = 1.0
option_type = 'C'
tenor_days = 7
side = -1
market = CBOEMarket(option_data)
contract = None
options = {}
aum = 10000
daily_pnls = pd.Series(0.0, index=market.date_range())
aums = pd.Series(0.0, index=market.date_range())
holdings = pd.Series(0.0, index=market.date_range())
underlying_data = option_data[['quote_date', 'underlying_bid_1545', 'underlying_ask_1545']]
underlying_prices = underlying_data.groupby('quote_date').first()
spot_prices = underlying_prices.mean(axis=1)
daily_pnl = 0                   # only needed until the first contract is created.
for date in market.date_range():
    if contract is not None:
        if date >= contract.expiration:
            underlying_price = spot_prices[date]
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
        n_contracts = side * np.abs(aum) / current_price
        options[date] = contract
        # print(pd.Timestamp(date).date(), contract.as_tuple())
        # print(prices)
    daily_pnls[date] = daily_pnl
    aum += daily_pnl
    aums[date] = aum
    holdings[date] = n_contracts
    previous_price = current_price
results = pd.concat([spot_prices, holdings, daily_pnls, aums], axis=1, keys=['SPX', 'holdings', 'pnl', 'aum'])

print(results)
