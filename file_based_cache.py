import os
import pandas as pd
import hashlib
import functools

def file_based_cache(directory='cache'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache directory if it doesn't exist
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Generate a unique key for the arguments
            arg_hash = hashlib.md5(str(args).encode() + str(kwargs).encode()).hexdigest()
            file_path = os.path.join(directory, f"{func.__name__}_{arg_hash}.pkl")

            # Check if the result is cached
            if os.path.exists(file_path):
                # Load and return the cached result
                return pd.read_pickle(file_path)

            # Execute the function and cache the result
            result = func(*args, **kwargs)
            pd.to_pickle(result, file_path)
            return result

        return wrapper
    return decorator

# Example usage
@file_based_cache()
def expensive_computation(a, b):
    # Simulate an expensive computation
    return a ** b

# The first call will compute and cache the result
result = expensive_computation(2, 10)

# Subsequent calls with the same arguments will use the cached result
result = expensive_computation(2, 10)
