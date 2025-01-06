# Number of breakpoints
param n > 0;

# X and Y coordinates of breakpoints
param x{1..n};
param y{1..n};

# Ensure x is strictly increasing
check {i in 1..n-1}: x[i] < x[i+1];

# Decision variable
var z;
var f;

# Objective: Minimize the value of the PWL function at z
minimize TotalCost: f;

# PWL constraint
s.t. PWLFunction: f = <<x, y>>(z);

# Example data
data;
param n := 5;
param x := 1 2 3 4 5;
param y := 1 4 9 16 25;

# Solve the problem
solve;

# Display results
display z, f;
