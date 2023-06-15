from math import exp, log, sqrt
from scipy.stats import norm
import pandas as pd

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

if __name__ == "__main__":
    # Define input parameters
    S = 100  # Current price of the underlying asset
    K = 100  # Strike price
    r = 0.05  # Risk-free interest rate
    T = 1  # Time to expiration (1 year)
    sigma = 0.2  # Volatility
    q = 0.02  # Dividend rate
    for option_type in ['call', 'put']:
        print(f"{option_type}\n{black_scholes(S, K, r, T, sigma, q, option_type)}")
    
