import pandas as pd


def flatten_dict(d, parent_key=(), sep='_'):
    """
    Flatten a nested dictionary. Each level of keys is joined with `sep`.
    The function is recursive.
    
    Parameters:
    - d (dict): The dictionary to flatten.
    - parent_key (tuple): The prefix corresponding to the upper levels of keys.
    - sep (str): The separator between keys; used when concatenating keys.
    
    Returns:
    - A flattened dictionary where keys are tuples representing paths.
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + (k,)
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
