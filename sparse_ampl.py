from amplpy import AMPL
import os

def convert_to_sparse(model_file, data_file, matrix_parameters, output_file):
    """
    Converts full matrix parameters to sparse matrix parameters in an AMPL model.

    :param model_file: Path to the AMPL model file (.mod)
    :param data_file: Path to the AMPL data file (.dat)
    :param matrix_parameters: List of full matrix parameter names to convert
    :param output_file: Path to save the updated sparse data file
    """
    # Initialize AMPL
    ampl = AMPL()
    
    # Load the model and data
    ampl.read(model_file)
    ampl.read_data(data_file)
    
    # Process each matrix parameter
    for param_name in matrix_parameters:
        # Get the full matrix parameter
        param = ampl.get_parameter(param_name)
        data = param.get_values().to_list()  # Convert to a list of tuples [(index1, index2, value), ...]
        
        # Create a sparse representation (excluding zero values)
        sparse_data = [(i, j, v) for i, j, v in data if v != 0]
        
        # Define a set for the sparse parameter indices
        sparse_set_name = f"{param_name}_indices"
        ampl.eval(f"set {sparse_set_name} within {{i, j}};")
        
        # Populate the set with valid indices
        sparse_indices = [(i, j) for i, j, _ in sparse_data]
        sparse_set = ampl.get_set(sparse_set_name)
        sparse_set.set_values(sparse_indices)
        
        # Define the sparse parameter with the new domain set
        sparse_param_name = f"{param_name}_sparse"
        ampl.eval(f"param {sparse_param_name} {{({sparse_set_name})}};")
        
        # Set the values for the sparse parameter
        sparse_param = ampl.get_parameter(sparse_param_name)
        sparse_param.set_values(sparse_data)
        
        # Optionally remove the original parameter if no longer needed
        # ampl.eval(f"drop param {param_name};")
        
    # Write the updated data to a file
    ampl.write_data(output_file)

    print(f"Updated data with sparse parameters and domain sets saved to {output_file}")


# Example usage
model_file = "model.mod"        # Path to your AMPL model file
data_file = "data.dat"          # Path to your AMPL data file
matrix_parameters = ["A", "B"]  # List of matrix parameter names to convert
output_file = "sparse_data.dat" # Path to save the updated sparse data

convert_to_sparse(model_file, data_file, matrix_parameters, output_file)
