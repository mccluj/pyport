"""Strategy class to test for rebalance and generate portfolio targets."""
import pandas as pd


class Strategy:
    def __init__(self, target_template, rebalance_rules):
        self.target_template = target_template
        self.rebalance_rules = rebalance_rules

    def needs_rebalance(self, market, portfolio):
        # Implementation to check if rebalance is needed
        # Return True if rebalance is needed, False otherwise
        pass

    def generate_target_portfolio(self, market, assets, portfolio):
        # Implementation to generate target portfolio
        # Return a pandas Series with target shares for each asset
        template = self.target_template
        if 'shares' in template:
            target = pd.Series(template['shares'])
        elif 'weights' in template:
            weights = pd.Series(template['weights'])
            target = Strategy.target_from_weights(weights, portfolio.aum, market, assets)
        return target

    @staticmethod
    def target_from_weights(weights, aum, market, assets):
        aum = portfolio.aum
        allocations = aum * weights
        assets = assets.reindex(weights.index)
        prices = assets.apply(lambda asset: asset.reprice(market).price)
        target = allocations.div(prices)
        return target
