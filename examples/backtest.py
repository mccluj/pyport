"""Simple Backtest driver to exercise pyport elements."""
from datetime import datetime
import yaml
import pandas as pd
import pyport
import numpy as np

config_string = """
assets:
  SPY: {type: stock, name: SPY}
  SPY_CALL: {type: option, name: SPY_CALL, underlyer: SPY, option_type: call, moneyness: 1.0, tenor: BM}
  SPY_CC: {type: basket, name: SPY_CC, shares: {SPY: 1, SPY_CALL: -1}}
  SPY_PUT: {type: option, name: SPY_PUT, underlyer: SPY, option_type: put, moneyness: 1.0, tenor: BM}

market:
  stocks:
    names: [SPY]
    filename: '~/data/yahoo/prices.csv'
  volatilities:
    vol_window: 65
  dividends:

portfolio:
  initial_cash: 10000

strategy:
  target_template:
    weights:
      SPY_CC: 1.0
    # shares:
    #   SPY_CC: 1.0
  rebalance_rules:
    frequency: BM

backtest:
  # dates: {start: 12/31/2021, end: null, frequency: B}
  dates: {start: 12/31/2021, frequency: B}
"""


class Assets:
    def __init__(self, config):
        self._prices = pd.Series()
        self.assets = config
        
    def reprice(self, date, market):
        """Reprice all assets. For derivatives, inject prices into market
        :param date: date object
        :param market: Market
        """
        print(self.assets)

    def prices(self, symbols=None):
        """Return pd.Series({symbol: price}) for use by others."""
        return self._prices


class Market:
    """Market provides asset prices (from sources and injected from calculations),
    dividend rates, actual dividends, volatilities and interest rates. 
    """
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

    def get_data(self, data_type, attribute, date, symbols=None):
        """Get current attribute values
        :param data_type: str -- 'spot' or 'historical'
        :param attribute: str -- e.g. 'prices', 'dividends'
        :param date: date object -- asof date
        :param symbols: (opt) list(str)
        :return: pd.Series
        """
        data = getattr(self, attribute).loc[:date, symbols]
        if data_type == 'spot':
            return data.iloc[-1]
        else:
            return data

    def get_current(self, date, symbols=None):
        return {'prices': get_data('spot', 'prices', date, symbols),
                'volatilities': get_data('spot', 'volatilities', date, symbols),
                'dividends': get_data('spot', 'dividends', date, symbols),
                'date': date,
                'discount_rates': 0.05}


class Backtest:
    def __init__(self, config):
        self.dates = None
        self.market = None
        self.assets = None
        self.portfolio = None
        self.strategy = None
        self._setup_assets(config)
        self._setup_market(config)
        self._setup_portfolio(config)
        self._setup_strategy(config)
        self._setup_backtest(config)

    def _setup_portfolio(self, config):
        self.portfolio = pyport.Portfolio(cash=config['portfolio']['initial_cash'])

    def _setup_strategy(self, config):
        self.strategy = pyport.Strategy(config=config['strategy'])

    def _setup_assets(self, config):
        self.assets = {}
        for symbol, _dict in config['assets'].items():
            asset_type = _dict.pop('type')
            _class = getattr(pyport, asset_type.capitalize())
            self.assets[symbol] = _class(**_dict)

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
            portfolio.update_mark_prices(self.assets.prices())
            if strategy.check_for_rebalance(context):
                target = strategy.compute_target(context)
                portfolio.rebalance(market, target)


def main():
    config = yaml.safe_load(config_string)
    bt = Backtest(config)
    bt.run()

if __name__ == '__main__':
    main()
