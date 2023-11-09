import pytest
from rebalancing_rules import RebalancingRules
from portfolio import Portfolio
from market_data import MarketData

@pytest.fixture
def mock_portfolio(mocker):
    portfolio = Portfolio(initial_holdings={'index_futures': 10, 'bond_futures': 20})
    mocker.patch.object(portfolio, 'calculate_metrics')
    return portfolio

@pytest.fixture
def mock_market_data(mocker):
    market_data = MarketData(initial_data={
        'index_futures': {'price': 110, 'contract_size': 1, 'delta': 0.5},
        'bond_futures': {'price': 120, 'contract_size': 1, 'duration': 4}
    })
    mocker.patch.object(market_data, 'get_data_for_asset', return_value=market_data.initial_data['index_futures'])
    return market_data

class TestRebalancingRules:
    @pytest.fixture
    def rebalancing_rules(self):
        rules = {
            'index_exposure': {'target_min': 0.5, 'target_max': 0.7},
            'portfolio_duration': {'target_min': 3, 'target_max': 7},
        }
        return RebalancingRules(rules)

    def test_determine_actions_no_action_needed(self, rebalancing_rules, mock_portfolio, mock_market_data):
        mock_portfolio.metrics = {'index_exposure': 0.6, 'portfolio_duration': 5}
        actions = rebalancing_rules.determine_actions(mock_portfolio.metrics, mock_portfolio, mock_market_data)
        assert actions == []  # No action should be taken if within target

    def test_determine_actions_buy_index_futures(self, rebalancing_rules, mock_portfolio, mock_market_data):
        mock_portfolio.metrics = {'index_exposure': 0.4, 'portfolio_duration': 5}
        actions = rebalancing_rules.determine_actions(mock_portfolio.metrics, mock_portfolio, mock_market_data)
        assert 'buy' in actions[0]['transaction']  # Expect a buy transaction

    def test_determine_actions_sell_index_futures(self, rebalancing_rules, mock_portfolio, mock_market_data):
        mock_portfolio.metrics = {'index_exposure': 0.8, 'portfolio_duration': 5}
        actions = rebalancing_rules.determine_actions(mock_portfolio.metrics, mock_portfolio, mock_market_data)
        assert 'sell' in actions[0]['transaction']  # Expect a sell transaction

# Additional tests would go here

if __name__ == "__main__":
    pytest.main()
