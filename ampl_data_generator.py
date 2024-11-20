import numpy as np
import random
from typing import Dict


class Portfolio:
    def __init__(self, config: Dict):
        """
        Initialize the Portfolio object with a configuration dictionary.

        Args:
            config (Dict): Configuration dictionary containing portfolio parameters.
        """
        # Store the entire configuration dictionary as an instance variable
        self.config = config

        # Initialize portfolio data
        self.stocks = self._generate_stocks()
        self.covariance_matrix = self._generate_covariance_matrix()
        self.expected_returns = self._generate_expected_returns()
        self.sectors = self._assign_sectors()

    def _generate_stocks(self):
        """
        Generate a list of stock identifiers.

        Returns:
            List[str]: List of stock identifiers (e.g., ['Stock1', 'Stock2', ...]).
        """
        num_stocks = self.config.get("num_stocks", 100)
        return [f"Stock{i}" for i in range(1, num_stocks + 1)]

    def _generate_covariance_matrix(self):
        """
        Generate a positive semi-definite covariance matrix.

        Returns:
            np.ndarray: Positive semi-definite covariance matrix.
        """
        num_stocks = self.config.get("num_stocks", 100)
        seed = self.config.get("seed", 42)
        np.random.seed(seed)
        random_matrix = np.random.uniform(0.01, 0.05, size=(num_stocks, num_stocks))
        return np.dot(random_matrix, random_matrix.T)  # Ensure PSD matrix

    def _generate_expected_returns(self):
        """
        Generate random expected returns for stocks.

        Returns:
            List[float]: List of expected returns for each stock.
        """
        num_stocks = self.config.get("num_stocks", 100)
        seed = self.config.get("seed", 42)
        np.random.seed(seed)
        return np.random.uniform(0.05, 0.2, num_stocks)

    def _assign_sectors(self):
        """
        Randomly assign stocks to sectors.

        Returns:
            List[str]: Sector assignment for each stock.
        """
        num_stocks = self.config.get("num_stocks", 100)
        num_sectors = self.config.get("num_sectors", 5)
        seed = self.config.get("seed", 42)
        random.seed(seed)
        return [f"Sector{random.randint(1, num_sectors)}" for _ in range(num_stocks)]

    def write_to_dat_file(self, filename: str):
        """
        Write the portfolio data to an AMPL-compatible `.dat` file.

        Args:
            filename (str): Path to the output `.dat` file.
        """
        with open(filename, 'w') as f:
            # Write the set of stocks
            f.write("set STOCKS := " + " ".join(self.stocks) + ";\n\n")

            # Write portfolio parameters
            f.write(f"param B := {self.config.get('budget', 1)};\n")
            f.write(f"param r_min := {self.config.get('r_min', 0.08)};\n")
            f.write(f"param max_sector_allocation := {self.config.get('max_sector_allocation', 0.3)};\n\n")

            # Write expected returns
            f.write("param mu :=\n")
            for stock, mu in zip(self.stocks, self.expected_returns):
                f.write(f"  {stock} {mu:.6f}\n")
            f.write(";\n\n")

            # Write covariance matrix
            f.write("param Q : " + " ".join(self.stocks) + " :=\n")
            for i, stock_i in enumerate(self.stocks):
                f.write(f"  {stock_i} " + " ".join(f"{self.covariance_matrix[i, j]:.6f}" for j in range(len(self.stocks))) + "\n")
            f.write(";\n\n")

            # Write sector assignments
            f.write("param sector :=\n")
            for stock, sector in zip(self.stocks, self.sectors):
                f.write(f"  {stock} {sector}\n")
            f.write(";\n")
