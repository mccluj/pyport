from pyport.assets.asset import Asset


class Bundle(Asset):
    def __init__(self, shares, assets):
        self.shares = shares
        self.assets = assets

    @classmethod
    def from_weights(cls, target_value, weights, assets):
        """Instantiate class from asset weights and target_value.
        :param weights: pd.Series of asset weights in portfoliio
        :param assets: pd.Series of instantiated assets
        :param target_value: float
        :return: Bundle
        """
        shares = target_value * weights / prices
        return cls(shares, assets)

    @classmethod
    def from_config(cls, config, asset_configs, market):
        """
        :param config: dictionary of bundle charateristics
        :param asset_configs: dictionary of asset configurations
        :param market: dictionary of current market prices, rates, etc
        :return: Bundle
        """
        if 'weights' in config:
            target_value = config['target_value']
            weights = pd.Series(config['weights'])
            symbols = set(weights.index)
        elif 'shares' in config:
            shares = pd.Series(config['shares'])
            symbols = set(shares.index)
        else:
            raise AttributeError('Must specify either weights or shares')
            
        missing_assets = symbols.difference(asset_configs)
        if missing_assets:
            raise RuntimeError(f'Missing assets: {missing_assets}')
        
        assets = pd.Series()
        for key, asset_config in asset_configs.items():
            asset_type = asset_configs['type']
            asset_class = getattr(pyport, asset_config)
            if asset_class is None:
                raise AttributeError(f'asset class {asset_type} is not defined')
            assets[key] = asset_class.from_config(asset_config, asset_configs, market)
        
        prices = assets.apply(lambda asset: asset.price)
        return cls.from_weights(
