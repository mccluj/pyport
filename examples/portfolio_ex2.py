"""Create a portfolio of stocks and options from targets and evaluate with current market values."""
import yaml
import pandas as pd
from pyport import Portfolio, Option

example_string = """
targets:
  AAPL: 100
  MSFT: 50
  SPY: -10
  SPY_put: -2

current_market:
  date: 2023-06-22
  prices:
    AAPL: 150
    MSFT:  90
    SPY:  400
    SPY_put: 4.0
  volatilities:
    SPY: 0.2
  discount_rates:
    0.05
  div_rates:
    SPY: 0.02

options:
  - [SPY_put, SPY, put, 6/23/2023, 400]

portfolio:
  cash: 10000
"""

def main():
    config = yaml.safe_load(example_string)
    market = config['current_market']
    market['prices'] = pd.Series(market['prices'])
    target = pd.Series(config['targets'])
    # Initial portfolio pricing
    portfolio = Portfolio(cash=config['portfolio']['cash'])
    portfolio.rebalance(market, target)
    print(portfolio.to_string())
    # Update market price for option
    option = Option(*config['options'][0])
    price_data = option.reprice(market)
    market['prices']['SPY_put'] = price_data.price
    portfolio.update_mark_prices(market['prices'])
    print(portfolio.to_string())
    
main()
