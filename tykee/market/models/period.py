from datetime import timedelta
from enum import Enum

import MetaTrader5 as MT5


class Period(Enum):
    """Enum for Periods."""

    M1 = ("1min", MT5.TIMEFRAME_M1, 60, 1, timedelta(minutes=1))
    M5 = ("5min", MT5.TIMEFRAME_M5, 300, 5, timedelta(minutes=5))
    M10 = ("10min", MT5.TIMEFRAME_M10, 600, 10, timedelta(minutes=10))
    M15 = ("15min", MT5.TIMEFRAME_M15, 900, 15, timedelta(minutes=15))
    M30 = ("30min", MT5.TIMEFRAME_M30, 1800, 30, timedelta(minutes=30))
    H1 = ("1H", MT5.TIMEFRAME_H1, 3600, 60, timedelta(hours=1))
    H4 = ("4H", MT5.TIMEFRAME_H4, 14400, 240, timedelta(hours=4))
    DAY = ("1D", MT5.TIMEFRAME_D1, 86400, 1440, timedelta(days=1))
    WEEK = ("1W", MT5.TIMEFRAME_W1, 604800, 10080, timedelta(weeks=1))
    MONTH = ("1M", MT5.TIMEFRAME_MN1, 2592000, 43200, timedelta(weeks=4))

    def __str__(self):
        """Return string representation of Period."""
        return self.name

    @classmethod
    def from_str(cls, name):
        """Construct Period from string."""
        return cls[name]

    @classmethod
    def default_period(cls):
        """Return default period."""
        return cls.M1

    @property
    def pandas(self):
        """Return pandas equivalent period string."""
        return self.value[0]

    @property
    def metatrader(self):
        """Return MetaTrader5 equivalent period enum."""
        return self.value[1]

    @property
    def seconds(self):
        """Return seconds equivalent period int."""
        return self.value[2]

    @property
    def minutes(self):
        """Return minutes equivalent period int."""
        return self.value[3]

    @property
    def timedelta(self):
        """Return timedelta equivalent period."""
        return self.value[4]
