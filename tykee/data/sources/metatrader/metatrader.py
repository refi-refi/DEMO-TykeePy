from datetime import datetime
from time import sleep
from typing import Union, Callable

import MetaTrader5 as mt
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

from tykee import logger, TykeeError
from tykee.data.sources.metatrader.models import MTCandleBatch
from tykee.data.utils.common import standardize_datetime
from tykee.market import Period, Symbol

MAX_FETCH_TRIES = 5


class MetaTrader:
    """
    Wrapper class for MetaTrader5 functionality.
    """

    def __init__(
        self,
        server: str = None,
        login: int = None,
        password: str = None,
        exe_path: str = None,
    ):
        self._config = {
            "server": server,
            "login": login,
            "password": password,
            "path": exe_path,
        }

    def candle_generator(
        self,
        symbol: Union[str, Symbol],
        period: Union[str, Period],
        start: Union[int, str, datetime],
        end: Union[int, str, datetime],
        batch_size: Union[int, relativedelta],
        int_type: bool = False,
    ):
        """
        Generator for fetching candlestick data_frame from MetaTrader5 terminal.

        Parameters
        ----------
        symbol: 'str', 'Symbol'
            Financial instrument's name as string or Symbol object.
        period: 'str', 'Period'
            Period (timeframe) of candlesticks.
        start: 'int', 'datetime'
            Date or int(index) of the first bar.
        end: 'int', 'datetime'
            Date or int(index) of the last bar.
        int_type: bool
            Either the returned candlestick data_frame is cast to an int or left as a float.
        batch_size: int, relativedelta
            Batch size for fetching candlestick data_frame from MetaTrader5.

        Returns
        ------
        candle_df: pandas.DataFrame
            Generator for historical candlestick data_frame.
        """
        symbol = symbol if isinstance(symbol, Symbol) else Symbol.from_str(symbol)
        period = period if isinstance(period, Period) else Period.from_str(period)
        start = start if isinstance(start, int) else standardize_datetime(start)
        end = end if isinstance(start, int) else standardize_datetime(end)
        fetch_type = self.fetch_type(start, end)
        mt_batch = MTCandleBatch(start, end, batch_size)

        logger.info(
            f"Yielding {symbol} {period} candlesticks from {start} to {end}, "
            f"fetch type: {fetch_type.__name__}"
        )

        batch = 0
        for b_start, b_end in zip(mt_batch.batch_starts, mt_batch.batch_ends):
            candle_df = pd.DataFrame(
                self.__fetch_raw_candles(symbol, period, b_start, b_end, fetch_type)
            )

            candle_df.drop_duplicates(keep="last", inplace=True)
            candle_df.drop(columns=["real_volume"], inplace=True)
            candle_df.rename(
                columns=dict(time="start_ts_utc", tick_volume="volume"), inplace=True
            )
            candle_df.insert(1, "end_ts_utc", candle_df.start_ts_utc + period.seconds)

            if int_type:
                for col in ("open", "high", "low", "close"):
                    candle_df[col] = candle_df[col] * pow(10, symbol.digits)
                candle_df = candle_df.astype(int)
            else:
                candle_df.insert(
                    0, "start_dt", pd.to_datetime(candle_df.start_ts, unit="s")
                )
                candle_df.insert(
                    1, "end_dt", pd.to_datetime(candle_df.end_ts, unit="s")
                )
            candle_df = candle_df.sort_values(by="start_ts_utc")
            batch += 1
            logger.info(
                f"{symbol} {period} {b_start} - {b_end}: Batch {batch} of {mt_batch.batch_count}"
            )
            yield candle_df

    def __fetch_raw_candles(
        self,
        symbol: Symbol,
        period: Period,
        start: Union[int, datetime],
        end: Union[int, datetime],
        mt_function: Callable,
    ) -> np.array:
        """

        Parameters
        ----------
        symbol
        period
        start
        end
        mt_function

        Returns
        -------
        candle_df: pd.DataFrame
            Historical candlestick data_frame.
        """
        candles = np.array([])
        if self.initialize() and self.symbol_in_market_watch(symbol):
            for _ in range(MAX_FETCH_TRIES):
                candles = mt_function(symbol.name, period.metatrader, start, end)
                logger.debug(
                    f"{symbol} candles {start} - {end} fetched: {len(candles)}"
                )
                if candles.size == 0:
                    logger.warning(
                        f"No candlesticks found for {symbol} {period} "
                        f"from {start} to {end}. Retrying..."
                    )
                    sleep(1)
                else:
                    break

        return candles

    def initialize(self) -> bool:
        """
        Creates connection to MetaTrader5.

        Returns
        -------
        bool
            True if connection is established, else raises TykeeError.
        """
        config_values = list(self._config.values())
        if all(config_values):
            if not mt.initialize(**self._config):
                raise TykeeError.mt_init_error(
                    "Invalid all input init", mt.last_error()
                )
        elif (
            self._config["path"]
            and any(config_values[:-1])
            and not all(config_values[:-1])
        ):
            raise TykeeError.mt_init_error(
                "Invalid all input init, missing info", mt.last_error()
            )
        elif self._config["path"]:
            if not mt.initialize(self._config["path"]):
                raise TykeeError.mt_init_error(
                    "Invalid terminal path init", mt.last_error()
                )
        else:
            if not mt.initialize():
                raise TykeeError.mt_init_error("Invalid no input init", mt.last_error())

        return True

    @staticmethod
    def symbol_in_market_watch(symbol: Symbol) -> bool:
        """
        Static method that checks if provided Symbol is in MetaTraders Market Watch,
        and adds it if it's possible.

        Notes
        -----
        Before using this method connection to MetaTrader must be established.
        either with mt.initialize() or self.initialize().

        Parameters
        ----------
        symbol: Symbol
            Symbol object which will be checked.

        Returns
        -------
        bool - True if symbol is in Market Watch,
        False if symbol is not in Market Watch and cannot be added.
        """
        if mt.symbol_select(symbol.name, True):
            logger.debug(f"Symbol {symbol} found in Market Watch")
            return True

        raise TykeeError(
            f"Symbol {symbol} not found in Market Watch and cannot be added."
        )

    @staticmethod
    def fetch_type(start: Union[int, datetime], end: Union[int, datetime]) -> Callable:
        """
        Static method that returns MetaTrader mt5.copy_rates_* function
        which will be used for fetching candlestick data_frame.

        Parameters
        ----------
        start: 'int', 'datetime'
            Date or index of the first bar.
        end: 'int', 'datetime'
            Date or index of the last bar.
        Returns
        -------
        Callable - MetaTrader5 function to copy candlestick data_frame from terminal.
        """
        if isinstance(start, int) and isinstance(end, int):
            fetch_function = mt.copy_rates_from_pos

        elif isinstance(start, datetime) and isinstance(end, int):
            fetch_function = mt.copy_rates_from

        elif isinstance(start, datetime) and isinstance(end, datetime):
            fetch_function = mt.copy_rates_range

        else:
            raise TykeeError(f"Invalid start and end types: {type(start)}, {type(end)}")

        return fetch_function
