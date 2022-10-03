""" Micro-Macro Label
"""
from typing import Union

import numpy as np
import pandas as pd

from tykee.data.models.history_data import HistoryData
from tykee.market.models.period import Period


def micro_macro_label(
    micro_data: HistoryData,
    macro_period: Union[str, Period],
    threshold_percentile: float = 0.95,
) -> pd.Series:
    """Micro-Macro Label

    Creates label column for original - micro_data DataFrame.

    Strategy
    ---------
    1.Find the largest macro period movements by threshold_percentile.

    2.Map the movements to micro period DataFrame.

    3.Shift labels by 2 for early entry.

    Parameters
    ----------
    micro_data: HistoryData
        HistoryData to be labeled.
    macro_period: str, Period
        Macro period which will be analyzed to obtain labels.
    threshold_percentile: float
        Percentile of the largest movements to be labeled.

    Returns
    -------
    labels: pd.Series
        Labels for the original/micro DataFrame.
    """
    macro_data = HistoryData(
        micro_data.symbol, macro_period, micro_data.start_dt, micro_data.end_dt
    )

    macro_df = macro_data.data_frame
    micro_df = micro_data.data_frame

    macro_df["close_open"] = (macro_df.close - macro_df.open).abs()
    start_ts_list = macro_df.loc[
        macro_df.close_open >= macro_df.close_open.quantile(threshold_percentile),
        "start_ts_utc",
    ].tolist()
    micro_df["macro_label"] = np.where(micro_df.start_ts_utc.isin(start_ts_list), 1, 0)

    return pd.Series(micro_df.macro_label.shift(-2), name="label")
