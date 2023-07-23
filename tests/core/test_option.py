"""Tests of Option class"""
import unittest
import pytest
import numpy as np
import pandas as pd
from pyport import Option
from pyport import AssetManager


class TestOption(unittest.TestCase):
    def setUp(self):
        self.market = {'date': '1/1/2023',
                       'prices': {'SPY': 400},
                       'discount_rates': 0.05,
                       'div_rates': {'SPY': 0.016},
                       'volatilities': {'SPY': 0.20},
                       }
        self.put_option = Option('put', 'SPY', 'put', '1/1/2024', 400)
        self.call_option = Option('call', 'SPY', 'call', '1/1/2024', 400)
        self.manager = AssetManager()

    def tearDown(self):
        self.manager.reset()

    def test_put_call_parity(self):
        strike = 400
        call = self.call_option.reprice(self.market)
        put = self.put_option.reprice(self.market)
        stock = self.market['prices']['SPY']
        discount = self.market['discount_rates']
        div_rate = self.market['div_rates']['SPY']
        forward = stock * np.exp(-div_rate) - strike * np.exp(-discount)
        self.assertAlmostEqual(call.price - put.price, forward)
        
    def test_equality(self):
        option_1 = Option('call', 'SPY', 'call', '1/1/2024', 400)
        assert option_1 == self.call_option
        assert self.call_option != self.put_option

    def test_time_to_expiry(self):
        option = self.call_option
        self.assertAlmostEqual(option.time_to_expiry('1/1/2023'), 1.0)

    def test_option_reprice(self):
        pricing_info = self.call_option.reprice(self.market)
        assert pricing_info.to_string() == 'call: date: 2023-01-01, price: 37.85, delta: 0.60, gamma: 0.00, vega: 151.42, theta: -21.37, rho: 200.86, und_price: 400.00'

    def test_identifier(self):
        assert self.call_option.to_string() == 'SPY_20240101_400.00_call'
        incomplete = Option('incomplete', None, None, None, None)
        assert incomplete.identifier is None

    def test_to_string(self):
        assert self.call_option.to_string() == 'SPY_20240101_400.00_call'

    def test_calculate_strike_error(self):
        market = self.market
        with pytest.raises(ValueError) as excinfo:
            _ = Option._calculate_strike(market)
        assert str(excinfo.value) == "Either 'strike' or 'moneyness' must be specified"
        
    def test_calculate_strike_with_moneyness(self):
        market = self.market
        strike = Option._calculate_strike(market, underlyer='SPY', moneyness=1.02)
        assert strike == 408
        strike = Option._calculate_strike(market, underlyer='SPY', moneyness='102%')
        assert strike == 408

    def test_calculate_implied_strike_missing_target_price(self):
        market = self.market
        with pytest.raises(KeyError) as excinfo:
            _ = Option._calculate_strike(market, underlyer='SPY', strike='implied')
        assert str(excinfo.value) == "'target_price'"

    def test_calculate_implied_strike(self):
        market = self.market
        target = Option('test', 'SPY', 'call', '1/1/2024', strike=408)
        target_price = target.reprice(market).price
        candidate = self.call_option
        strike = Option._calculate_strike(market, strike='implied', candidate=candidate, target_price=target_price)
        self.assertAlmostEqual(strike, target.strike)

    def test_calculate_expiration_with_float_tenor(self):
        market = self.market
        option = self.call_option
        expiration = Option._calculate_expiration(market, tenor=1.0)
        assert expiration == pd.Timestamp('1/1/2024')

    def test_calculate_expiration_with_string_tenor(self):
        market = self.market
        option = self.call_option
        expiration = Option._calculate_expiration(market, tenor='A')
        assert expiration == pd.Timestamp('12/31/2023')

    def test_instantiate_with_implied_and_tenor(self):
        market = self.market
        target = Option('test', 'SPY', 'call', '12/31/2023', strike=408).reprice(market)
        option = Option.from_market(market, 'test', underlyer='SPY', option_type='call',
                                    tenor='A', strike='implied', target_price=target.price)
        assert option.expiration == pd.Timestamp('12/31/2023')
        self.assertAlmostEqual(option.strike, 408)
