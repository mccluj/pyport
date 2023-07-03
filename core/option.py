"""Option class"""
from math import exp, log, sqrt
from scipy.stats import norm
import numpy as np
import pandas as pd
from pyport.core.asset import Asset, AssetPrice


class Option(Asset):
    def __init__(self, underlyer, option_type, expiration, strike):
        self.underlyer = underlyer
        self.option_type = option_type
        self.expiration = pd.Timestamp(expiration)
        self.strike = strike
        name = f'{underlyer}_{self.expiration:%Y%m%d}_{strike:.2f}_{option_type}'
        super().__init__(name)
        
    @staticmethod
    def from_the_market(context, **kwargs):
        """Define option attributes based on current market levels. Alternatives:
        expiration could be computed from market.date + time_delta from tenor frequency.
        strike could be defined as a percent of spot or implied from an given option price.
        :param context: dict -- market, assets, models
        """
        market = context['market']
        option_type = kwargs['option_type']
        underlyer = kwargs['underlyer']
        underlyer_price = market['spot_prices'][underlyer]
        
        if 'expiration' in kwargs:
            expiration = kwargs['expiration']
        elif 'tenor' in kwargs:
            expiration = pd.Timestamp(market['date']) + to_offset(kwargs['tenor'])
        else:
            raise AttributeError('Either expiration or tenor must be specified')
        if 'strike' in kwargs:
            strike = kwargs['strike']
            if isinstance(strike, str):
                if strike[-1] == '%':
                    strike = 0.01 * float(strike[:-1]) * underlyer_price
                else:
                    strike = float(strike)
            elif 'price' in kwargs:
                price = kwargs['price']
                rate = market['rate']
                date = pd.Timestamp(market['date'])
                time_to_expiry = (expiration - date) / pd.Timedelta('365 days')
                div_rate = context['models']['dividend_rate']['underlyer']
                strike = implied_strike(price, underlyer_price, rate, time_to_expiry,
                                        div_rate, option_type)
        return Option(underlyer, option_type, expiration, strike)

    def reprice(self, context):
        market = context['market']
        models = context['models']
        date = market['date']
        underlyler = self.underlyler
        time_to_expiry = (self.expiration - date) / pd.Timestamp('365 days')
        underlyer_price = market['spot_prices'][underlyer]
        div_rate = models.get('div_rates', {}).get(underlyer, 0.0)
        sigma = models['volatilities'][undelyer]
        data = black_scholes(underlyer_price, self.strike, time_to_expiry,
                             sigma, div_rate, self.option_type)
        return AssetPrice(name=self.name, date=date, price=price)
        
    def __eq__(self, other):
        attributes = ['name', 'underlyer', 'option_type', 'expiration', 'strike']
        return all([getattr(self, key) == getattr(other, key) for key in attributes])


class OptionPrice(AssetPrice):
    def __init__(self, name, price, date, **kwargs):
        super().__init__(name, price, date, **kwargs)
        for key in ['delta', 'gamma', 'vega', 'theta', 'rho', 'underlying_price']:
            setattr(self, key, kwargs[key])
        
    def to_string(self):
        
        return_string = f'Option({self.name}, {self.date:%Y-%m-%d}'
        val_strings = [f'{key}: {getatttr(self, key):.4f}'
                       for key in ['delta', 'gamma', 'vega', 'theta', 'rho', 'underlying_price']]
        return_string += ', '.join(val_strings)


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
        option = black_scholes(S, K, r, T, sigma, q, option_type)
        return option['price']

    # Adjust the interval bounds if they are too close
    epsilon = 1e-6
    interval_lower = max(epsilon, S * exp(-q * T) - S * exp(-r * T))
    interval_upper = S * exp(-q * T) + S * exp(-r * T)
    # Use a root-finding algorithm to find the implied strike
    from scipy.optimize import brentq
    implied_strike = brentq(lambda K: black_scholes_strike(K) - price, interval_lower, interval_upper)
    return implied_strike
                
                
def black_scholes(S, K, r, T, sigma, q, option_type):
    """
    Calculates the Black-Scholes option pricing model with Greeks.

    :param S: Current price of the underlying asset.
    :param K: Strike price of the option.
    :param r: Risk-free interest rate.
    :param T: Time to expiration (in years).
    :param sigma: Volatility of the underlying asset.
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
