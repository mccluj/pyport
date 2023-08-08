import pandas as pd
from scipy.interpolate import interp1d

class RateEngine:
    def __init__(self, dataframe):
        # Assuming the DataFrame has columns 'date', 'days', and 'rate'
        self.df = dataframe
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df.sort_values(by=['date', 'days'], inplace=True)
    
    def get_rate(self, target_date):
        target_date = pd.to_datetime(target_date)
        # Get the rows for the specific date
        filtered_data = self.df[self.df['date'] == target_date]
        
        if filtered_data.empty:
            return None
        
        interpolation_function = interp1d(filtered_data['days'], filtered_data['rate'], kind='linear', fill_value="extrapolate")
        
        # You can interpolate based on the days you want
        desired_days = filtered_data['days'].iloc[0] # Modify this as needed
        rate = interpolation_function(desired_days)
        
        return rate

# Sample DataFrame
data = {'date': ['2022-01-01', '2022-01-01', '2022-06-01', '2022-06-01', '2022-12-01', '2022-12-01'],
        'days': [0, 5, 150, 155, 365, 370],
        'rate': [2.0, 2.1, 2.5, 2.6, 3.0, 3.1]}

df = pd.DataFrame(data)

engine = RateEngine(df)

# Get the rate for a given date
date = '2022-06-01'
rate = engine.get_rate(date)
print(f"Interpolated rate for {date}: {rate}")
