### --- CORE DEFINITIONS ---
# Sets, parameters, variables
include core.mod;

### --- LOT ACCOUNTING & TAX IMPACT ---
include lot_accounting.mod;

### --- POSITION & WASH-SALE LOGIC ---
include position_computation.mod;

### --- AUM CONSTRAINTS ---
include aum_constraints.mod;

### --- OBJECTIVE FUNCTION ---
include objective.mod;
