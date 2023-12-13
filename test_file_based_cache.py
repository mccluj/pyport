import os
import pytest
from your_module import expensive_computation  # Replace with actual import

def test_expensive_computation_caching():
    """
    Test the caching mechanism of the expensive_computation function.
    It verifies if the function output is correctly cached and retrieved.
    """
    # Clear cache before test
    cache_dir = 'cache'
    if os.path.exists(cache_dir):
        for f in os.listdir(cache_dir):
            os.remove(os.path.join(cache_dir, f))

    # First call should compute the result
    result1 = expensive_computation(2, 3)
    assert result1 == 8, "First computation should return the correct result"

    # Second call should retrieve the result from cache
    result2 = expensive_computation(2, 3)
    assert result2 == 8, "Second computation should retrieve result from cache"

    # Verify that a cache file was created
    cache_file = os.path.join(cache_dir, 'expensive_computation_{}.pkl'.format(
        hashlib.md5(b'(2, 3)()').hexdigest()
    ))
    assert os.path.exists(cache_file), "Cache file should exist"
