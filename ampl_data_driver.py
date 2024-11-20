# Define a configuration dictionary
config = {
    "num_stocks": 100,
    "num_sectors": 5,
    "budget": 1,
    "r_min": 0.08,
    "max_sector_allocation": 0.3,
    "seed": 42
}

# Create a Portfolio instance
portfolio = Portfolio(config)

# Write portfolio data to a file
portfolio.write_to_dat_file("portfolio.dat")
