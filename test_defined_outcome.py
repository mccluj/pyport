"""Tests of DefinedOutcomBasket"""
from pyport.core.defined_outcome import DefinedOutcome


class TestDefinedOutcome:
    def setup_class(self):
        self.initial_configuration = {
            'etf': {
                'expense_ratio': 0.008,
                'issue_price': 25,
                'name': 'PJUN',
                'tenor_days': 365,
                },
            'assets': {
                'capped_call': {
                    'asset_type': 'Option',
                    'strike': 'implied',
                    'tenor_days': 365,
                    'option_type': 'call',
                    'underlyer': 'SPY'},
                'base_call': {
                    'asset_type': 'Option',
                    'moneyness': 0.01,
                    'tenor_days': 365,
                    'option_type': 'call',
                    'underlyer': 'SPY'},
                'upper_put': {
                    'asset_type': 'Option',
                    'moneyness': 1.0,
                    'tenor_days': 365,
                    'option_type': 'put',
                    'underlyer': 'SPY'},
                'lower_put': {
                    'asset_type': 'Option',
                    'moneyness': 0.85,
                    'tenor_days': 365,
                    'option_type': 'put',
                    'underlyer': 'SPY'},
                },
            'shares': {
                'capped_call': -1,
                'base_call': 1,
                'upper_put': 1,
                'lower_put': -1
                },
            }
        self.existing_configuration = {
            'etf': {
                'expense_ratio': 0.008,
                'issue_price': 25,
                'name': 'PJUN',
                'expiration': '6/1/2024',
                },
            'assets': {
                'capped_call': {
                    'asset_type': 'Option',
                    'strike': 'implied',
                    'expiration': '6/1/2024',
                    'option_type': 'call',
                    'underlyer': 'SPY'},
                'base_call': {
                    'asset_type': 'Option',
                    'moneyness': 0.01,
                    'expiration': '6/1/2024',
                    'option_type': 'call',
                    'underlyer': 'SPY'},
                'upper_put': {
                    'asset_type': 'Option',
                    'moneyness': 1.0,
                    'expiration': '6/1/2024',
                    'option_type': 'put',
                    'underlyer': 'SPY'},
                'lower_put': {
                    'asset_type': 'Option',
                    'moneyness': 0.85,
                    'expiration': '6/1/2024',
                    'option_type': 'put',
                    'underlyer': 'SPY'},
                },
            'shares': {
                'capped_call': -1,
                'base_call': 1,
                'upper_put': 1,
                'lower_put': -1
                },
            }
        self.initial_market = {
            'prices': {'SPY': 400},
            'volatilities': {'SPY': {'*': 0.2}},
            'discount_rates': 0.05,
            'dividend_yields': {'SPY': 0.02},
            }
        self.current_market = {
            'prices': {'SPY': 400},
            'volatilities': {'SPY': {'*': 0.2}},
            'discount_rates': 0.05,
            'dividend_yields': {'SPY': 0.02},
            }
        self.initial_date = '6/1/2023'
        self.current__date = '9/1/2023'

    def test_initial_defined_outcome(self):
        defined_outcome = DefinedOutcome.from_market(self.initial_market, self.initial_date,
                                                      self.initial_configuration)
        
