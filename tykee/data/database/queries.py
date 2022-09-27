"""Placeholder script for queries"""
from tykee.market import Symbol


def LAST_CANDLE_BY_SYMBOL(symbol: Symbol, schema: str = "rest-api") -> str:
    """Returns the last candles end_ts_utc for a given symbol"""
    return f"""
        SELECT end_ts_utc FROM {schema}.candles
        WHERE symbol_id = {symbol.index}
        ORDER BY end_ts_utc DESC 
        LIMIT 1
        """
