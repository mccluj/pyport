"""Tests of CBOEOption."""
import pytest
import pandas as pd
from pyport.core.cboe_option import CBOEOption, OptionType


class TestCBOEOption:
    def setup_class(self):
        print('Setup class level resources')

    def teardown_class(self):
        print('Teardown class level resources')

    def setup_method(self, method):
        self.call_option = CBOEOption('^SPX', 'SPXW', '1/1/2024', 'C', 100)
        print('Setup for {method.__name__}')

    def teardown_method(self, method):
        print('Teardown for {method.__name__}')

    def test_base_constructor(self):
        option = self.call_option
        assert option.expiration == pd.Timestamp('1/1/2024')
        assert option.root == 'SPXW'
        assert option.option_type == OptionType.CALL
        

    def test_base_tubple(self):
        expected = ('^SPX', 'SPXW', pd.Timestamp('1/1/2024'), 'C', 100)
        assert self.call_option.as_tuple() == expected
        
