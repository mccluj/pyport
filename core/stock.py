"""Stock asset class"""
import sys
import argparse
import pandas as pd
from pyport import Asset, PricingResult


class Stock(Asset):
    def __init__(self, name):
        super().__init__(name)
        self.price = None

    def unit_reprice(self, spot):
        return spot

    def reprice(self, market):
        spot = market['spot_prices'][self.name]
        price = self.unit_reprice(spot)
        return PricingResult(self.name, price, market['date'])

    def compute_accrued_income(self, market, acquisition_date):
        """Accrue dividends after acquisition date and on or before market date."""
        dividends = market.get('dividends', {}).get(self.name)
        if dividends is not None:
            mask = (dividends.index > acquisition_date) & (dividends.index <= market['date'])
            return dividends.loc[mask].sum()
        else:
            return 0


def parse_args():
    parser = argparse.ArgumentParser(description='Stock Pricing Tool')
    parser.add_argument('-a', '--acquisition', required=True, help='SPY,300,1/1/2021')
    parser.add_argument('-m', '--market', required=True, help='400,1/1/2021')
    parser.add_argument('-d', '--dividends', help='2/1/2021 5,3/1/2021 10')
    return parser.parse_args()

    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage = f'{sys.argv[0]} --market "400,6/30/2021" --acquisition "SPY,300,1/1/2001" --dividends "2/1/2021 5,3/1/2021 10"'
        print(usage)
        sys.exit(1)
        
    args = parse_args()
    tokens = args.acquisition.split(',')
    ticker, acquisition_price, acquisition_date = tokens[0], float(tokens[1]), pd.Timestamp(tokens[2])
    tokens = args.market.split(',')
    price, date = float(tokens[0]), pd.Timestamp(tokens[1])
    tokens = args.dividends.split(',')
    dividends = pd.Series(dtype=float)
    for token in tokens:
        div_tokens = token.split(' ')
        div_date, div_amount = pd.Timestamp(div_tokens[0]), float(div_tokens[1])
        dividends[div_date] = div_amount
    market = {'spot_prices': {ticker: price},
              'date': date,
              'dividends': {ticker: dividends}}

    stock = Stock(ticker).initialize(market)
    print(f'stock: {stock.to_string()}')
    print(f'dividends:\n{dividends}')
    print(f'PriceResult:\n{stock.reprice(market).to_string()}')
    accrued_income = stock.compute_accrued_income(market, acquisition_date)
    print(f'Accrued Income:\n{accrued_income}')
