""" History Data Model
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Union

import pandas as pd

from tykee.data import Database
from tykee.data.utils.common import standardize_datetime
from tykee.market import Symbol, Period


@dataclass(frozen=True)
class HistoryData:
    """HistoryData dataclass"""

    symbol: Union[str, Symbol]
    period: Union[str, Period]
    start_dt: Union[str, datetime]
    end_dt: Union[str, datetime]
    data_frame: pd.DataFrame = None

    def __post_init__(self):
        if isinstance(self.symbol, str):
            object.__setattr__(self, "symbol", Symbol.from_str(self.symbol))
        if isinstance(self.period, str):
            object.__setattr__(self, "period", Period.from_str(self.period))

        object.__setattr__(self, "start_dt", standardize_datetime(self.start_dt))
        object.__setattr__(self, "end_dt", standardize_datetime(self.end_dt))

        db = Database()
        data = db.get_symbol_history(
            self.symbol,
            self.period,
            self.start_dt,
            self.end_dt,
        )
        db.close()
        object.__setattr__(self, "data_frame", data)

    def add_datetime_cols(self):
        """Adds datetime columns"""
        self.data_frame.insert(
            loc=0,
            column="start_dt",
            value=pd.to_datetime(self.data_frame.start_ts_utc, unit="s").dt.tz_localize(
                "UTC"
            ),
        )
        self.data_frame.insert(
            loc=1,
            column="end_dt",
            value=pd.to_datetime(self.data_frame.end_ts_utc, unit="s").dt.tz_localize(
                "UTC"
            ),
        )

    def to_float_type(self):
        """Returns price data_frame as floats"""
        float_df = self.data_frame.copy()
        for col in ("open", "high", "low", "close"):
            float_df[col] /= pow(10, self.symbol.digits)
        return float_df
