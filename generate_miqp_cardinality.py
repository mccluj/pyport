import numpy as np
import random


def generate_stock_set(num_stocks):
    """Generate a list of stock identifiers."""
    return [f"Stock{i}" for i in range(1, num_stocks + 1)]


def generate_covariance_matrix(num_stocks, seed=42):
    """
    Generate a positive semi-definite covariance matrix.
    
    Args:
        num_stocks (int): Number of stocks in the portfolio.
        seed (int): Random seed for reproducibility.

    Returns:
        np.ndarray: Covariance matrix of size (num_stocks, num_stocks).
    """
    np.random.seed(seed)
    P = np.random.uniform(0.01, 0.05, size=(num_stocks, num_stocks))
    covariance_matrix = np.dot(P, P.T)  # Create a PSD matrix
    return covariance_matrix


def generate_expected_returns(num_stocks, low=0.05, high=0.20, seed=42):
    """
    Generate random expected returns for stocks.
    
    Args:
        num_stocks (int): Number of stocks in the portfolio.
        low (float): Minimum return value.
        high (float): Maximum return value.
        seed (int): Random seed for reproducibility.

    Returns:
        list: List of expected returns for each stock.
    """
    np.random.seed(seed)
    return np.random.uniform(low, high, num_stocks)


def assign_sectors(num_stocks, num_sectors, seed=42):
    """
    Randomly assign stocks to sectors.
    
    Args:
        num_stocks (int): Number of stocks in the portfolio.
        num_sectors (int): Number of sectors.
        seed (int): Random seed for reproducibility.

    Returns:
        list: A list of sector assignments for each stock.
    """
    random.seed(seed)
    return [f"Sector{random.randint(1, num_sectors)}" for _ in range(num_stocks)]


def save_to_dat_file(file_path, stocks, covariance_matrix, expected_returns, sectors, max_sector_allocation, budget, min_return, cardinality):
    """
    Save the generated data to a `.dat` file in AMPL format.
    
    Args:
        file_path (str): Path to the output `.dat` file.
        stocks (list): List of stock identifiers.
        covariance_matrix (np.ndarray): Covariance matrix.
        expected_returns (list): List of expected returns.
        sectors (list): Sector assignments for each stock.
        max_sector_allocation (float): Maximum allocation for any sector.
        budget (float): Total portfolio budget.
        min_return (float): Minimum required portfolio return.
        cardinality (int): Maximum number of stocks in the portfolio.
    """
    with open(file_path, 'w') as f:
        # Write the set of stocks
        f.write("set STOCKS := " + " ".join(stocks) + ";\n\n")

        # Write the budget parameter
        f.write(f"param B := {budget};\n\n")

        # Write the minimum return parameter
        f.write(f"param r_min := {min_return};\n\n")

        # Write the cardinality parameter
        f.write(f"param k := {cardinality};\n\n")

        # Write the expected returns
        f.write("param mu :=\n")
        for stock, mu in zip(stocks, expected_returns):
            f.write(f"  {stock} {mu:.6f}\n")
        f.write(";\n\n")

        # Write the covariance matrix
        f.write("param Q : " + " ".join(stocks) + " :=\n")
        for i, stock_i in enumerate(stocks):
            f.write(f"  {stock_i} " + " ".join(f"{covariance_matrix[i, j]:.6f}" for j in range(len(stocks))) + "\n")
        f.write(";\n\n")

        # Write the set of sectors
        unique_sectors = sorted(set(sectors))
        f.write("set SECTORS := " + " ".join(unique_sectors) + ";\n\n")

        # Write the sector assignments
        f.write("param sector :=\n")
        for stock, sector in zip(stocks, sectors):
            f.write(f"  {stock} {sector}\n")
        f.write(";\n\n")

        # Write the maximum sector allocation parameter
        f.write(f"param max_sector_allocation := {max_sector_allocation};\n")


def main():
    # Parameters
    num_stocks = 100  # Number of stocks
    num_sectors = 5   # Number of sectors
    budget = 1        # Total budget
    min_return = 0.08  # Minimum required return
    cardinality = 10  # Maximum number of stocks
    max_sector_allocation = 0.3  # Max allocation per sector

    # Generate data
    stocks = generate_stock_set(num_stocks)
    covariance_matrix = generate_covariance_matrix(num_stocks)
    expected_returns = generate_expected_returns(num_stocks)
    sectors = assign_sectors(num_stocks, num_sectors)

    # Save to AMPL .dat file
    file_path = "portfolio.dat"
    save_to_dat_file(file_path, stocks, covariance_matrix, expected_returns, sectors, max_sector_allocation, budget, min_return, cardinality)
    print(f"Generated data saved to {file_path}")


if __name__ == "__main__":
    main()
