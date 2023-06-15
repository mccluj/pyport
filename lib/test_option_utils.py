from pyport.lib.black_scholes import black_scholes
from pyport.lib.option_utils import implied_strike

def test_implied_strike():
    # Test inputs
    option_price = 10.35
    current_price = 100.0
    risk_free_rate = 0.05
    time_to_expiration = 0.5
    volatility = 0.2
    dividend_rate = 0.0
    option_type = 'call'
    tolerance = 1e-6

    # Calculate implied strike
    implied_strike_price = implied_strike(option_price, current_price, risk_free_rate, time_to_expiration,
                                          volatility, dividend_rate, option_type)

    # Calculate option price using the implied strike
    option = black_scholes(current_price, implied_strike_price, risk_free_rate, time_to_expiration,
                           volatility, dividend_rate, option_type)
    calculated_option_price = option['price']

    # Check if calculated option price matches the original option price within tolerance
    assert abs(calculated_option_price - option_price) < tolerance, "Test failed: Option prices do not match"

    print("Unit test passed successfully.")


# Run the unit test
test_implied_strike()
