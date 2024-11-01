import re

def convert_small_numbers_to_zero(input_file: str, output_file: str, threshold: float = 1e-8):
    # Regular expression to identify numbers, including scientific notation (e.g., 1e-15)
    number_pattern = re.compile(r"([-+]?\d*\.\d+|\d+)([eE][-+]?\d+)?")
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    modified_lines = []
    for line in lines:
        # Replace each small number with zero if it's below the threshold
        modified_line = number_pattern.sub(lambda match: "0" if abs(float(match.group())) <= threshold else match.group(), line)
        modified_lines.append(modified_line)
    
    with open(output_file, 'w') as f:
        f.writelines(modified_lines)

# Usage:
# convert_small_numbers_to_zero("data.dat", "modified_data.dat")
