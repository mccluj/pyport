# Define sets and parameters
set STOCKS;

param expected_return{STOCKS};
param transaction_cost{STOCKS};
param initial_position{STOCKS};

# Define decision variables
var buy{STOCKS} >= 0;
var sell{STOCKS} >= 0;
var hold{STOCKS};
var buy_indicator{STOCKS}, binary;

# Objective: Maximize portfolio return
maximize total_return:
    sum {s in STOCKS} (expected_return[s] * hold[s] - transaction_cost[s] * (buy[s] + sell[s]));

# Constraints
subject to
    # Holdings update
    holdings_update{s in STOCKS}:
        hold[s] = initial_position[s] + buy[s] - sell[s];

    # Ensure buy or sell but not both using the single indicator
    buy_link{s in STOCKS}:
        buy[s] <= M * buy_indicator[s];

    sell_link{s in STOCKS}:
        sell[s] <= M * (1 - buy_indicator[s]);

# Big M should be a large number
param M := 10000;
