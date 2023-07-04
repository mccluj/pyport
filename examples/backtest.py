"""Simple Backtest driver to exercise pyport elements."""
import datetime
import yaml
import pandas as pd
import pyport


config_string = """
assets:
  - {type: stock, name: SPY, ticker: SPY}
  - {type: option, ticker: ATM_CALL, underlyer: SPY, option_type: call, moneyness: 1.0, tenor: BM}

backtest:
  dates: {start: 12/31/2021, end: null, frequency: B}

market:
  stock_prices: '~/data/yahoo/prices.csv'
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
        self._stock_prices = None
        self._read_stock_prices(config['stock_prices'])

    def _read_stock_prices(self, filename):
        raw = pd.read_csv(filename, index_col=[0], parse_dates=[0])
        self._stock_prices = raw

    def current(self, date):
        return self._data[date]

class Backtest:
    def __init__(self, config):
        self.dates = None
        self.market = None
        self.assets = None
        self._setup_assets(config)
        self._setup_market_data(config)
        self._setup_backtest(config)

    def _setup_assets(self, config):
        self.assets = {}
        for _dict in config['assets']:
            asset_type = _dict.pop('type')
            _class = getattr(pyport, asset_type.capitalize())
            name = _dict.pop('ticker')
            asset = _class(**_dict)
            self.assets[name] = asset
            
    def _setup_market(self, config):
        self.market = Market(config['market'])

    def _setup_backtest(self, config):
        dates_cfg = config['backtest']['dates']
        self.dates = pd.date_range(start=dates_cfg['start'],
                                   end=dates_cfg.get('end', datetime.now().date()),
                                   frequency=dates_cfg.get('frequency', 'B'))

    def run(self):
        for date in self.dates:
            market.current(date)
            assets.reprice(market)
            portfolio.mark_positions(assets.prices())
            if strategy.check_for_rebalance(context):
                target = strategy.compute_target(context)
                portfolio.rebalance(market, target)


if __name__ == '__main__':
    config = yaml.safe_load(config_string)
    bt = Backtest(config)
