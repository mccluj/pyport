import pandas as pd

# Example volatility surface data
data = {
    (0.9, 30): 0.20, (1.0, 30): 0.18, (1.1, 30): 0.19,
    (0.9, 60): 0.21, (1.0, 60): 0.19, (1.1, 60): 0.20,
    (0.9, 90): 0.22, (1.0, 90): 0.20, (1.1, 90): 0.21
}
df = pd.DataFrame(list(data.items()), columns=['Moneyness_Days', 'Volatility'])
df[['Moneyness', 'Days']] = pd.DataFrame(df['Moneyness_Days'].tolist(), index=df.index)
df.drop('Moneyness_Days', axis=1, inplace=True)

def interpolate_volatility(moneyness, days):
    # Filter the slices for the given moneyness
    relevant_slices = df[df['Moneyness'] == moneyness]

    # Find the days slice at or below and at or above
    lower_slice = relevant_slices[relevant_slices['Days'] <= days].max()
    upper_slice = relevant_slices[relevant_slices['Days'] >= days].min()

    # Check if exact match
    if lower_slice['Days'] == days:
        return lower_slice['Volatility']
    elif upper_slice['Days'] == days:
        return upper_slice['Volatility']

    # Weighted average
    total_days_gap = upper_slice['Days'] - lower_slice['Days']
    weight_lower = (upper_slice['Days'] - days) / total_days_gap
    weight_upper = (days - lower_slice['Days']) / total_days_gap

    return weight_lower * lower_slice['Volatility'] + weight_upper * upper_slice['Volatility']

# Example usage
moneyness = 1.0
days = 45
volatility = interpolate_volatility(moneyness, days)
print(f"Interpolated Volatility for Moneyness {moneyness} and Days {days}: {volatility}")
