"""Simulate cash-secured pub strategy at different leverages."""
import os
import logging
import numpy as np
import pandas as pd
from pyport.core.cboe_option import CBOEOption, OptionType, calculate_payoff
from pyport.market.cboe import CBOEMarket


# path = '~/data/cboe/UnderlyingOptionsEODCalcs.pkl'
# market = CBOEMarket.from_pickle(path)
path = '~/data/cboe/UnderlyingOptionsEODCalcs_2022-08.zip'
market = CBOEMarket.from_csv(path)

config = dict(
    underlying_symbol='^SPX',
    root='SPXW',
    moneyness=1.0,
    option_type='P',
    tenor_days=7,
)
initial_aum = 10000
side = -0.1

def simulate_strategy(market, config, initial_aum, side):
    aum = initial_aum
    results = pd.DataFrame(0.0, index=market.date_range(), columns=['spot', 'holdings', 'daily_pnl', 'aum'])
    daily_pnl = 0                   # only needed until the first contract is created.
    contract = None
    for date in market.date_range():
        spot = market.get_underlying_quote(date, config['underlying_symbol'])['mid']
        if contract is not None:
            if date >= contract.expiration:
                contract_payoff = calculate_payoff(contract, spot)
                contract_pnl = n_contracts * (contract_payoff - initial_price)
                logging.debug("%s: expiration %s %s, pnl: %s",
                              date.date(), f'{spot:.2f}', contract_payoff, daily_pnl)
                daily_pnl = n_contracts * (contract_payoff - previous_price)
                contract = None
            else:
                current_price = market.get_quote(date, contract)['ask']
                daily_pnl = n_contracts * (current_price - previous_price)
        if contract is None:
            contract = market.find_option(date=date, spot=spot, **config)
            initial_price = market.get_quote(date, contract)['bid']
            n_contracts = side * np.abs(aum) / initial_price
            value = n_contracts * initial_price
            logging.debug("%s: rebalance  %s %s = %s @ %s %s",
                          date.date(), f'{spot:.2f}', f'{value:.2f}', f'{n_contracts:.2f}',
                          initial_price, contract.as_tuple())
            current_price = initial_price
        aum += daily_pnl
        results.loc[date] = (spot, n_contracts, daily_pnl, aum)
        previous_price = current_price
    results['underlying_aum'] = 10000 * results['spot'] / results['spot'].iloc[0]
    return results


def compare_leverage_ratios():
    summary = {}
    for side in np.arange(-0.1, 0.01, 0.01):
        key = f'{side:.0%}'
        print(f'leverage: {key}')
        results = simulate_strategy(market, config, initial_aum, side)
        summary[key] = results.aum

    pd.DataFrame(summary).to_csv('short_puts.csv')


def main():
    results = simulate_strategy(market=market, config=config, initial_aum=10000, side=0.10)
    print(results)


if __name__ == '__main__':
    log_file = 'backtest.log'
    log_file = None
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(levelname)s - %(message)s')
                        # format='%(asctime)s - %(levelname)s - %(message)s')
    main()
