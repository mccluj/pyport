class TradeNetter:
    def __init__(self, trades, prices_dict):
        """Initialize the TradeNetter with trades and prices."""
        self.trades = trades
        self.prices_dict = prices_dict
        self.net_shares = {}

    def calculate_net_shares(self):
        """Calculate the net trade shares for each asset."""
        for trade in self.trades:
            asset = trade['asset']
            shares = trade['trade_shares']
            if asset in self.net_shares:
                self.net_shares[asset] += shares
            else:
                self.net_shares[asset] = shares

    def get_price_based_on_net_shares(self, asset):
        """Return the appropriate price based on the net trade shares."""
        total_shares = self.net_shares[asset]
        price_info = self.prices_dict[asset]
        if total_shares < 0:
            return price_info['bid_price']
        elif total_shares == 0:
            return price_info['mid_price']
        else:
            return price_info['ask_price']

    def apply_prices_to_trades(self):
        """Apply the correct price to each trade based on net shares."""
        for trade in self.trades:
            asset = trade['asset']
            trade['applied_price'] = self.get_price_based_on_net_shares(asset)

    def process_trades(self):
        """Process trades to calculate net shares and apply prices."""
        self.calculate_net_shares()
        self.apply_prices_to_trades()
        return self.trades

def main():
    # Sample trades list of dictionaries
    trades = [
        {'asset': 'asset1', 'trade_shares': -100},
        {'asset': 'asset1', 'trade_shares': 50},
        {'asset': 'asset2', 'trade_shares': 200},
        {'asset': 'asset2', 'trade_shares': -150},
        {'asset': 'asset3', 'trade_shares': 0},
        {'asset': 'asset3', 'trade_shares': 0}
    ]

    # Sample prices dictionary
    prices_dict = {
        'asset1': {'bid_price': 99, 'mid_price': 100, 'ask_price': 101},
        'asset2': {'bid_price': 102, 'mid_price': 103, 'ask_price': 104},
        'asset3': {'bid_price': 104, 'mid_price': 106, 'ask_price': 108}
    }

    # Create a TradeNetter instance and process trades
    trade_netter = TradeNetter(trades, prices_dict)
    processed_trades = trade_netter.process_trades()

    # Display the result
    for trade in processed_trades:
        print(trade)

if __name__ == "__main__":
    main()
