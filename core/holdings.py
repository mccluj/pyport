"""Container class for holdings."""
import pandas as pd
from pyport import Holding


class Holdings:
    def __init__(self):
        self.holdings = []

    def add_holding(self, holding):
        self.holdings.append(holding)

    def remove_holding(self, holding):
        self.holdings.remove(holding)

    def get_holdings(self):
        return self.holdings
