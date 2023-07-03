"""Tests of Option class"""
import unittest
import pytest
from pyport import Option


class TestOption(unittest.TestCase):
    def setUp(self):
        self.context = {
            'market': {'date': '1/1/2023',
                       'spot_prices': {'SPY': 400},
                       'discount_rates': 0.05,
                       },
            'models': {'volatilities': {'SPY': 0.20},
                       'div_rates': {'SPY': 0.016},
                       },

            }

    def test_put_call_parity(self):
        call = Option('SPY', 'call', '1/1/2024', 400).reprice(self.context)
        put = Option('SPY', 'put', '1/1/2024', 400).reprice(self.context)

    def test_equality(self):
        option_1 = Option('SPY', 'call', '1/1/2024', 400)
        option_2 = Option('SPY', 'call', '1/1/2024', 400)
        option_3 = Option('SPY', 'put', '1/1/2024', 400)
        assert option_1 == option_2
        assert option_2 != option_3

    def test_to_string(self):
        option = Option('SPY', 'call', '1/1/2024', 400)
        assert option.to_string() == 'Option(SPY_20240101_400.00_call)'

    def test_option_reprice(self):
        pricing_info = Option('SPY', 'call', '1/1/2024', 400).reprice(self.context)
        assert pricing_info.to_string() == 'SPY_20240101_400.00_call: date: 2023-01-01, price: 37.85, delta: 0.60, gamma: 0.00, vega: 151.42, theta: -21.37, rho: 200.86, und_price: 400.00'
