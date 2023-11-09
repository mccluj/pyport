class Backtester:
    def __init__(self, portfolio, market_data, rebalancing_rules):
        self.portfolio = portfolio
        self.market_data = market_data
        self.rebalancing_rules = rebalancing_rules

    def run(self, start_date, end_date):
        current_date = start_date
        while current_date <= end_date:
            # Assume we have a function to fetch new market data for the current date
            new_market_data = self.fetch_market_data_for_date(current_date)
            self.market_data.update(new_market_data)

            self.portfolio.calculate_metrics(self.market_data.data)
            actions = self.rebalancing_rules.determine_actions(self.portfolio.metrics, self.portfolio, self.market_data)
            self.portfolio.update_holdings(actions)

            self.report(current_date, self.portfolio.metrics, actions)
            current_date += timedelta(days=1)

    def fetch_market_data_for_date(self, date):
        # Placeholder for fetching market data logic
        pass

    def report(self, date, metrics, actions):
        # Placeholder for reporting logic
        pass
