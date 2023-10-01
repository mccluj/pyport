"""Defined outcome class to create an asset from a basket of options and a bond."""
import pandas as pd
import pyport


class DefinedOutcome:
    """DefinedOutcome represents a basket of assets, typically with one asset "implied", meaning some attribute
    of that asset, say option strike, must be imputed from the market value of the other assets and a given
    target value for the basket.
    As a base class, this can be derived to allow for bespoke calculations, e.g. BufferETF could add remaining
    buffer and cap to it's calculated values.
    Attributes:
      name (str or tuple)
      shares (pd.Series) -- shares of member assets, indexed by their "role" names.
      assets -- dictionary of assets indexed by the asset name
    """
    def __init__(self, name, shares, assets):
        """
        :param name: str or tuple
        :param shares: dict or pd.Series
        :param assets: dict
        """
        self.name = name
        self.shares = shares
        self.assets = assets

    @classmethod
    def from_market(self, market, date, configuration):
        """Create a DefinedOutcome instance from market data, date and configuration.
        1. Instantiate all sub-assets, without repricing.
        2. If 'implied' assets, compute implied attribute (e.g. strike).

        2023-10-01 -- 'etf' stanza is meta data. if expense_ratio provided, then nav is
                       (1 - expense_ratio * tenor_days / 365) x price + expense_ratio * remaining_days / 365 * inception_value
        :param market: MarketData
        :param date: datetime
        :param configuration: dict -- etf, assets, and shares stanzas
        """
        etf_definition = configuration['etf']
        etf_name = etf_definition['name']
        shares = pd.Series(configuration['shares'])
        implied_item = None
        assets = pd.Series(dtype=object)
        for name, definition in configuration['assets'].items():
            if 'implied' in definition.values():
                if implied_item is None:
                    implied_item = name, definition
                else:
                    raise ValueError(f'Cannot have more than one "implied" asset.')
            _class = getattr(pyport, definition['asset_type'])
            assets[name] = _class.from_market(market, date, definition)
        if implied_item is not None:
            name, definition = implied_item
            assets[name] = self.solve_implied_asset(market, date, definition)
        return DefinedOutcomeBasket(etf_name, shares, assets)

    def reprice(self, market, date, detail=False):
        date = pd.Timestamp(date)
        shares = self.shares
        assets = self.assets
        price_data = pd.DataFrame(index=shares.index)
        for asset_name, asset_shares in shares.items():
            asset = assets[asset_name]
            price_data.loc[asset_name] = asset.reprice(market, date)
        price = shares @ price_data.price
        delta = shares @ price_data.delta.fillna(0)
        return_data = pd.Series({'name': self.name,
                                 'date': date,
                                 'price': price,
                                 'delta': delta,
                                 })
        return return_data, price_data if detail else return_data

    def solve_implied_asset(self, market, date, definition):
        value = 0
        for name, shares in self.shares.items():
            try:
                asset = self.assets[name]
                value += shares * asset.reprice(market, date).price
            except AttributeError as e:
                implied_asset = asset
                pass
        try:
            shares = np.sign(target_value - value)
            target_asset_value = np.abs(target_value - value)
            implied_asset.compute_implied_strike(target_asset_value, market, date)
        except Exception as e:
            print(f'Cannot solve for implied strike: {e}')
            raise e
