"""Simulate cash-secured pub strategy at different leverages.
TODO:
1. write module to compute metrics from results
2. (?) Save cboe pickle file with quote_date as index
3. Run alternate strategies with one market load.
"""
import os
import logging
import numpy as np
import pandas as pd
from pyport.core.cboe_option import CBOEOption, OptionType, calculate_payoff
from pyport.market.cboe_by_date import CBOEMarket


# path = '~/data/cboe/SPX/UnderlyingOptionsEODCalcs_2022-08.zip'
# path = '~/data/cboe/SPX/UnderlyingOptionsEODCalcs.pkl'
# path = '~/data/cboe/SPY/UnderlyingOptionsEODQuotes.pkl'
# path = '~/data/cboe/SPY/UnderlyingOptionsEODQuotes_2022-11.zip'
# market = CBOEMarket.from_csv(path)

SPX_config = dict(
    underlying_symbol='^SPX',
    root='SPXW',
    moneyness=1.0,
    option_type='P',
    tenor_days=7,
)
SPY_config = dict(
    underlying_symbol='SPY',
    root='SPY',
    moneyness=1.0,
    option_type='C',
    tenor_days=7,
)
cboe_config = SPX_config
cboe_config = SPY_config

delta = 0.5
def simulate_strategy(market, config, dates=None):
    contract = None
    if dates is None:
        dates = market.date_range()
    results = pd.DataFrame(0.0, index=pd.Index(dates, name='Date'),
                           columns=['spot', 'price', 'delta', 'daily_pnl', 'option_type', 'expiration', 'strike'])
    daily_pnl = 0                   # only needed until the first contract is created.
    for date in dates:
        market.set_date(date)
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
                # current_price = market.get_quote(date, contract)['ask']
                current_price = market.get_quote(date, contract)['mid']
                daily_pnl = current_price - previous_price
        if contract is None:
            contract = market.find_option(date=date, spot=spot, **config)
            # initial_price = market.get_quote(date, contract)['bid']
            initial_price = market.get_quote(date, contract)['mid']
            logging.debug("%s %.2f: ACQ price=%.2f %s",
                          date.date(), spot, initial_price, contract.as_tuple())
            current_price = initial_price
        # delta = market.get_delta(date, contract)
        results.loc[date] = (spot, current_price, delta, daily_pnl,
                             contract.option_type.value, contract.expiration.date(), contract.strike)
        previous_price = current_price
        print(f'{date} spot={spot:8.2f} price={current_price:8.2f}', flush=True)
    return results


def main():
    date_path = '~/data/cboe/SPY/dates.txt'
    dates = pd.read_csv(date_path, parse_dates=[0], header=None)[0]
    # path = '~/data/cboe/SPY/UnderlyingOptionsEODQuotes_with_option_id.pkl'
    path = '~/data/cboe/SPY/UnderlyingOptionsEODQuotes_with_option_id_and_quote_date_index.pkl'
    print('Setup CBOEMarket')
    market = CBOEMarket.from_pickle(path)
    print('Start simulating')
    results = simulate_strategy(market=market, config=cboe_config, dates=dates)
    results.to_csv('simulate_one_contract.csv')
    # print(results)


if __name__ == '__main__':
    log_file = None
    log_file = f"{__file__.split('.')[0]}.log"
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        filemode='w',
                        # format='%(asctime)s - %(levelname)s - %(message)s',
                        format='%(asctime)s - %(message)s',
                        datefmt='%H:%M:%S')
    main()
