from typing import NamedTuple, List

class Asset:
    name: str
    price: float

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

class Stock(Asset):
    dividend: float

    def __init__(self, name: str, price: float, dividend: float):
        super().__init__(name, price)
        self.dividend = dividend

class Option(Asset):
    greeks: NamedTuple

    def __init__(self, name: str, price: float, greeks: NamedTuple):
        super().__init__(name, price)
        self.greeks = greeks

class Bond(Asset):
    metrics: NamedTuple

    def __init__(self, name: str, price: float, metrics: NamedTuple):
        super().__init__(name, price)
        self.metrics = metrics

# Example NamedTuple for Greeks and Metrics
class OptionGreeks(NamedTuple):
    delta: float
    gamma: float
    # Add other greeks as needed

class BondMetrics(NamedTuple):
    duration: float
    convexity: float
    # Add other metrics as needed

# Example usage
option_greeks = OptionGreeks(delta=0.5, gamma=0.1)
option = Option(name="Option XYZ", price=100.0, greeks=option_greeks)

bond_metrics = BondMetrics(duration=5.0, convexity=1.2)
bond = Bond(name="Bond ABC", price=105.0, metrics=bond_metrics)

print(option.name, option.greeks)
print(bond.name, bond.metrics)
