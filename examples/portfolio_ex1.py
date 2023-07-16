"""Create a portfolio of stocks from targets and evaluate with current market values."""
import yaml
import pandas as pd
from pyport import Portfolio

example_string = """
targets:
  AAPL: 100
  MSFT: 50
  SPY: -10

current_market:
  date: 2023-06-23
  prices:
    AAPL: 150
    MSFT:  90
    SPY:  400

portfolio:
  cash: 10000
"""

def main():
    config = yaml.safe_load(example_string)
    current_market = {'date': pd.Timestamp(config['current_market']['date']),
                      'prices': pd.Series(config['current_market']['prices'])}

    target = pd.Series(config['targets'])
    portfolio = Portfolio(cash=config['portfolio']['cash'])
    portfolio.rebalance(current_market, target)
    print(portfolio.to_string())


main()
