"""Placeholder for the feature engineering functions."""
from math import sqrt

import numpy as np
import pandas as pd

from tykee import TykeeError


def volatility(data_series: pd.Series, rolling_period: int = 14) -> pd.Series:
    """Calculate rolling volatility of a given period."""
    return pd.Series(
        data=data_series.rolling(window=rolling_period).std() * sqrt(rolling_period),
        name=f"Volatility_{rolling_period}",
    ).fillna(0)


def datetime_sin(data_series: pd.Series, period: str) -> pd.Series:
    """Calculate sine of the timestamp column in the given period.
    Attributes
    ----------
    data_series: 'pd.Series'
        Timestamp column.
    period: 'str'
        Period of the sine function.
    """
    periods = {
        "day": 24 * 60 * 60,
        "week": 7 * 24 * 60 * 60,
        "year": 365.25 * 24 * 60 * 60,
    }
    if period in periods:
        return pd.Series(
            data=np.sin(data_series * (2 * np.pi / periods[period])),
            name=f"sin_{period}",
        ).round(5)

    raise TykeeError.value_error(datetime_sin.__name__, period, list(periods.keys()))


def datetime_cos(data_series: pd.Series, period: str) -> pd.Series:
    """Calculate cosine of the timestamp column in the given period.
    Attributes
    ----------
    data_series: 'pd.Series'
        Timestamp column.
    period: 'str'
        Period of the cosine function.
    """
    periods = {
        "day": 24 * 60 * 60,
        "week": 7 * 24 * 60 * 60,
        "year": 365.25 * 24 * 60 * 60,
    }
    if period in periods:
        return pd.Series(
            data=np.cos(data_series * (2 * np.pi / periods[period])),
            name=f"cos_{period}",
        ).round(5)

    raise TykeeError.value_error(datetime_cos.__name__, period, list(periods.keys()))
