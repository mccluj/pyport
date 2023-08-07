import numpy as np
from scipy.interpolate import interp1d

class RateEngine:
    """
    A class for interpolating discount rates based on tenor in days.

    Parameters:
    ----------
    discount_rates : dict
        A dictionary containing tenor in days as keys and corresponding discount rates as values.

    Attributes:
    -----------
    tenors : array_like
        An array containing the sorted tenor values.
    rates : array_like
        An array containing the corresponding sorted discount rate values.
    interp_func : scipy.interpolate.interp1d
        The interpolation function based on the input discount rates.

    Methods:
    --------
    get_rate(tenor: float) -> float:
        Returns the interpolated discount rate for the given tenor in days.
    """

    def __init__(self, discount_rates):
        self.tenors, self.rates = zip(*sorted(discount_rates.items()))
        self.interp_func = interp1d(self.tenors, self.rates, kind='linear', fill_value='extrapolate')

    def get_rate(self, tenor):
        """
        Get the interpolated discount rate for the given tenor in days.

        Parameters:
        -----------
        tenor : float
            The tenor for which the discount rate needs to be interpolated.

        Returns:
        --------
        float
            The interpolated discount rate.
        """
        return self.interp_func(tenor)


# Unit tests for RateEngine class
import unittest

class TestRateEngine(unittest.TestCase):
    def test_interpolation(self):
        # Test interpolation with sample data
        discount_rates = {30: 0.02, 60: 0.025, 180: 0.03, 365: 0.035}
        engine = RateEngine(discount_rates)

        # Interpolate within the data range
        self.assertAlmostEqual(engine.get_rate(90), 0.0275, places=4)

        # Extrapolate below the data range (flat extrapolation)
        self.assertAlmostEqual(engine.get_rate(15), 0.02, places=4)

        # Extrapolate above the data range (flat extrapolation)
        self.assertAlmostEqual(engine.get_rate(500), 0.035, places=4)

    def test_single_rate(self):
        # Test when there's only one rate in the data
        discount_rates = {90: 0.03}
        engine = RateEngine(discount_rates)

        # Interpolate at the single data point (should return the same rate)
        self.assertAlmostEqual(engine.get_rate(90), 0.03, places=4)

        # Extrapolate below the data range (flat extrapolation)
        self.assertAlmostEqual(engine.get_rate(30), 0.03, places=4)

        # Extrapolate above the data range (flat extrapolation)
        self.assertAlmostEqual(engine.get_rate(180), 0.03, places=4)

if __name__ == '__main__':
    unittest.main()
