"""Market class"""
import os
import numpy as np
import pandas as pd


class Market:
    def __init__(self, config):
        """
        :param config: dict -- data sources, etc
        """
        self.bars = None
        self.volatilities = None
        self.dividends = None
        self.div_rates = None
        self._initialize(config)

    def _initialize(self, config):
        bars = Market.load_stock_bars(config['stocks'])
        self.stock_vols = Market.calculate_volatilities(bars, config['volatilities'])
        self.dividends = Market.calculate_dividends(bars)
        self.stock_div_rates = Market.calculate_div_rates(bars, config.get('div_rates', {}))
        self.stock_bars = bars

    @staticmethod
    def load_stock_bars(config):
        """Read daily bars file for each symbol in config.
        Format:
        Date,open,high,low,close,adj_close,volume
        1993-01-29,43.96875,43.96875,43.75,43.9375,25.029373,1003200
        :config: dict
        :return: dict -- {symbol: pd.DataFrame}
        :note: consider down sampling data for weekly or monthly backtests.
        """
        bar_directory = config['bar_directory']
        bars = {}
        for symbol in config['symbols']:
            path = os.path.join(bar_directory, f'{symbol}.csv')
            bars[symbol] = pd.read_csv(path, index_col=[0], parse_dates=[0])
        return bars

    @staticmethod
    def calculate_volatilities(bars, config):
        """Return historical annualized volatilities.
        :param bars: dict -- {symbol: pd.DataFrame(daily bars)}
        :param config: dict
        :return pd.Series -- annual vols by symbol
        """
        span = config['window']
        field = config.get('price_field', 'Adj Close')
        results = {}
        for symbol, frame in bars.items():
            prices = frame[field]
            daily_vols = prices.pct_change().ewm(span=span).std()
            results[symbol] = daily_vols * np.sqrt(252)
        return pd.Series(results)

    @staticmethod
    def calculate_dividends(bars):
        """Return implied dividends from adjusted and unadjusted closes.
        :param bars: dict -- {symbol: pd.DataFrame(ohlcav)}
        :return: dict -- {symbol: pd.Series)
        """
        dividends = {}
        for symbol, _bars in bars.items():
            tr_prices = _bars.adj_close
            pr_prices = _bars.close
            dividends[symbol] = ((tr_prices.pct_change() - pr_prices.pct_change())
                                 .mul(pr_prices.shift())
                                 .fillna(0))
        return dividends

    @staticmethod
    def calculate_div_rates(bars, config):
        """Return rolling dividend rates. 
        :param bars: dict -- {symbol: pd.DataFrame}
        :param config: dict
        :return: dict -- {symbol: pd.Series)
        """
        window = config['window']
        min_periods = config.get('min_periods', 50)
        div_rates = {}
        for symbol, _bars in bars.items():
            price_returns = _bars.close.pct_change()
            total_returns = _bars.adj_close.pct_change()
            pr_mean = price_returns.rolling(window, min_periods=min_periods).mean()
            tr_mean = total_returns.rolling(window, min_periods=min_periods).mean()
            div_rates[symbol] = 252 * (tr_mean - pr_mean).fillna(0)
        return div_rates

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
