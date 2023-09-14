"""Simulate cash-secured pub strategy at different leverages."""
import os
import numpy as np
import pandas as pd
from pyport.core.cboe_option import CBOEOption, OptionType, calculate_payoff
from pyport.market.cboe import CBOEMarket


path = '~/data/cboe/UnderlyingOptionsEODCalcs_2022-08.csv'
market = CBOEMarket.from_path(path)

underlying_symbol='^SPX'
root = 'SPXW'
moneyness = 1.0
option_type = 'C'
tenor_days = 7
side = -1
contract = None

aum = 10000
daily_pnls = pd.Series(0.0, index=market.date_range())
aums = pd.Series(0.0, index=market.date_range())
holdings = pd.Series(0.0, index=market.date_range())
spot_prices = pd.Series(0.0, index=market.date_range())
daily_pnl = 0                   # only needed until the first contract is created.
for date in market.date_range():
    if contract is not None:
        if date >= contract.expiration:
            spot = market.get_underlying_quote(date, underlying_symbol)['mid']
            contract_payoff = calculate_payoff(contract, spot)
            daily_pnl = n_contracts * (contract_payoff - previous_price)
            contract = None
        else:
            current_price = market.get_quote(date, contract)['ask']
            daily_pnl = n_contracts * (current_price - previous_price)
    if contract is None:
        spot = market.get_underlying_quote(date, underlying_symbol)['mid']
        strike = spot * moneyness
        contract = market.find_option(date=date, underlying_symbol=underlying_symbol, root=root,
                                      option_type=option_type, tenor_days=7, strike=strike)
        current_price = market.get_quote(date, contract)['bid']
        n_contracts = side * np.abs(aum) / current_price
    daily_pnls[date] = daily_pnl
    aum += daily_pnl
    aums[date] = aum
    holdings[date] = n_contracts
    spot_prices[date] = spot
    previous_price = current_price
results = pd.concat([spot_prices, holdings, daily_pnls, aums], axis=1, keys=['SPX', 'holdings', 'pnl', 'aum'])

print(results)
