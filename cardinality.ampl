set ASSETS;
param C;  # Maximum "sparsity" (approximate cardinality)
param returns {ASSETS};  # Expected returns
param cov {ASSETS, ASSETS};  # Covariance matrix for risk
param risk_limit;  # Maximum allowable risk

var x {ASSETS} >= 0;  # Fraction of portfolio allocated to each asset
var s {ASSETS} >= 0;  # Slack variables to approximate sparsity

# Objective: Maximize expected return (modify if needed)
maximize TotalReturn:
    sum {i in ASSETS} returns[i] * x[i];

# Risk constraint
subject to RiskConstraint:
    sum {i in ASSETS, j in ASSETS} cov[i,j] * x[i] * x[j] <= risk_limit;

# Sparsity approximation: linking x[i] and s[i]
subject to SparsityLinking {i in ASSETS}:
    s[i] >= x[i];

# Cardinality approximation
subject to CardinalityConstraint:
    sum {i in ASSETS} s[i] <= C;

# Budget constraint
subject to Budget:
    sum {i in ASSETS} x[i] = 1;
