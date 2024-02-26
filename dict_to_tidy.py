import pandas as pd

def dict_to_tidy(df, current_path=None, current_data=None):
    """
    Recursively traverses a nested dictionary to collect paths and values,
    converting them into a format suitable for a tidy DataFrame.

    :param df: The nested dictionary to convert.
    :param current_path: The accumulated path keys, representing column labels.
    :param current_data: Accumulated data rows.
    :return: A list of dictionaries, where each dictionary represents a row in the tidy DataFrame.
    """
    if current_path is None:
        current_path = []
    if current_data is None:
        current_data = []

    if isinstance(df, dict):
        for key, value in df.items():
            # Recurse into the dictionary, adding the current key to the path
            dict_to_tidy(value, current_path + [key], current_data)
    else:
        # At a leaf node, construct a row from the path and the leaf node value
        data_row = {path_key: path_value for path_key, path_value in zip(current_path, current_path)}
        data_row['value'] = df  # Assuming the final value is what we want to capture
        current_data.append(data_row)

    return current_data

# Example nested dictionary
nested_dict = {
    '2023': {
        'January': {
            'Sales': 150,
            'Expenses': 100,
        },
        'February': {
            'Sales': 200,
            'Expenses': 150,
        },
    },
    '2024': {
        'January': {
            'Sales': 180,
            'Expenses': 130,
        },
    },
}

# Convert the nested dictionary to a tidy format
tidy_data = dict_to_tidy(nested_dict)

# Convert the list of dictionaries to a DataFrame
tidy_df = pd.DataFrame(tidy_data)

print(tidy_df)
