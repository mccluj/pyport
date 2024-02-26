from collections import namedtuple

# Define the structure of your named tuple
Record = namedtuple('Record', 'outcome_period date asset category feature value')

def flatten_nested_dict(nested_dict):
    records = []

    # Iterate through the levels of nesting
    for outcome_period, dates in nested_dict.items():
        for date, assets in dates.items():
            for asset, categories in assets.items():
                for category, features in categories.items():
                    for feature, value in features.items():
                        # For each combination, create a Record instance
                        record = Record(outcome_period, date, asset, category, feature, value)
                        records.append(record)
    
    return records

# Example nested dictionary
nested_dict = {
    'Q1': {
        '2023-01-01': {
            'Asset1': {
                'CategoryA': {
                    'Feature1': 100,
                    'Feature2': 200,
                }
            },
            'Asset2': {
                'CategoryB': {
                    'Feature3': 300,
                }
            },
        },
    },
}

# Convert to list of named tuples
records = flatten_nested_dict(nested_dict)

# Example output
for record in records:
    print(record)
