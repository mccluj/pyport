# Sets
set STOCKS;                  # Set of stocks
set SECTORS;                 # Set of sectors

# Parameters
param B;                     # Total budget (usually 1 for a normalized portfolio)
param r_min;                 # Minimum required portfolio return
param k;                     # Maximum number of stocks allowed in the portfolio
param max_sector_allocation; # Maximum allocation to any single sector

param mu {STOCKS};           # Expected returns for each stock
param Q {STOCKS, STOCKS};    # Covariance matrix of stock returns
param sector {STOCKS} symbolic; # Sector assignment for each stock (symbolic)

# Decision variables
var x {STOCKS} >= 0;         # Portfolio weights for each stock
var z {STOCKS} binary;       # Binary variable: 1 if stock is included in the portfolio, 0 otherwise

# Objective: Minimize portfolio risk (variance)
minimize PortfolioRisk:
    sum {i in STOCKS, j in STOCKS} Q[i, j] * x[i] * x[j];

# Constraints
subject to BudgetConstraint:
    sum {i in STOCKS} x[i] = B;

subject to ReturnConstraint:
    sum {i in STOCKS} mu[i] * x[i] >= r_min;

subject to CardinalityConstraint:
    sum {i in STOCKS} z[i] <= k;

subject to LogicalLink {i in STOCKS}:
    x[i] <= z[i];  # Ensure weights are 0 if a stock is not selected

# Sector Constraint: Limit allocation per sector
subject to SectorConstraint {s in SECTORS}:
    sum {i in STOCKS: sector[i] = s} x[i] <= max_sector_allocation;
