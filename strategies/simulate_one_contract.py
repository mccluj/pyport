"""Simulate cash-secured pub strategy at different leverages."""
import os
import logging
import numpy as np
import pandas as pd
from pyport.core.cboe_option import CBOEOption, OptionType, calculate_payoff
from pyport.market.cboe import CBOEMarket


path = '~/data/cboe/UnderlyingOptionsEODCalcs.pkl'
# market = CBOEMarket.from_pickle(path)
path = '~/data/cboe/UnderlyingOptionsEODCalcs_2022-08.zip'
market = CBOEMarket.from_csv(path)

config = dict(
    underlying_symbol='^SPX',
    root='SPXW',
    moneyness=1.0,
    option_type='C',
    tenor_days=7,
)

def simulate_strategy(market, config):
    results = pd.DataFrame(0.0, index=pd.Index(market.date_range(), name='Date'),
                           columns=['spot', 'price', 'delta', 'daily_pnl'])
    daily_pnl = 0                   # only needed until the first contract is created.
    contract = None
    for date in market.date_range():
        spot = market.get_underlying_quote(date, config['underlying_symbol'])['mid']
        if contract is not None:
            if date >= contract.expiration:
                contract_payoff = calculate_payoff(contract, spot)
                contract_pnl = contract_payoff - initial_price
                daily_pnl = contract_payoff - previous_price
                logging.debug("%s %.2f: EXP contract_payoff=%.2f daily_pnl=%.2f contract_pnl: %.2f",
                              date.date(), spot, contract_payoff, daily_pnl, contract_pnl)
                contract = None
            else:
                current_price = market.get_quote(date, contract)['ask']
                daily_pnl = current_price - previous_price
        if contract is None:
            contract = market.find_option(date=date, spot=spot, **config)
            initial_price = market.get_quote(date, contract)['bid']
            logging.debug("%s %.2f: ACQ price=%.2f %s",
                          date.date(), spot, initial_price, contract.as_tuple())
            current_price = initial_price
        delta = market.get_delta(date, contract)
        results.loc[date] = (spot, current_price, delta, daily_pnl)
        previous_price = current_price
        print(f'{date} spot={spot:8.2f} price={current_price:8.2f}', flush=True)
    return results


def main():
    results = simulate_strategy(market=market, config=config)
    results.to_csv('simulate_one_contract.csv')
    # print(results)


if __name__ == '__main__':
    log_file = None
    log_file = f"{__file__.split('.')[0]}.log"
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        # format='%(asctime)s - %(levelname)s - %(message)s',
                        format='%(asctime)s - %(message)s',
                        datefmt='%H:%M:%S')
    main()
