"""Scaling functions."""
from pandas import DataFrame

EXCLUDE_COLS = ["ts", "dt", "flag", "label", "sin", "cos"]


def normalizer(df: DataFrame, min_max=(0, 1)) -> DataFrame:
    r"""
    Normalize data_frame to a range of [a, b].

    Equation:

    .. math::
        (b - a) * \frac{x - min(x)}{max(x) - min(x)}  + a

    Parameters
    ----------
    df : DataFrame
        DataFrame to normalize.
    min_max: tuple
        Tuple of the new (min, max) values.

    Returns
    -------
    result_df: DataFrame
        Normalized DataFrame.
    """
    result_df = df.copy()
    cols = [
        col for col in df.columns if not any(e_col in col for e_col in EXCLUDE_COLS)
    ]
    min_val, max_val = min_max
    result_df[cols] = (max_val - min_val) * (
        result_df[cols] - result_df[cols].min()
    ) / (result_df[cols].max() - result_df[cols].min()) + min_val
    return result_df.fillna(0)


def standardizer(df: DataFrame) -> DataFrame:
    r"""
    Standardize data_frame so that the mean of observed values is 0 and the standard deviation is 1.

    Equation:

    .. math::
        \frac{x - mean(x)}{std(x)}

    Parameters
    ----------
    df: DataFrame
        DataFrame to standardize.

    Returns
    -------
    result_df: DataFrame
        Standardized DataFrame.
    """
    result_df = df.copy()
    cols = [
        col for col in df.columns if not any(e_col in col for e_col in EXCLUDE_COLS)
    ]
    result_df[cols] = (result_df[cols] - result_df[cols].mean()) / result_df[cols].std()
    return result_df.fillna(0)
