"""Placeholder for the feature engineering functions."""
from math import sqrt

import pandas as pd


def volatility(price_series: pd.Series, rolling_period: int = 14) -> pd.Series:
    """Calculate rolling volatility of a given period."""
    return pd.Series(
        data=price_series.close.rolling(window=rolling_period).std()
        * sqrt(rolling_period),
        name=f"Volatility_{rolling_period}",
    ).fillna(0)
