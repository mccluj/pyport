"""
Holding class. Unless needed it will not be tailored to asset type.
For now it will not inherit from Asset.
For now it has no unit_reprice. I assume pricing with no market context makes no sense.
"""
import sys
import argparse
import re
import pandas as pd
# from pprint import pprint
import pprint


class Holding:
    def __init__(self, asset, acquisition_date, acquisition_price, quantity):
        self.asset = asset
        self.acquisition_date = pd.Timestamp(acquisition_date)
        self.acquisition_price = acquisition_price
        self.quantity = quantity
        self.valuation = None

    def get_current_valuation(self, market):
        """Update valuation on this holding."""
        accrued_income = self.asset.compute_accrued_income(market, self.acquisition_date)
        price = self.asset.reprice(market).price
        self.valuation = HoldingValuation(market['date'], price, accrued_income, self.quantity)
        

    def to_string(self, indent=0):
        attributes = [f'asset: {self.asset.to_string(indent)}',
                      f'acquisition_date: {self.acquisition_date}',
                      f'acquisition_price: {self.acquisition_price}',
                      f'quantity: {self.quantity}',
                      ]
        if self.valuation is not None:
            attributes.append(f'valuation:\n{self.valuation.to_string()}')
        else:
            attributes.append(f'valuation:\n{self.valuation}')
        return '\n'.join(attributes)

        
class HoldingValuation:
    def __init__(self, date, asset_price, asset_income, quantity):
        self.date = pd.Timestamp(date)
        self.asset_price = asset_price
        self.asset_income = asset_income
        self.holding_income = quantity * asset_income
        self.holding_value = quantity * (asset_price + asset_income)
                                     
    def __eq__(self, other):
        return ((self.date == other.date) &
                (self.asset_price == other.asset_price) &
                (self.asset_income == other.asset_income) &
                (self.holding_income == other.holding_income) &
                (self.holding_value == other.holding_value))

    def to_string(self):
        return pprint.pformat(self.__dict__)


def parse_args():
    parser = argparse.ArgumentParser(description='Stock Pricing Tool')
    parser.add_argument('-a', '--acquisition', help='SPY,300,1/1/2021')
    parser.add_argument('-m', '--market', help='400,1/1/2021')
    parser.add_argument('-d', '--dividends', help='2/1/2021 5,3/1/2021 10')
    parser.add_argument('-x', '--example', action='store_true', help='Example setup of Holding')
    args = parser.parse_args()
    if args.example:
        example = ['--market', "400,6/30/2021",
                   '--acquisition', "SPY,300,1/1/2001",
                   '--dividends', "2/1/2021 5,3/1/2021 10"]
        args = parser.parse_args(example)
    return args
    
if __name__ == '__main__':
    from pyport import Stock

    if len(sys.argv) < 2:
        usage = '--market "400,6/30/2021" --acquisition "SPY,300,1/1/2001" --dividends "2/1/2021 5,3/1/2021 10"'
        print(f'{sys.argv[0]} {usage}'
        sys.exit(1)
    args = parse_args()
    print(args)
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

    stock = Stock(ticker)
    accrued_income = stock.compute_accrued_income(market, acquisition_date)
    holding = Holding(stock, acquisition_date, acquisition_price, 10)
    print(holding.to_string())
    holding.get_current_valuation(market)
    print(holding.to_string())
    