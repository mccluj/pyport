import pandas as pd
from math import log, sqrt, exp
from scipy.stats import norm
from pyport.lib.black_scholes import black_scholes


class Option:
    """
    Represents a financial option.
    """

    def __init__(self, underlyer, strike, expiration, option_type, exercise):
        """Initialize the Option instance with provided parameters."""
        self.underlyer = underlyer
        self.strike = strike
        self.expiration = pd.Timestamp(expiration)
        self.option_type = option_type
        self.exercise = exercise

    @classmethod
    def from_config(cls, market, config):
        """Construct 
        :param market: dict -- context information
        :param config: dict -- option configuration parameters
        """
        underlyer = config['underlyer']
        spot = market['spot_prices'][underlyer]
        date = pd.Timestamp(market['date'])
        strike = string_to_float(config['strike'], reference=spot)
        if 'expiry' in config:
            expiry = pd.Timestamp(config['expiry'])
        elif 'tenor' in config:
            expiry = date + to_offset(config['tenor'])
        else:
            raise RuntimeError('Either expiry or tenor needed for creation')
        exercise = config.get('exercise', 'european')
        option_type = config['option_type']
        object = cls(underlyer, strike, exercise, option_type, exercise)
        object.initial_valuation = object.reprice(market)
        return object
        
    def unit_reprice(self, date, spot, volatility, discount, dividend_rate):
        """Compute the price and greeks for a single option using the specified model."""
        if self.exercise == 'american':
            # Placeholder for future binomial tree implementation
            return None  # Placeholder return value for American-style options
        time_to_expiry = (self.expiration - pd.Timestamp(date)) / pd.Timedelta('365D')
        results = black_scholes(spot, self.strike, discount, time_to_expiry, volatility, dividend_rate, self.option_type)
        return OptionPricingResult(**results)

    def reprice(self, market):
        """Reprice the option using the market structure."""
        date = market['date']
        spot = market['spot_prices'][self.underlyer]
        volatility = market['volatilities'][self.underlyer]
        dividend_rate = market['dividend_rates'][self.underlyer]
        discount = market['discount_rates'][date]
        return self.unit_reprice(date, spot, volatility, discount, dividend_rate)


class OptionPricingResult:
    """
    Represents the result of option pricing including price and greeks.
    """

    def __init__(self, price, delta, gamma, theta, vega, rho):
        """Initialize the OptionPricingResult instance with provided values."""
        self.price = price
        self.delta = delta
        self.gamma = gamma
        self.theta = theta
        self.vega = vega
        self.rho = rho


# Usage example
if __name__ == '__main__':
    market = {
        'date': pd.Timestamp('2023-06-14'),
        'spot_prices': {'AAPL': 150.0, 'GOOG': 2500.0},
        'volatilities': {'AAPL': 0.2, 'GOOG': 0.3},
        'dividend_rates': {'AAPL': 0.02, 'GOOG': 0.0},
        'discount_rates': {pd.Timestamp('2023-06-14'): 0.05}
    }

    option = Option('AAPL', 160.0, pd.Timestamp('2023-12-31'), 'put', 'european')
    result = option.reprice(market)

    print("Option Price:", result.price)
    print("Delta:", result.delta)
    print("Gamma:", result.gamma)
    print("Theta:", result.theta)
    print("Vega:", result.vega)
    print("Rho:", result.rho)
