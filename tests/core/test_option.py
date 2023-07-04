"""Tests of Option class"""
import unittest
import pytest
import numpy as np
import pandas as pd
from pyport import Option


class TestOption(unittest.TestCase):
    def setUp(self):
        self.market = {'date': '1/1/2023',
                       'spot_prices': {'SPY': 400},
                       'discount_rates': 0.05,
                       'div_rates': {'SPY': 0.016},
                       'volatilities': {'SPY': 0.20},
                       }

    def test_put_call_parity(self):
        strike = 400
        call = Option('spy_call', 'SPY', 'call', '1/1/2024', strike).reprice(self.market)
        put = Option('spy_put', 'SPY', 'put', '1/1/2024', strike).reprice(self.market)
        stock = self.market['spot_prices']['SPY']
        discount = self.market['discount_rates']
        div_rate = self.market['div_rates']['SPY']
        forward = stock * np.exp(-div_rate) - strike * np.exp(-discount)
        self.assertAlmostEqual(call.price - put.price, forward)
        
    def test_equality(self):
        option_1 = Option('spy_call', 'SPY', 'call', '1/1/2024', 400)
        option_2 = Option('spy_call', 'SPY', 'call', '1/1/2024', 400)
        option_3 = Option('spy_put', 'SPY', 'put', '1/1/2024', 400)
        assert option_1 == option_2
        assert option_2 != option_3

    def test_time_to_expiry(self):
        option = Option('test', 'SPY', 'call', '1/1/2024', 400)
        self.assertAlmostEqual(option.time_to_expiry('1/1/2023'), 1.0)

    def test_to_string(self):
        option = Option('spy_call', 'SPY', 'call', '1/1/2024', 400)
        assert option.to_string() == 'Option(spy_call)'

    def test_option_reprice(self):
        pricing_info = Option('spy_call', 'SPY', 'call', '1/1/2024', 400).reprice(self.market)
        assert pricing_info.to_string() == 'spy_call: date: 2023-01-01, price: 37.85, delta: 0.60, gamma: 0.00, vega: 151.42, theta: -21.37, rho: 200.86, und_price: 400.00'

    def test_rename(self):
        option = Option('spy_call', 'SPY', 'call', '1/1/2024', 400)
        assert option.name == 'spy_call'
        option.rename('dummy')
        assert option.name == 'dummy'
        option.rename()
        assert option.name == 'SPY_20240101_400.00_call'

    def test_to_string(self):
        option = Option('test', 'SPY', 'call', '1/1/2024', strike=400)
        assert option.to_string() == 'SPY_20240101_400.00_call'

    def test_instantiate_strike_value_error(self):
        market = self.market
        option = Option('test', 'SPY', 'call', '1/1/2024')
        assert option.strike is None
        with pytest.raises(ValueError) as excinfo:
            option._instantiate_strike(market)
        assert str(excinfo.value) == 'Either strike or moneyness must be specified'
        
    def test_instantiate_strike_percent_of_spot(self):
        market = self.market
        option = Option('test', 'SPY', 'call', '1/1/2024', moneyness=1.02).instantiate(market)
        assert option.strike == 408
        option = Option('test', 'SPY', 'call', '1/1/2024', moneyness='102%').instantiate(market)
        assert option.strike == 408

    def test_instantiate_implied_strike_missing_option_price(self):
        market = self.market
        with pytest.raises(ValueError) as excinfo:
            _ = Option('test', 'SPY', 'call', '1/1/2024', strike='implied').instantiate(market)
        assert str(excinfo.value) == 'missing option_price implied strike calculation'

    def test_instantiate_implied_strike(self):
        market = self.market
        target = Option('test', 'SPY', 'call', '1/1/2024', strike=408).reprice(market)
        option = Option('test', 'SPY', 'call', '1/1/2024', strike='implied')
        option.instantiate(market, option_price=target.price)
        self.assertAlmostEqual(option.strike, 408)

    def test_instantiate_with_float_tenor(self):
        market = self.market
        option = Option('test', 'SPY', 'call', strike=400, tenor=1.0).instantiate(market)
        assert option.expiration == pd.Timestamp('1/1/2024')

    def test_instantiate_with_string_tenor(self):
        market = self.market
        option = Option('test', 'SPY', 'call', strike=400, tenor='A').instantiate(market)
        assert option.expiration == pd.Timestamp('12/31/2023')

    def test_instantiate_with_implied_and_tenor(self):
        market = self.market
        target = Option('test', 'SPY', 'call', '12/31/2023', strike=408).reprice(market)
        option = (Option('test', 'SPY', 'call', strike='implied', tenor='A')
                  .instantiate(market, target.price))
        assert option.expiration == pd.Timestamp('12/31/2023')
        self.assertAlmostEqual(option.strike, 408)
