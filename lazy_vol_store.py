import numpy as np
import pandas as pd
from collections import OrderedDict
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator


class VolSurface:
    def __init__(self, points: np.ndarray, vols: np.ndarray):
        self.linear = LinearNDInterpolator(points, vols)
        self.nearest = NearestNDInterpolator(points, vols)

    @classmethod
    def from_frame(cls, g: pd.DataFrame):
        points = g[["days", "moneyness"]].to_numpy(float)
        vols = g["volatility"].to_numpy(float)
        return cls(points, vols)

    def interpolate(self, days: float, moneyness: float) -> float:
        vol = self.linear(days, moneyness)

        if np.isnan(vol):
            vol = self.nearest(days, moneyness)

        return float(vol)


class LazyVolStore:
    def __init__(self, df: pd.DataFrame, max_cache_size: int | None = None):
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])

        self.df = df.set_index(
            ["date", "ticker", "option_type"]
        ).sort_index()

        self.cache = OrderedDict()
        self.max_cache_size = max_cache_size

    def get_vol(
        self,
        date,
        ticker: str,
        option_type: str,
        days: float,
        moneyness: float,
    ) -> float:
        key = (pd.Timestamp(date), ticker, option_type)
        surface = self._get_surface(key)
        return surface.interpolate(days, moneyness)

    def _get_surface(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]

        try:
            g = self.df.loc[key]
        except KeyError as exc:
            raise KeyError(f"No vol surface for {key}") from exc

        surface = VolSurface.from_frame(g)

        self.cache[key] = surface
        self.cache.move_to_end(key)

        if self.max_cache_size is not None and len(self.cache) > self.max_cache_size:
            self.cache.popitem(last=False)

        return surface

    def clear_cache(self):
        self.cache.clear()
