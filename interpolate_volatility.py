import pandas as pd
import numpy as np

def interpolate_volatility(df, target_days, target_moneyness):
    # Step 1: Identify nearest columns
    # Find the days to expiration closest to but less than or equal to target_days
    lower_day = df.columns[df.columns <= target_days].max()
    # Find the days to expiration closest to but greater than or equal to target_days
    upper_day = df.columns[df.columns >= target_days].min()

    # Step 2: 1D Interpolation for each column
    def interpolate_1d(col, target_moneyness):
        # Interpolate within this column for the target moneyness
        return np.interp(target_moneyness, df.index, df[col])

    lower_vol = interpolate_1d(lower_day, target_moneyness)
    upper_vol = interpolate_1d(upper_day, target_moneyness)

    # Step 3: Weighted Average
    if lower_day != upper_day:
        # Weight by inverse of distance to target_days
        total_interval = upper_day - lower_day
        weight_lower = (upper_day - target_days) / total_interval
        weight_upper = (target_days - lower_day) / total_interval
        final_vol = lower_vol * weight_lower + upper_vol * weight_upper
    else:
        # If the target_days is exactly one of the columns, use that column's value
        final_vol = lower_vol  # or upper_vol, they are the same in this case

    return final_vol

# Example DataFrame
data = {
    10: {0.9: 0.15, 1.0: 0.12, 1.1: 0.10},
    20: {0.9: 0.16, 1.0: 0.13, 1.1: 0.11},
    30: {0.9: 0.17, 1.0: 0.14, 1.1: 0.12}
}
df = pd.DataFrame(data)

# Example usage
target_days = 15
target_moneyness = 1.05
interpolated_volatility = interpolate_volatility(df, target_days, target_moneyness)
print("Interpolated Volatility:", interpolated_volatility)
