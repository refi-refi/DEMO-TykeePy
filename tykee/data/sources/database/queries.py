"""Placeholder script for queries"""
from tykee.market import Symbol, Period


def SYMBOL_HISTORY(
    symbol: Symbol, period: Period, date_from: int, date_to: int, schema: str = "rest"
) -> str:
    """Returns historical data_frame for a symbol"""
    return f"""
        SET TIME ZONE 'UTC';
        SELECT * FROM {schema}.change_period({symbol.index}, {period.index}, {date_from}, {date_to});
    """


def LAST_CANDLE_BY_SYMBOL(symbol: Symbol, schema: str = "rest") -> str:
    """Returns the last candles end_ts_utc for a given symbol"""
    return f"""
        SELECT end_ts_utc FROM {schema}.candles
        WHERE symbol_id = {symbol.index}
        ORDER BY end_ts_utc DESC 
        LIMIT 1
        """
