import unittest
import pandas as pd

class TestRateEngine(unittest.TestCase):
    def setUp(self):
        # Sample DataFrame with date, tenor, and rate columns
        data = {
            'date': ['2023-08-01', '2023-08-02', '2023-08-03'],
            'tenor': [[30, 60, 90], [45, 75, 105], [60, 90, 120]],
            'rate': [[0.02, 0.025, 0.03], [0.022, 0.027, 0.032], [0.023, 0.028, 0.033]]
        }
        self.discount_rates_df = pd.DataFrame(data)
        self.engine = RateEngine(self.discount_rates_df)

    def test_interpolation(self):
        # Test interpolation with sample data
        interpolated_rate = self.engine.get_rate('2023-08-01', 75)
        self.assertAlmostEqual(interpolated_rate, 0.0275, places=4)

    def test_extrapolation(self):
        # Extrapolate below the data range (flat extrapolation)
        interpolated_rate = self.engine.get_rate('2023-08-01', 15)
        self.assertAlmostEqual(interpolated_rate, 0.02, places=4)

        # Extrapolate above the data range (flat extrapolation)
        interpolated_rate = self.engine.get_rate('2023-08-01', 150)
        self.assertAlmostEqual(interpolated_rate, 0.03, places=4)

    def test_missing_date(self):
        # Test when the provided date is not in the data
        with self.assertRaises(ValueError):
            self.engine.get_rate('2023-08-04', 75)

if __name__ == '__main__':
    unittest.main()
