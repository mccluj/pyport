# Define sets and parameters
set STOCKS;

param expected_return{STOCKS};
param transaction_cost{STOCKS};
param initial_position{STOCKS};
param max_trade{STOCKS};

# Define decision variables
var long_hold{STOCKS} >= 0 <= max_trade[STOCKS];
var short_hold{STOCKS} >= 0 <= max_trade[STOCKS];
var net_hold{STOCKS};
var long_indicator{STOCKS}, binary;

# Objective: Maximize portfolio return
maximize total_return:
    sum {s in STOCKS} (expected_return[s] * net_hold[s] - transaction_cost[s] * (long_hold[s] + short_hold[s]));

# Constraints
subject to
    # Net holdings update
    net_holdings_update{s in STOCKS}:
        net_hold[s] = initial_position[s] + long_hold[s] - short_hold[s];

    # Ensure long or short but not both using the single indicator
    long_short_exclusivity{s in STOCKS}:
        long_hold[s] <= max_trade[s] * long_indicator[s];

    short_link{s in STOCKS}:
        short_hold[s] <= max_trade[s] * (1 - long_indicator[s]);
