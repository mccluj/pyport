"""Simulate cash-secured pub strategy at different leverages."""
import os
import numpy as np
import pandas as pd
from pyport.core.cboe_option import CBOEOption, OptionType, calculate_payoff
from pyport.market.cboe import CBOEMarket


path = '~/data/cboe/UnderlyingOptionsEODCalcs_2022-08.csv'
market = CBOEMarket.from_path(path)

config = dict(
    underlying_symbol='^SPX',
    root='SPXW',
    moneyness=1.0,
    option_type='C',
    tenor_days=7,
)

contract = None

side = -1
aum = 10000
results = pd.DataFrame(0.0, index=market.date_range(), columns=['spot', 'holdings', 'daily_pnl', 'aum'])
daily_pnl = 0                   # only needed until the first contract is created.
for date in market.date_range():
    spot = market.get_underlying_quote(date, config['underlying_symbol'])['mid']
    if contract is not None:
        if date >= contract.expiration:
            contract_payoff = calculate_payoff(contract, spot)
            daily_pnl = n_contracts * (contract_payoff - previous_price)
            contract = None
        else:
            current_price = market.get_quote(date, contract)['ask']
            daily_pnl = n_contracts * (current_price - previous_price)
    if contract is None:
        contract = market.find_option(date=date, spot=spot, **config)
        current_price = market.get_quote(date, contract)['bid']
        n_contracts = side * np.abs(aum) / current_price
    aum += daily_pnl
    results.loc[date] = (spot, n_contracts, daily_pnl, aum)
    previous_price = current_price

print(results)
