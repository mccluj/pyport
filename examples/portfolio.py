class Portfolio:
    def __init__(self, initial_holdings):
        self.holdings = initial_holdings  # Dictionary of asset names and quantities

    def calculate_metrics(self, market_data):
        portfolio_value = sum(market_data[asset]['price'] * quantity 
                              for asset, quantity in self.holdings.items())

        index_exposure = sum(market_data[asset]['delta'] * quantity 
                             for asset in self.holdings if 'index' in asset)

        portfolio_duration = sum(market_data[asset]['duration'] * quantity 
                                 for asset in self.holdings if 'bond' in asset)

        self.metrics = {
            'portfolio_value': portfolio_value,
            'index_exposure': index_exposure,
            'portfolio_duration': portfolio_duration
        }

    def update_holdings(self, actions):
        for action in actions:
            asset = action['asset']
            transaction_type = action['transaction']
            quantity = action['quantity']
            
            if transaction_type == 'buy':
                self.holdings[asset] += quantity
            elif transaction_type == 'sell':
                self.holdings[asset] = max(0, self.holdings[asset] - quantity)  # Ensure no negative quantities
