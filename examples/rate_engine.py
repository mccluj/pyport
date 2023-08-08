import numpy as np
from scipy.interpolate import interp1d
import pandas as pd

class RateEngine:
    """
    A class for interpolating discount rates based on date and tenor in days.

    Parameters:
    ----------
    discount_rates : pd.DataFrame
        A DataFrame containing 'date', 'tenor', and 'rate' columns.

    Methods:
    --------
    get_rate(date: str, tenor: float) -> float:
        Returns the interpolated discount rate for the given date and tenor in days.
    """

    def __init__(self, discount_rates):
        self.discount_rates = discount_rates
        self.interp_func = None
        self.update_interpolator()

    def update_interpolator(self):
        self.interp_func = interp1d(self.discount_rates['tenor'], self.discount_rates['rate'],
                                    kind='linear', fill_value='extrapolate')

    def get_rate(self, date, tenor):
        """
        Get the interpolated discount rate for the given date and tenor in days.

        Parameters:
        -----------
        date : str
            The date for which the discount rate needs to be interpolated (YYYY-MM-DD).
        tenor : float
            The tenor in days for which the discount rate needs to be interpolated.

        Returns:
        --------
        float
            The interpolated discount rate.
        """
        matching_rates = self.discount_rates[self.discount_rates['date'] == date]
        if len(matching_rates) > 0:
            return self.interp_func(tenor)
        else:
            raise ValueError(f"No matching rate data found for date: {date}")


# Sample DataFrame with date, tenor, and rate columns
data = {
    'date': ['2023-08-01', '2023-08-02', '2023-08-03'],
    'tenor': [30, 60, 90],
    'rate': [0.02, 0.025, 0.03]
}
discount_rates_df = pd.DataFrame(data)

# Create an instance of RateEngine
engine = RateEngine(discount_rates_df)

# Test the interpolation
interpolated_rate = engine.get_rate('2023-08-01', 75)
print(f"Interpolated rate: {interpolated_rate:.5f}")
