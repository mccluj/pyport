"""Options that incorporate CBOE qualifiers."""
import numpy as np
import pandas as pd
from enum import Enum


class OptionType(Enum):
    CALL = 'C'
    PUT = 'P'
    
    def lookup(key):
        if type(key) == OptionType:
            return key
        elif key.lower() in ['call', 'c']:
            return OptionType.CALL
        elif key.lower() in ['put', 'p']:
            return OptionType.PUT
        else:
            raise ValueError(f'Invalid key: {key}')


class CBOEOption:
    def __init__(self, underlying_symbol, root, expiration, option_type, strike):
        self.underlying_symbol = underlying_symbol
        self.root = root
        self.expiration = pd.Timestamp(expiration)
        self.option_type = OptionType.lookup(option_type)
        self.strike = strike

    def as_tuple(self):
        if self.option_type == OptionType.CALL:
            option_type = 'C'
        else:
            option_type = 'P'
        return (self.underlying_symbol, self.root, self.expiration.date(), option_type, self.strike)


def calculate_payoff(option, underlying_price):
    if option.option_type == OptionType.CALL:
        payoff = np.maximum(0.0, underlying_price - option.strike)
    else:
        payoff = np.maximum(0.0, option.strike - underlying_price)
    return payoff

