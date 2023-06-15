import pandas as pd


def string_to_float(string, reference=None):
    if isinstance(string, str):
        if string[-1] == '%':
            value = 0.01 * float(string.strip('%'))
            if isreference is not None:
                result *= reference
    result = float(string)
    return result
