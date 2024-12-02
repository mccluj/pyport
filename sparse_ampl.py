from amplpy import AMPL

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
    ampl.readData(data_file)  # Corrected method name
    
    # Process each matrix parameter
    for param_name in matrix_parameters:
        # Get the full matrix parameter
        param = ampl.getParameter(param_name)
        data = param.getValues().toPandas()  # Convert to a Pandas DataFrame
        
        # Filter for non-zero values
        sparse_data = data[data['value'] != 0]  # Keep only non-zero entries
        sparse_indices = sparse_data[['index1', 'index2']].to_records(index=False).tolist()
        sparse_values = sparse_data['value'].tolist()
        
        # Define a set for the sparse parameter indices
        sparse_set_name = f"{param_name}_indices"
        ampl.eval(f"set {sparse_set_name} within {{i, j}};")
        
        # Populate the set with valid indices
        sparse_set = ampl.getSet(sparse_set_name)
        sparse_set.setValues(sparse_indices)
        
        # Define the sparse parameter with the new domain set
        sparse_param_name = f"{param_name}_sparse"
        ampl.eval(f"param {sparse_param_name} {{({sparse_set_name})}};")
        
        # Populate the sparse parameter with its values
        sparse_param = ampl.getParameter(sparse_param_name)
        sparse_param.setValues({tuple(idx): val for idx, val in zip(sparse_indices, sparse_values)})
        
        # Optionally remove the original parameter if no longer needed
        # ampl.eval(f"drop param {param_name};")
        
    # Write the updated data to a file
    ampl.writeData(output_file)  # Corrected method name

    print(f"Updated data with sparse parameters and domain sets saved to {output_file}")


# Example usage
model_file = "model.mod"        # Path to your AMPL model file
data_file = "data.dat"          # Path to your AMPL data file
matrix_parameters = ["A", "B"]  # List of matrix parameter names to convert
output_file = "sparse_data.dat" # Path to save the updated sparse data

convert_to_sparse(model_file, data_file, matrix_parameters, output_file)
