"""HoldingsPortfolio class"""
from copy import deepcopy
import pandas as pd


class HoldingsPortfolio:
    """HoldingsPortfolio maintains its holdings by updating with current market,
    adds and removes holdings. Checks for rebalance are performed here as
    instructed by a strategy class instance, as is a new portfolio target.
    From the new target and current holdings, a trade list is generated (that
    may incorporate tax inventory management) and new holdings are generated.
    Methods for evaluating trading (turnover, cost per share, etc) are available here.
    """
    def __init__(self, initial_cash=0, inventory_policy='FIFO'):
        self.cash = initial_cash
        self.holdings = []
        self.target = None
        self.trades = None
        self.inventory_policy = inventory_policy

    def reprice(self, context):
        _ = [holding.reprice(context) for holding in self.holdings]
        
    @property
    def aum(self):
        if self.holdings:
            return self.cash + self.to_frame().value.sum()
        else:
            return self.cash

    @staticmethod
    def holding_tax_rate(holding, date, price):
        """Return taxation rate per unit of holding."""
        if date > holding.acquisition_date + pd.Timedelta('365 days'):
            tax_rate = 0.2 * (price - holding.acquisition_price)
        else:
            tax_rate = 0.4 * (price - holding.acquisition_price)
        return tax_rate

    def get_asset_holdings(self, asset, date, price):
        """Get holdings for a given asset and order them according to inventory policy.
        :param asset: str -- asset symbol
        :param date: pd.Timestamp -- evaluation date for 'minimum_tax' inventory calculation
        :param price: float -- asset price for 'minimum_tax' inventory calculation
        :return: list(Holding)
        """
        holdings = [holding for holding in self.holdings if holding.asset == asset]
        if self.inventory_policy == 'FIFO':
            inventory = sorted(holdings, key=lambda holding: holding.acquisition_date)
        elif self.inventory_policy == 'minimum_tax':
            inventory = sorted(holdings, key=lambda holding: holding_tax_rate(holding, date, price))
        else:
            inventory = holdings
        return holdings

    def rebalance(self, target, context):
        """Update holdings with new target shares
        :param target: pd.Series -- target shares by asset
        :param context: dict - market data, asset definitions
        :return: None
        """
        date = context['market']['date']
        target = pd.Series(target)
        prices = pd.Series(context['market']['spot_prices']).reindex(target.index)
        for symbol, target_quantity in target.items():
            price = prices[symbol]
            asset_holdings = self.get_asset_holdings(symbol, date, price)
            current_quantity = sum([holding.quantity for holding in asset_holdings])
            quantity_change = target_quantity - current_quantity
            new_holding = Holding(symbol, date, price, target_quantity)
            if quantity_change > 0:
                if current_quantity >= 0:
                    self.add_holding(new_holding)
                else:
                    residual_holding = self.reduce_holdings(asset_holdings, new_holding)
                    if residual_holding is not None:
                        self.add_holding(residual_holding)
            elif quantity_change < 0:
                if current_quantity <= 0:
                    self.add_holding(new_holding)
                else:
                    residual_holding = self.reduce_holdings(asset_holdings, new_holding)
                    if residual_holding is not None:
                        self.add_holding(residual_holding)
            else:
                pass            # no trade

    def reduce_holdings(self, holdings, target_holding):
        """Use shares in target_holding to close out open holdings. Any unused target_holding
        is returned as a residual Holding.
        :param holdings: list(Holding) -- open holdings for a given asset
        :param target_holding: Holding -- holding with available shares to close open holdings
        :return: None or Holding -- holding with residual quantity, if any, else None
        """
        original_holdings = deepcopy(holdings)
        for holding in original_holdings:
            if holding.quantity <= target_holding.quantity:
                self.delete_holding(holding, price=target_holding.acquisition_price)
                target_holding.quantity -= holding.quantity
            else:
                self.reduce_holding(holding, quantity=target_holding.quantity,
                                    price=target_holding.acquisition_price)
                target_holding.quantity = 0
        if target_holding.quantity > 0:
            return target_holding
        else:
            return None

    def reduce_holding(self, holding, quantity, price):
                                    
        quantity_change = target_holding.quantity - holding.quantity
        holding.quantity = target_holding.quantity
        self.cash += quantity_change * price
        
    def delete_holding(self, holding, price):
        self.cash += holding.quantity * price
        self.holdings.remove(holding)

    def add_holding(self, holding):
        self.cash -= holding.quantity * holding.acquisition_price
        self.holdings.append(holding)

    def to_frame(self):
        """DataFrame representation of the holdings."""
        if self.holdings:
            frame = pd.concat([holding.to_series() for holding in self.holdings], axis=1).T
        else:
            frame = pd.DataFrame()
        return frame

    def to_string(self):
        strings = [f'cash: {self.cash}',
                   self.to_frame().to_string(),
                   ]
        return '\n'.join(strings)
