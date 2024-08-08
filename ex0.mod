set Stocks;
param M;  # A sufficiently large constant
param max_investment;
param min_return{Stocks};
param expected_return{Stocks};
param risk{Stocks};
param max_risk{Stocks};

var weights{Stocks};
var long_weights{Stocks} >= 0;
var is_positive{Stocks} binary;

# Objective: Maximize total return
maximize TotalReturn:
    sum {i in Stocks} expected_return[i] * long_weights[i];

# Constraints
s.t. BudgetConstraint:
    sum{i in Stocks} long_weights[i] <= max_investment;

s.t. ReturnConstraint{i in Stocks}:
    expected_return[i] * long_weights[i] >= min_return[i];

s.t. RiskConstraint{i in Stocks}:
    risk[i] * long_weights[i] <= max_risk[i];

# Binary variable constraints
s.t. LongWeightsDef{i in Stocks}:
    long_weights[i] = weights[i] * is_positive[i];

s.t. PositiveWeights{i in Stocks}:
    weights[i] >= long_weights[i];

s.t. IndicatorPositive{i in Stocks}:
    weights[i] <= M * is_positive[i];

s.t. IndicatorZero{i in Stocks}:
    weights[i] >= -M * (1 - is_positive[i]);
