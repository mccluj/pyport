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
        self.interp_functions = self._create_interp_functions()

    def _create_interp_functions(self):
        interp_functions = {}

        def create_interp_function(group):
            return interp1d(group['tenor'], group['rate'], kind='linear', fill_value='extrapolate')

        grouped = self.discount_rates.groupby('date')
        for date, group in grouped:
            interp_functions[date] = create_interp_function(group)

        return interp_functions

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
        if date in self.interp_functions:
            return self.interp_functions[date](tenor)
        else:
            raise ValueError(f"No matching rate data found for date: {date}")
