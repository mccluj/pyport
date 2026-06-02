from collections import OrderedDict
import pandas as pd


class LazyVolStore:
    def __init__(self, df: pd.DataFrame, max_cache_size: int | None = None):
        self.df = df.copy()
        self.df["date"] = pd.to_datetime(self.df["date"])

        self.df = self.df.set_index(["date", "ticker", "option_type"]).sort_index()

        self.cache = OrderedDict()
        self.max_cache_size = max_cache_size

    def get_vol(self, date, ticker, option_type, days, moneyness) -> float:
        key = (pd.Timestamp(date), ticker, option_type)

        surface = self._get_surface(key)

        return surface.interpolate(days, moneyness)

    def _get_surface(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]

        surface = self._build_surface(key)

        self.cache[key] = surface
        self.cache.move_to_end(key)

        if self.max_cache_size is not None and len(self.cache) > self.max_cache_size:
            self.cache.popitem(last=False)

        return surface

    def _build_surface(self, key):
        try:
            g = self.df.loc[key]
        except KeyError:
            raise KeyError(f"No volatility surface for {key}")

        return VolSurface.from_frame(g)
