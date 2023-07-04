"""Option class"""
from math import exp, log, sqrt
from scipy.stats import norm
import numpy as np
import pandas as pd
from pandas.tseries.frequencies import to_offset
from pyport.core.asset import Asset, AssetPrice

# TODO: Add moneyness keyword

class Option(Asset):
    def __init__(self, name, underlyer, option_type, expiration=None, strike=None,
                 moneyness=None, tenor=None):
        """
        :param name: str
        :param underlyer: str
        :param option_type: "put" or "call"
        :param strike: float or "implied"
        :param moneyness: float -- decimal percent of spot
        :param expiration: date object
        :param tenor: float(years) or str(pandas freq)
        """
        super().__init__(name)
        self.underlyer = underlyer
        self.option_type = option_type
        if expiration is not None:
            self.expiration = pd.Timestamp(expiration)
        else:
            self.expiration = expiration
        self.strike = strike
        self.moneyness = moneyness
        self.tenor = tenor
        
    def rename(self, name=None):
        if name is None:
            name = f'{self.underlyer}_{self.expiration:%Y%m%d}_{self.strike:.2f}_{self.option_type}'
        super().__init__(name)
        
    def instantiate(self, market, option_price=None):
        """Define option attributes based on current market levels. Alternatives:
        expiration could be computed from market.date + time_delta from tenor frequency.
        strike could be defined as a percent of spot or implied from an given option price.
        :param market: dict
        :param option_price: float -- for computing implied strike
        """
        # Expiration must be done first, in case implied strike needs to be calculated.
        self._instantiate_expiration(market)
        self._instantiate_strike(market, option_price)
        return self

    def _instantiate_expiration(self, market):
        """Compute expiration as market date + tenor
        :param market: dict
        """
        date = pd.Timestamp(market['date'])
        if self.expiration is None:
            if isinstance(self.tenor, (np.float64, float, int)):
                self.expiration = date + pd.Timedelta('365 Days') * self.tenor
            else:
                self.expiration = pd.Timestamp(market['date']) + to_offset(self.tenor)
        
    def _instantiate_strike(self, market, option_price=None):
        """Compute strike as percent of spot or as implied from an option_price.
        :param market: dict
        :param option_price: float -- for computing implied strike
        :return: float -- strike
        """
        strike = self.strike
        spot_price = market['spot_prices'][self.underlyer]
        date = pd.Timestamp(market['date'])
        if strike == 'implied':
            if option_price is None:
                raise ValueError('missing option_price implied strike calculation')
            rate = market['discount_rates']
            div_rate = market.get('div_rates', {}).get(self.underlyer, 0)
            volatility = market['volatilities'][self.underlyer]
            self.strike = implied_strike(option_price, spot_price, rate, self.time_to_expiry(date),
                                         volatility, div_rate, self.option_type)
        elif self.moneyness is not None:
            if isinstance(self.moneyness, (np.float64, float, int)):
                self.strike = spot_price * self.moneyness
            else:
                moneyness = 0.01 * float(self.moneyness[:-1])  # drop '%'
                self.strike = spot_price * moneyness
        elif isinstance(strike, (np.float64, float, int)):
            pass                # strike is unchanged
        else:
            raise ValueError(f'Either strike or moneyness must be specified')

    def time_to_expiry(self, date):
        date = pd.Timestamp(date)
        return (self.expiration - date) / pd.Timedelta('365 days')
        
    def reprice(self, market):
        date = pd.Timestamp(market['date'])
        underlyer = self.underlyer
        spot_price = market['spot_prices'][underlyer]
        discount_rate = market['discount_rates']
        div_rate = market.get('div_rates', {}).get(underlyer, 0.0)
        sigma = market['volatilities'][underlyer]
        data = black_scholes(spot_price, self.strike, self.time_to_expiry(date),
                             sigma, discount_rate, div_rate, self.option_type)
        data['und_price'] = spot_price
        return OptionPrice(name=self.name, date=date, **data)
        
    def __eq__(self, other):
        attributes = ['name', 'underlyer', 'option_type', 'expiration', 'strike']
        return all([getattr(self, key) == getattr(other, key) for key in attributes])

    def to_string(self, indent=0):
        return f'{self.underlyer}_{self.expiration:%Y%m%d}_{self.strike:.2f}_{self.option_type}'
        

class OptionPrice(AssetPrice):
    def __init__(self, name, date, **kwargs):
        super().__init__(name, date, **kwargs)
        for key in ['delta', 'gamma', 'vega', 'theta', 'rho', 'und_price']:
            setattr(self, key, kwargs[key])
        
    def to_string(self, delim=', '):
        core_string = f'{self.name}: '
        date_string = f'date: {self.date:%Y-%m-%d}, '
        val_strings = [f'{key}: {getattr(self, key):.2f}'
                       for key in ['price', 'delta', 'gamma', 'vega', 'theta', 'rho', 'und_price']]
        return core_string + date_string + delim.join(val_strings)


def implied_strike(price, S, r, T, sigma, q, option_type):
    """
    Computes an option's implied strike given its option price using the Black-Scholes formula.

    :param price: Option price.
    :param S: Current price of the underlying asset.
    :param r: Risk-free interest rate.
    :param T: Time to expiration (in years).
    :param sigma: Volatility of the underlying asset.
    :param q: Dividend rate of the underlying asset.
    :param option_type: Type of the option, either 'call' or 'put'.

    :return: Implied strike price.
    """
    def black_scholes_strike(K):
        option = black_scholes(S, K, T, sigma, r, q, option_type)
        return option['price']

    # Adjust the interval bounds if they are too close
    epsilon = 1e-6
    interval_lower = max(epsilon, S * exp(-q * T) - S * exp(-r * T))
    interval_upper = S * exp(-q * T) + S * exp(-r * T)
    # Use a root-finding algorithm to find the implied strike
    from scipy.optimize import brentq
    implied_strike = brentq(lambda K: black_scholes_strike(K) - price, interval_lower, interval_upper)
    return implied_strike
                
                
def black_scholes(S, K, T, sigma, r, q, option_type):
    """
    Calculates the Black-Scholes option pricing model with Greeks.

    :param S: Current price of the underlying asset.
    :param K: Strike price of the option.
    :param T: Time to expiration (in years).
    :param sigma: Volatility of the underlying asset.
    :param r: Risk-free interest rate.
    :param q: Dividend rate of the underlying asset.
    :param option_type: Type of the option, either 'call' or 'put'.

    :return: A dictionary containing the option price and Greeks (delta, gamma, vega, theta, and rho).
    """
    d1 = (log(S / K) + (r - q + (sigma ** 2) / 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    if option_type == 'call':
        price = S * exp(-q * T) * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
        delta = exp(-q * T) * norm.cdf(d1)
        theta = (-S * sigma * exp(-q * T) * norm.pdf(d1)) / (2 * sqrt(T)) - r * K * exp(-r * T) * norm.cdf(d2) + q * S * exp(-q * T) * norm.cdf(d1)
    elif option_type == 'put':
        price = K * exp(-r * T) * norm.cdf(-d2) - S * exp(-q * T) * norm.cdf(-d1)
        delta = -exp(-q * T) * norm.cdf(-d1)
        theta = (-S * sigma * exp(-q * T) * norm.pdf(d1)) / (2 * sqrt(T)) + r * K * exp(-r * T) * norm.cdf(-d2) - q * S * exp(-q * T) * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option_type. Must be either 'call' or 'put'.")

    gamma = exp(-q * T) * norm.pdf(d1) / (S * sigma * sqrt(T))
    vega = S * exp(-q * T) * norm.pdf(d1) * sqrt(T)
    rho = K * T * exp(-r * T) * norm.cdf(d2) if option_type == 'call' else -K * T * exp(-r * T) * norm.cdf(-d2)

    return {
        'price': price,
        'delta': delta,
        'gamma': gamma,
        'vega': vega,
        'theta': theta,
        'rho': rho
    }
