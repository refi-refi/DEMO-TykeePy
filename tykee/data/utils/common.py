"""Placeholder for different data related transformations"""
from datetime import datetime
from typing import Union

import pytz
from dateutil import parser


def standardize_datetime(date_time: Union[str, datetime]) -> datetime:
    """
    Static method to standardize str or datetime inputs
    to datetime.datetime object with UTC timezone.

    Parameters
    ----------
    date_time: str, datetime
        String or datetime object which will be standardized.

    Returns
    -------
    dt: datetime
        Datetime with UTC timezone.
    """
    date_time = date_time if isinstance(date_time, datetime) else parser.parse(date_time)
    return date_time if date_time.tzinfo == pytz.UTC else pytz.utc.localize(date_time)
