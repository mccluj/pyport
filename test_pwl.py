from amplpy import AMPL

def test_ampl_pwl():
    # Initialize the AMPL object
    ampl = AMPL()

    # Define the PWL structure in AMPL model as a string
    ampl_model = """
    param n integer > 0;  # Number of breakpoints
    param x{1..n};  # X-coordinates of breakpoints
    param y{1..n};  # Y-coordinates of breakpoints

    # Ensure x is sorted in ascending order
    check {i in 1..n-1}: x[i] < x[i+1];

    var z;  # Decision variable
    var f;  # Value of the PWL function at z

    minimize obj: f;  # Objective to minimize

    s.t. PWLConstraint: f = <<x, y>>(z);
    """

    # Load the model into AMPL
    ampl.eval(ampl_model)

    # Test data for PWL structure
    n = 5  # Number of breakpoints
    x = [1, 2, 3, 4, 5]  # X-coordinates of breakpoints
    y = [1, 4, 9, 16, 25]  # Y-coordinates of breakpoints

    # Set data in AMPL
    ampl.param['n'] = n
    ampl.param['x'] = x
    ampl.param['y'] = y

    # Solve the model with a test value for z
    ampl.eval("let z := 2.5;")
    ampl.solve()

    # Retrieve results
    f_value = ampl.getVariable('f').value()
    z_value = ampl.getVariable('z').value()

    print(f"PWL function value at z = {z_value}: f = {f_value}")

# Run the test
test_ampl_pwl()
