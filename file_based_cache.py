import os
import pandas as pd
import hashlib
import functools

def file_based_cache(directory='cache'):
    """
    A decorator for caching the output of a function using pandas and pickle files.
    It stores the function results on the filesystem and retrieves them when the function
    is called again with the same arguments.

    Args:
    - directory (str): The directory where the cache files will be stored.

    Returns:
    - A wrapper function that implements the caching logic.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Ensure the cache directory exists
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Create a unique hash key based on the function's name and arguments
            arg_hash = hashlib.md5(str(args).encode() + str(kwargs).encode()).hexdigest()
            file_path = os.path.join(directory, f"{func.__name__}_{arg_hash}.pkl")

            # Load and return the result if it's already cached
            if os.path.exists(file_path):
                return pd.read_pickle(file_path)

            # Call the function and save the result to a pickle file
            result = func(*args, **kwargs)
            pd.to_pickle(result, file_path)
            return result

        return wrapper
    return decorator

# Example usage of the decorator
@file_based_cache()
def expensive_computation(a, b):
    """
    Example function that performs an expensive computation.
    
    Args:
    - a (int): A number
    - b (int): Another number
    
    Returns:
    - int: The result of raising a to the power of b
    """
    return a ** b
