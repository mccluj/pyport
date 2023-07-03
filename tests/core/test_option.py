"""Tests of Option class"""
import unittest
import pytest
from pyport import Option


class TestOption(unittest.TestCase):
    def setUp(self):
        self.context = {
            'market': {'date': '1/1/2023',
                       'spot_prices': {'SPY': 400},
                       'rates': 0.05,
                       },
            'models': {'volatilities': {'SPY': 0.20},
                       'div_rates': {'SPY': 0.016},
                       },

            }

    def test_put_call_parity(self):
        pass

    def test_equality(self):
        option_1 = Option('SPY', 'call', '1/1/2024', 400)
        option_2 = Option('SPY', 'call', '1/1/2024', 400)
        option_3 = Option('SPY', 'put', '1/1/2024', 400)
        assert option_1 == option_2
        assert option_2 != option_3

    @pytest.mark.skip
    def test_to_string(self):
        print(self.option.to_string())

    @pytest.mark.skip
    def test_reprice(self):
        result = self.option.reprice(self.context)
        print(result)
