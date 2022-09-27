from dataclasses import dataclass, field
from datetime import datetime
from typing import Union, List

from dateutil.relativedelta import relativedelta

from tykee import TykeeError


@dataclass
class MTCandleBatch:
    """Class for batching fetch start and end parameters"""

    start: Union[int, datetime]
    end: Union[int, datetime]
    batch_size: Union[int, relativedelta]
    batch_count: int = field(default_factory=int)
    batch_starts: List[Union[int, datetime]] = field(default_factory=list)
    batch_ends: List[Union[int, datetime]] = field(default_factory=list)

    def __post_init__(self):
        if all(isinstance(arg, int) for arg in (self.start, self.end)):
            self.int_int_batching()
        elif all(isinstance(arg, datetime) for arg in (self.start, self.end)):
            self.dt_dt_batching()

        elif isinstance(self.start, datetime) and isinstance(self.end, int):
            raise NotImplementedError(
                "MTCandlesBatches.__post_init__() datetime - int fetch_type"
            )
        else:
            raise TykeeError(
                f"Invalid MTCandlesBatches.__post_init__() args: "
                f"{self.start} ({type(self.start).__name__}), "
                f"{self.end} ({type(self.end).__name__})"
            )

    def int_int_batching(self):
        """Batching for int-int fetch_type"""
        assert_msg = (
            f"Must provide int 'batch_size' for int-int fetching,"
            f" type '{type(self.batch_size).__name__}' was passed"
        )
        assert isinstance(self.batch_size, int), assert_msg

        row_count = self.end - self.start
        leftover = row_count % self.batch_size

        self.batch_count = (
            int(row_count / self.batch_size)
            if leftover == 0
            else int(row_count / self.batch_size + 1)
        )

        self.batch_starts = []
        self.batch_ends = []
        for i in range(self.batch_count):
            self.batch_starts.append(i * self.batch_size)
            if i + 1 == self.batch_count and leftover > 0:
                self.batch_ends.append(self.end)
            else:
                self.batch_ends.append((i + 1) * self.batch_size)

    def dt_dt_batching(self):
        """Batching for dt-dt fetch_type"""
        assert_msg = (
            f"Must provide relativedelta 'batch_size' for datetime-datetime fetching,"
            f" type '{type(self.batch_size).__name__}' was passed"
        )
        assert isinstance(self.batch_size, relativedelta), assert_msg

        current_dt = self.start
        dates = [current_dt]
        while current_dt < self.end:
            current_dt += self.batch_size
            dates.append(current_dt)

        self.batch_starts = dates[:-1]
        self.batch_ends = dates[1:]
        if self.batch_ends[-1] != self.end:
            self.batch_ends[-1] = self.end
        self.batch_ends = [
            batch - relativedelta(minutes=1) for batch in self.batch_ends
        ]
        self.batch_count = len(self.batch_starts)
