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

data;
set ASSETS := A1 A2 A3 A4;

# Expected returns for each asset
param returns :=
  A1 0.12
  A2 0.10
  A3 0.08
  A4 0.07;

# Covariance matrix for asset returns (symmetric)
param cov (tr):
       A1      A2      A3      A4 :=
  A1   0.10    0.02    0.01    0.03
  A2   0.02    0.08    0.01    0.02
  A3   0.01    0.01    0.05    0.01
  A4   0.03    0.02    0.01    0.07;

# Maximum allowable risk (variance)
param risk_limit := 0.04;

# Cardinality constraint approximation parameter
param C := 0.8;

# Budget constraint is implicit in the model (sum of x[i] = 1)
