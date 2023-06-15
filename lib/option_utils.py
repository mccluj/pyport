from math import exp, log, sqrt
from scipy.stats import norm
from pyport.lib.black_scholes import black_scholes


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



if __name__ == '__main__':
    # Example usage
    option_price = 10.35
    current_price = 100.0
    risk_free_rate = 0.05
    time_to_expiration = 0.5
    volatility = 0.2
    dividend_rate = 0.0
    option_type = 'call'

    implied_strike_price = implied_strike(option_price, current_price, risk_free_rate, time_to_expiration,
                                          volatility, dividend_rate, option_type)
    print("Implied Strike Price:", implied_strike_price)
    
