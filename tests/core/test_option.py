import unittest
from datetime import datetime, timedelta

import pandas as pd
from pandas import Timestamp
from pyport.lib.black_scholes import black_scholes
from pyport.core.option import Option, OptionPricingResult


class OptionTests(unittest.TestCase):

    def setUp(self):
        self.market = {
            'date': pd.Timestamp('3/1/2023'),
            'spot_prices': {'AAPL': 150.0},
            'volatilities': {'AAPL': 0.2},
            'dividend_rates': {'AAPL': 0.01},
            'discount_rates': 0.05,
        }
        self.config = {
            'underlyer': 'AAPL',
            'strike': '155.0',
            'expiry': '2023-06-30',
            'option_type': 'call',
            'exercise': 'european'
        }

    def test_default_init_and_from_config(self):
        # Create option using default __init__
        default_option = Option('AAPL', 155.0, '2023-06-30', 'call', 'european')

        # Create option using from_config
        config_option = Option.from_config(self.market, self.config)

        # Verify option attributes are the same
        self.assertEqual(default_option.underlyer, config_option.underlyer)
        self.assertEqual(default_option.strike, config_option.strike)
        self.assertEqual(default_option.expiration, config_option.expiration)
        self.assertEqual(default_option.option_type, config_option.option_type)
        self.assertEqual(default_option.exercise, config_option.exercise)

    def test_reprice(self):
        # Create option using default __init__
        default_option = Option('AAPL', 155.0, '2023-06-30', 'call', 'european')

        # Create option using from_config
        config_option = Option.from_config(self.market, self.config)

        # Compute option price and Greeks using default __init__
        default_result = default_option.reprice(self.market)

        # Compute option price and Greeks using from_config
        config_result = config_option.reprice(self.market)

        # Verify option pricing and Greeks are the same
        self.assertAlmostEqual(default_result.price, config_result.price, places=4)
        self.assertAlmostEqual(default_result.delta, config_result.delta, places=4)
        self.assertAlmostEqual(default_result.gamma, config_result.gamma, places=4)
        self.assertAlmostEqual(default_result.theta, config_result.theta, places=4)
        self.assertAlmostEqual(default_result.vega, config_result.vega, places=4)
        self.assertAlmostEqual(default_result.rho, config_result.rho, places=4)


if __name__ == '__main__':
    unittest.main()
