# Define the solver
option solver cplex;

# Set CPLEX options
option cplex_options 'mipgap=0.01 mipemphasis=1 heuristicfreq=10 timelimit=300';

# Model variables, constraints, and objective
var x{i in ASSETS} >= 0;           # Portfolio weights
var z{i in ASSETS} binary;        # Binary inclusion variables

minimize PortfolioRisk:
    sum {i in ASSETS, j in ASSETS} Q[i,j] * x[i] * x[j];

subject to Budget:
    sum {i in ASSETS} x[i] = 1;

subject to ReturnConstraint:
    sum {i in ASSETS} mu[i] * x[i] >= r_min;

subject to CardinalityConstraint:
    sum {i in ASSETS} z[i] <= k;

subject to LogicalLink{i in ASSETS}:
    x[i] <= z[i];

# Solve the problem
solve;

# Display results
display x, z;
