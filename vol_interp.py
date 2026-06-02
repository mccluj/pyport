import numpy as np
import pandas as pd
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator


class VolSurfaceInterpolator:
    def __init__(self, df: pd.DataFrame):
        self.surfaces = {}

        required = {
            "date", "ticker", "option_type",
            "days", "moneyness", "volatility"
        }
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])

        keys = ["date", "ticker", "option_type"]

        for key, g in df.groupby(keys, sort=False):
            points = g[["days", "moneyness"]].to_numpy(float)
            values = g["volatility"].to_numpy(float)

            if len(g) < 3:
                continue

            self.surfaces[key] = {
                "linear": LinearNDInterpolator(points, values),
                "nearest": NearestNDInterpolator(points, values),
            }

    def get_vol(
        self,
        date,
        ticker: str,
        option_type: str,
        days: float,
        moneyness: float,
        fallback: str = "nearest",
    ) -> float:
        key = (pd.Timestamp(date), ticker, option_type)

        if key not in self.surfaces:
            raise KeyError(f"No surface for {key}")

        surf = self.surfaces[key]
        vol = surf["linear"](days, moneyness)

        if np.isnan(vol):
            if fallback == "nearest":
                vol = surf["nearest"](days, moneyness)
            else:
                raise ValueError(
                    f"Point outside interpolation hull: "
                    f"days={days}, moneyness={moneyness}"
                )

        return float(vol)
