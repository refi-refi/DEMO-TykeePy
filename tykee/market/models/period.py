from enum import Enum

import MetaTrader5 as MT5
from dateutil.relativedelta import relativedelta


class Period(Enum):
    """Enum for Periods."""

    M1 = (1, "1min", MT5.TIMEFRAME_M1, 60, 1, relativedelta(minutes=1))
    M5 = (2, "5min", MT5.TIMEFRAME_M5, 300, 5, relativedelta(minutes=5))
    M10 = (3, "10min", MT5.TIMEFRAME_M10, 600, 10, relativedelta(minutes=10))
    M15 = (4, "15min", MT5.TIMEFRAME_M15, 900, 15, relativedelta(minutes=15))
    M30 = (5, "30min", MT5.TIMEFRAME_M30, 1800, 30, relativedelta(minutes=30))
    H1 = (6, "1H", MT5.TIMEFRAME_H1, 3600, 60, relativedelta(hours=1))
    H4 = (7, "4H", MT5.TIMEFRAME_H4, 14400, 240, relativedelta(hours=4))
    DAY = (8, "1D", MT5.TIMEFRAME_D1, 86400, 1440, relativedelta(days=1))
    MONTH = (9, "1M", MT5.TIMEFRAME_MN1, 2592000, 43200, relativedelta(months=1))

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
    def index(self):
        """Return Period's index that matches Database index."""
        return self.value[0]

    @property
    def pandas(self):
        """Return pandas equivalent period string."""
        return self.value[1]

    @property
    def metatrader(self):
        """Return MetaTrader5 equivalent period enum."""
        return self.value[2]

    @property
    def seconds(self):
        """Return seconds equivalent period int."""
        return self.value[3]

    @property
    def minutes(self):
        """Return minutes equivalent period int."""
        return self.value[4]

    @property
    def relativedelta(self):
        """Return relativedelta equivalent period."""
        return self.value[5]
