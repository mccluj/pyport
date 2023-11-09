class RebalancingRules:
    def __init__(self, rules):
        self.rules = rules

    def determine_actions(self, current_metrics, portfolio, market_data):
        actions = []
        # Logic to determine actions based on index exposure
        index_exposure_target = (self.rules['index_exposure']['target_min'] + 
                                 self.rules['index_exposure']['target_max']) / 2
        if current_metrics['index_exposure'] < index_exposure_target:
            quantity_to_buy = self.calculate_quantity('index_futures', 'buy', 
                                                      current_metrics['index_exposure'], 
                                                      index_exposure_target, portfolio, market_data)
            actions.append({'asset': 'index_futures', 'transaction': 'buy', 'quantity': quantity_to_buy})
        elif current_metrics['index_exposure'] > index_exposure_target:
            quantity_to_sell = self.calculate_quantity('index_futures', 'sell', 
                                                       current_metrics['index_exposure'], 
                                                       index_exposure_target, portfolio, market_data)
            actions.append({'asset': 'index_futures', 'transaction': 'sell', 'quantity': quantity_to_sell})
        # ... Add more logic for other metrics and rules
        return actions

    def calculate_quantity(self, asset, transaction_type, current_metric, target_metric, portfolio, market_data):
        # Placeholder for the logic to calculate the quantity to buy or sell
        adjustment_factor = target_metric - current_metric
        quantity = adjustment_factor * market_data.get_data_for_asset(asset).get('contract_size', 1)
        return max(0, quantity) if transaction_type == 'buy' else min(0, quantity)


portfolio = {
    'index_option': 100,    # Example quantity
    'intermediate_bonds': 500,  # Example quantity
    'index_futures': 10,    # Example quantity
    'bond_futures': 20,     # Example quantity
}

market_data = {
    'index_option': {'price': 200, 'delta': 0.5, 'duration': 5},
    'intermediate_bonds': {'price': 105, 'duration': 4},
    'index_futures': {'price': 110, 'contract_size': 1},
    'bond_futures': {'price': 120, 'contract_size': 1},
}

rebalance_rules = {
    'index_exposure': {'target_min': 0.5, 'target_max': 0.7},
    'portfolio_duration': {'target_min': 3, 'target_max': 7},
}
