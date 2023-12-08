import numpy as np
from scipy.interpolate import interp1d

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def interpolate_volatility(vol_surface, moneyness, days, moneyness_levels, days_levels):
    # Find the indices for the nearest days slices
    idx_below = find_nearest(days_levels[days_levels <= days], days)
    idx_above = find_nearest(days_levels[days_levels >= days], days)

    # Interpolate (or find) volatility for each slice
    interp_below = interp1d(moneyness_levels, vol_surface[:, idx_below], fill_value="extrapolate")
    vol_below = interp_below(moneyness)

    interp_above = interp1d(moneyness_levels, vol_surface[:, idx_above], fill_value="extrapolate")
    vol_above = interp_above(moneyness)

    # Weighted average based on days distance
    total_distance = days_levels[idx_above] - days_levels[idx_below]
    weight_below = (days_levels[idx_above] - days) / total_distance
    weight_above = (days - days_levels[idx_below]) / total_distance

    return vol_below * weight_below + vol_above * weight_above

# Example usage
vol_surface = np.array([[...]])  # Your volatility data
moneyness_levels = np.array([...])  # Your moneyness levels
days_levels = np.array([...])  # Your days levels

vol = interpolate_volatility(vol_surface, target_moneyness, target_days, moneyness_levels, days_levels)
print("Interpolated Volatility:", vol)
