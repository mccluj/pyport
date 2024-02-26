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

    # Check if the current item is a dictionary (to continue recursion) or a leaf node (to collect data)
    if isinstance(df, dict):
        for key, value in df.items():
            # Recurse into the dictionary, adding the current key to the path
            dict_to_tidy(value, current_path + [key], current_data)
    else:
        # At a leaf node, combine the path with the leaf node value into a single dictionary
        current_data.append({**{path[i]: val for i, val in enumerate(current_path)}, 'value': df})

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
