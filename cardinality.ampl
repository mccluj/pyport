# ======================================================
# mvo_cardinality.mod
# Mean-Variance Optimization with Quadratic Cardinality Penalty
# ======================================================

reset;

########################################################
# 1. MODEL DECLARATIONS
########################################################
set ASSETS;

param mu {ASSETS};          # expected returns
param Sigma {ASSETS,ASSETS};# covariance matrix
param lambda >= 0, <= 1;    # risk aversion parameter
param gamma >= 0;           # penalty weight for cardinality approximation
param epsilon >= 0;         # small constant inside sqrt
param budget;               # sum of weights constraint

var x {i in ASSETS} >= 0;   # portfolio weights (long-only in this example)

# ------------------------------------------------------
# 1.1 Objective Function:
#     Minimize [ λ * (x'Σx)  - (1 - λ)* (μ'x)  + γ * ∑ sqrt(ε + x_i^2 ) ]
# ------------------------------------------------------
minimize MVO_obj:
      lambda * sum {i in ASSETS, j in ASSETS} (x[i] * Sigma[i,j] * x[j])
    - (1 - lambda) * sum {i in ASSETS} (mu[i] * x[i])
    + gamma * sum {i in ASSETS} sqrt(epsilon + x[i]^2);

# ------------------------------------------------------
# 1.2 Constraints
# ------------------------------------------------------
subject to budget_cons:
    sum {i in ASSETS} x[i] = budget;

########################################################
# 2. DATA SECTION
########################################################
data;

set ASSETS := A B C D E;

# Synthetic expected returns
param mu :=
  A  0.12
  B  0.09
  C  0.15
  D  0.07
  E  0.11
;

# Covariance matrix (assumed symmetric, so we use "tr" format)
param Sigma (tr):
      A      B      C      D      E :=
A     0.04   0.006  0.001  0.000  0.000
B            0.05   0.002  0.000  0.000
C                   0.06   0.000  0.000
D                          0.03   0.000
E                                 0.04
;

# Model parameters
param lambda   := 0.5;     # medium risk aversion
param gamma    := 2.0;     # cardinality penalty weight
param epsilon  := 1e-4;    # small constant for sqrt
param budget   := 1.0;

########################################################
# 3. SOLVE
########################################################
option solver cplex;  # or another solver that supports quadratic models
solve;

# 4. REPORT RESULTS
display x;
display sum{i in ASSETS} (abs(x[i]) > 1e-6);  # approximate "active" positions
