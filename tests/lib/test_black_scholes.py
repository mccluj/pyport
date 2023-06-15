import unittest
from math import exp, log, sqrt
from scipy.stats import norm
import pandas as pd
from pyport.lib.black_scholes import black_scholes


class BlackScholesTestCase(unittest.TestCase):

    def test_call_option(self):
        S = 100.0
        K = 100.0
        r = 0.05
        T = 1.0
        sigma = 0.2
        q = 0.02
        option_type = 'call'
        expected_results = {'price': 9.227005508154036, 'delta': 0.586851146134764, 'gamma': 0.018950578755008718, 'vega': 37.901157510017434, 'theta': -5.0893189139983335, 'rho': 49.45810910532236}

        result = black_scholes(S, K, r, T, sigma, q, option_type)
        self.assertAlmostEqual(result, expected_results, places=6)

    def test_put_option(self):
        S = 100.0
        K = 100.0
        r = 0.05
        T = 1.0
        sigma = 0.2
        q = 0.02
        option_type = 'put'

        expected_results = {'price': 6.330080627549918, 'delta': -0.3933475271719913, 'gamma': 0.018950578755008718, 'vega': 37.901157510017434, 'theta': -2.293569138108274, 'rho': -45.66483334474905}
        result = black_scholes(S, K, r, T, sigma, q, option_type)
        self.assertAlmostEqual(result, expected_results, places=6)

    def test_invalid_option_type(self):
        S = 100.0
        K = 100.0
        r = 0.05
        T = 1.0
        sigma = 0.2
        q = 0.0
        option_type = 'invalid'

        with self.assertRaises(ValueError):
            black_scholes(S, K, r, T, sigma, q, option_type)

if __name__ == '__main__':
    unittest.main()
