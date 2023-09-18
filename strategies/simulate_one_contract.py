"""Simulate cash-secured pub strategy at different leverages."""
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
    option_type='P',
    tenor_days=7,
)
cboe_config = SPX_config
cboe_config = SPY_config

delta = 0.5
def simulate_strategy(market, config):
    contract = None
    dates = market.date_range()
    results = pd.DataFrame(0.0, index=pd.Index(dates, name='Date'),
                           columns=['spot', 'price', 'delta', 'daily_pnl'])
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
                current_price = market.get_quote(date, contract)['ask']
                daily_pnl = current_price - previous_price
        if contract is None:
            contract = market.find_option(date=date, spot=spot, **config)
            initial_price = market.get_quote(date, contract)['bid']
            logging.debug("%s %.2f: ACQ price=%.2f %s",
                          date.date(), spot, initial_price, contract.as_tuple())
            current_price = initial_price
        # delta = market.get_delta(date, contract)
        results.loc[date] = (spot, current_price, delta, daily_pnl)
        previous_price = current_price
        print(f'{date} spot={spot:8.2f} price={current_price:8.2f}', flush=True)
    return results


def main():
    path = '~/data/cboe/SPY/UnderlyingOptionsEODQuotes_with_option_id.pkl'
    print('Setup CBOEMarket')
    market = CBOEMarket.from_pickle(path)
    print('Start simulating')
    results = simulate_strategy(market=market, config=cboe_config)
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
