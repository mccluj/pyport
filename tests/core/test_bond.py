"""Tests of Bond class"""
import unittest
import pytest
import numpy as np
import pandas as pd
from pyport import Bond


class TestBond(unittest.TestCase):
    def setUp(self):
        self.market = {'date': '1/1/2023',
                       'prices': {'SPY': 400},
                       'discount_rates': 0.05,
                       'div_rates': {'SPY': 0.016},
                       'volatilities': {'SPY': 0.20},
                       }

    def test_bond_from_notional_and_tenor_years(self):
        bond = Bond.from_market(self.market, 'test_bond', notional=100, tenor=1.0)
        assert bond.notional == 100
        assert bond.maturity == pd.Timestamp('1/1/2024')

    def test_bond_from_notional_and_tenor_freq(self):
        bond = Bond.from_market(self.market, 'test_bond', notional=100, tenor='BA')
        assert bond.notional == 100
        assert bond.maturity == pd.Timestamp('12/29/2023')

    def test_bond_from_target_price_and_tenor_years(self):
        target_price = 100 * np.exp(-0.05)
        bond = Bond.from_market(self.market, 'test_bond', target_price=target_price, tenor=1.0)
        self.assertAlmostEqual(bond.notional, 100.0)

    def test_bond_to_string(self):
        bond = Bond.from_market(self.market, 'test_bond', notional=100, tenor=1.0)
        assert bond.to_string() == 'test_bond 20240101 100.0000'
        
