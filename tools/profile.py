"""Generate profile report after running
python -m cProfile -o output.pstats <my-script>.py
"""
import pstats

# Create a Stats object
stats = pstats.Stats('output.pstats')

# Strip off the lengthy directory names
stats.strip_dirs()

# Sort statistics by the cumulative time spent in the function
# stats.sort_stats('cumulative')
stats.sort_stats('tottime')

# Display the stats
stats.print_stats()
