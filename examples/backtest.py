"""Simple Backtest driver to exercise pyport elements."""
from datetime import datetime
import yaml
import pandas as pd
import pyport
import numpy as np

config_string = """
assets:
  - {type: stock, name: SPY}
  - {type: option, name: SPY_CALL, underlyer: SPY, option_type: call, moneyness: 1.0, tenor: BM}

backtest:
  # dates: {start: 12/31/2021, end: null, frequency: B}
  dates: {start: 12/31/2021, frequency: B}

market:
  stocks:
    names: [SPY]
    filename: '~/data/yahoo/prices.csv'
  volatilities:
    vol_window: 65
  dividends:
"""


class Assets:
    def __init__(self, config):
        self._prices = pd.Series()
        self.config = config

    def reprice(self, date, market):
        """Reprice derivatives and combine with stock prices"""

    def prices(self):
        return self._prices

class Market:
    def __init__(self, config):
        self.prices = None
        self.volatilities = None
        self._read_stock_data(config['stocks'])
        self._calc_volatilities(config['volatilities'])
        self._calc_dividends(config['dividends'])

    def _read_stock_data(self, config):
        raw = (pd.read_csv(config['filename'], index_col=[0], parse_dates=[0])
               .loc[:, config['names']])           
        self.prices = raw.dropna()

    def _calc_volatilities(self, config):
        daily_volatilities = self.prices.pct_change().ewm(span=config['vol_window']).std()
        self.volatilities = daily_volatilities * np.sqrt(252)
        
    def _calc_dividends(self, config):
        self.dividends = 0 * self.prices
        
    def current(self, date):
        _dict = {'prices': self.prices.loc[:date].iloc[-1],
                 'volatilities': self.volatilities.loc[:date].iloc[-1],
                 'date': date,
                 'discount_rates': 0.05,
                 'div_rates': self.dividends.loc[:date].iloc[-1]}
        return _dict

class Backtest:
    def __init__(self, config):
        self.dates = None
        self.market = None
        self.assets = None
        self._setup_assets(config)
        self._setup_market(config)
        self._setup_backtest(config)

    def _setup_assets(self, config):
        self.assets = {}
        for _dict in config['assets']:
            asset_type = _dict.pop('type')
            _class = getattr(pyport, asset_type.capitalize())
            asset = _class(**_dict)
            name = _dict['name']
            self.assets[name] = asset
            
    def _setup_market(self, config):
        self.market = Market(config['market'])

    def _setup_backtest(self, config):
        dates_cfg = config['backtest']['dates']
        self.dates = pd.date_range(start=dates_cfg['start'],
                                   end=dates_cfg.get('end', datetime.now().date()),
                                   freq=dates_cfg.get('frequency', 'B'))

    def run(self):
        for date in self.dates:
            market = self.market.current(date)
            self.assets.reprice(market)
            portfolio.mark_positions(self.assets.prices())
            if strategy.check_for_rebalance(context):
                target = strategy.compute_target(context)
                portfolio.rebalance(market, target)


if __name__ == '__main__':
    config = yaml.safe_load(config_string)
    bt = Backtest(config)
    bt.run()
