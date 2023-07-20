"""
option.py - A module implementing the Option class and related functions for option pricing and calculations.

The Option class represents an option contract and inherits from the Asset class.
It provides methods to instantiate option attributes based on market levels, calculate expiration and strike,
reprice the option based on current market data, and compare options for equality.

The module also includes the OptionPrice class that inherits from the AssetPrice class.
It represents the price of an option at a specific date and provides methods for string representation.

The module includes the following functions:
- implied_strike(price, S, r, T, sigma, q, option_type): Computes an option's implied strike given its option price.
- black_scholes(S, K, T, sigma, r, q, option_type): Calculates the Black-Scholes option pricing model with Greeks.

Author: John McClure
Date: July 2023
"""

from math import exp, log, sqrt
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
import pandas as pd
from pandas.tseries.frequencies import to_offset
from pyport.core.asset import Asset, AssetPrice


class Option(Asset):
    """
    The Option class represents an option contract.

    Attributes:
        underlyer (str): Underlying asset of the option.
        option_type (str): Option type, either "put" or "call".
        expiration (pd.Timestamp or None): Expiration date of the option.
        strike (float or "implied"): Strike price of the option.
        identifier: string representation of the option. 
    """

    def __init__(self, name, underlyer, option_type, expiration, strike):
        """
        Initialize the Option object.

        :param name: str - Name of the option.
        :param underlyer: str - Underlying asset of the option.
        :param option_type: str - "put" or "call".
        :param expiration: date
        :param strike: float
        """
        super().__init__(name, [underlyer])
        self.underlyer = underlyer
        self.option_type = option_type
        self.strike = strike
        self.expiration = pd.Timestamp(expiration)
        try:
            self.identifier = f'{self.underlyer}_{self.expiration:%Y%m%d}_{self.strike:.2f}_{self.option_type}'
        except:
            self.identifier = None
            
    def rename(self, name):
        """
        Rename the Option object.

        :param name: str - New name for the option.
        :return: None
        """
        super().__init__(name, [self.underlyer])

    @classmethod
    def from_market(cls, market, name, **kwargs):
        underlyer = kwargs['underlyer']
        option_type = kwargs['option_type']
        expiration = Option._calculate_expiration(market, **kwargs)
        candidate = Option(name, underlyer, option_type, expiration, None)
        strike = Option._calculate_strike(market, candidate=candidate, **kwargs)
        return Option(name, underlyer, option_type, expiration, strike)

    @staticmethod
    def _calculate_expiration(market, **kwargs):
        """Calculate expiration from 'expiration' or 'tenor'.
        :param market: dict
        :param expiration: date
        :param tenor: float or str
        :return: pd.Timestamp
        """
        if 'expiration' in kwargs:
            expiration = kwargs['expiration']
        elif 'tenor' in kwargs:
            tenor = kwargs['tenor']
            date = pd.Timestamp(market['date'])
            if isinstance(tenor, (np.float64, float, int)):
                expiration = date + pd.Timedelta('365 Days') * tenor
            else:
                expiration = date + to_offset(tenor)
        else:
            raise ValueError('Either expiration or tenor must be specified')
        return expiration

    @staticmethod
    def _calculate_strike(market, **kwargs):
        """Calculate strike from 'strike', 'moneyness' or 'implied'. Precedence in that order
        if multiple choices provided.
        :param strike: float or 'implied' (Optional)
        :param moneyness: float or str (Optional) -- percent of spot. '%' allowed at the end for clarity.
        :param target_price: float (Optional) -- target option price if computing implied strike.
        :param candidate: Option (Optional) -- for implied strike, Option with all terms except strike.
        :return: float
        """
        strike = kwargs.get('strike')
        if isinstance(strike, (float, int, np.float64)):
            pass                # use strike as is
        elif 'moneyness' in kwargs:
            moneyness = kwargs['moneyness']
            if isinstance(moneyness, str):
                moneyness = 0.01 * float(moneyness.strip('%'))
            else:
                moneyness = float(moneyness)
            underlyer = kwargs['underlyer']
            spot = market['prices'][underlyer]
            strike = moneyness * spot
        elif strike == 'implied':
            target_price = kwargs['target_price']
            candidate = kwargs['candidate']
            underlyer = candidate.underlyer
            option_type = candidate.option_type
            date = pd.Timestamp(market['date'])
            tenor = candidate.time_to_expiry(date)
            rate = market['discount_rates']
            spot = market['prices'][underlyer]
            div_rate = market.get('div_rates', {}).get(underlyer, 0)
            volatility = market['volatilities'][underlyer]
            strike = implied_strike(target_price, spot, rate, tenor, volatility, div_rate, option_type)
        else:
            raise ValueError("Either 'strike' or 'moneyness' must be specified")
        return strike

    def time_to_expiry(self, date):
        """
        Calculate the time to expiration in years.

        :param date: date object - As-of date.
        :return: float - Time to expiration in years.
        """
        date = pd.Timestamp(date)
        return (self.expiration - date) / pd.Timedelta('365 days')

    def reprice(self, market):
        """
        Calculate the price of the option based on current market data.

        :param market: dict - Current market data.
        :return: OptionPrice - Price of the option.
        """
        date = pd.Timestamp(market['date'])
        underlyer = self.underlyer
        spot_price = market['prices'][underlyer]
        discount_rate = market['discount_rates']
        div_rate = market.get('div_rates', {}).get(underlyer, 0.0)
        sigma = market['volatilities'][underlyer]
        data = black_scholes(spot_price, self.strike, self.time_to_expiry(date),
                             sigma, discount_rate, div_rate, self.option_type)
        data['und_price'] = spot_price
        return OptionPrice(name=self.name, date=date, **data)

    def __eq__(self, other):
        """
        Compare two options for equality.

        :param other: Option - The other option to compare.
        :return: bool - True if the options are equal, False otherwise.
        """
        attributes = ['name', 'underlyer', 'option_type', 'expiration', 'strike']
        return all(getattr(self, key) == getattr(other, key) for key in attributes)

    def to_string(self, indent=0):
        """
        Return a string representation of the option.

        :param indent: int - Indentation level.
        :return: str - String representation of the option.
        """
        return self.identifier


class OptionPrice(AssetPrice):
    """
    The OptionPrice class represents the price of an option at a specific date.

    Attributes:
        delta (float): Option delta.
        gamma (float): Option gamma.
        vega (float): Option vega.
        theta (float): Option theta.
        rho (float): Option rho.
        und_price (float): Underlying asset price.

    Methods:
        __init__(name, date, **kwargs): Initialize the OptionPrice object.
        to_string(delim): Return a string representation of the option price.
    """

    def __init__(self, name, date, **kwargs):
        """
        Initialize the OptionPrice object.

        :param name: str - Name of the option price.
        :param date: date object - Date of the option price.
        :param kwargs: dict - Keyword arguments for additional attributes:
                      (e.g. price, delta, gamma, vega, theta, rho, und_price).
        """
        super().__init__(name, date, **kwargs)
        for key in ['delta', 'gamma', 'vega', 'theta', 'rho', 'und_price']:
            setattr(self, key, kwargs[key])

    def to_string(self, delim=', '):
        """
        Return a string representation of the option price.

        :param delim: str - Delimiter between attribute-value pairs.
        :return: str - String representation of the option price.
        """
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
        theta = ((-S * sigma * exp(-q * T) * norm.pdf(d1)) / (2 * sqrt(T))
                 - r * K * exp(-r * T) * norm.cdf(d2) + q * S * exp(-q * T) * norm.cdf(d1))
    elif option_type == 'put':
        price = K * exp(-r * T) * norm.cdf(-d2) - S * exp(-q * T) * norm.cdf(-d1)
        delta = -exp(-q * T) * norm.cdf(-d1)
        theta = ((-S * sigma * exp(-q * T) * norm.pdf(d1)) / (2 * sqrt(T))
                 + r * K * exp(-r * T) * norm.cdf(-d2) - q * S * exp(-q * T) * norm.cdf(-d1))
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
