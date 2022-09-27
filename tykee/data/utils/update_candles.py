import asyncio
from datetime import datetime
from typing import Union

import requests
from dateutil.relativedelta import relativedelta

from tykee.data import Database, MetaTrader
from tykee.data.database.queries import LAST_CANDLE_BY_SYMBOL
from tykee.logging import logger
from tykee.market.models.symbol import Symbol

DEFAULT_UPDATE_FROM = datetime(2012, 1, 1)


def main(
    update_from: Union[int, str, datetime] = "last",
    update_to: Union[int, str, datetime] = "now",
):
    """
    Update candles table in the database with the latest candles from MetaTrader.

    Parameters
    ----------
    update_from: Union[int, str, datetime]
        Start date of the update. Either 'last' or datetime or int expected.
    update_to: Union[int, str, datetime]
        End date of the update. Either 'now' or datetime or int expected.

    Returns
    -------
    None
    """
    start = datetime.now()
    mt = MetaTrader()
    db = Database()

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(update_symbol_candles(mt, db, symbol, update_from, update_to))
        for symbol in get_symbols()
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    logger.info(f"DB candles updated in: {datetime.now() - start}")


async def update_symbol_candles(
    mt_conn: MetaTrader,
    db_conn: Database,
    symbol: Symbol,
    update_from: Union[int, datetime],
    update_to: Union[int, datetime],
):
    """
    Get candles from MetaTrader and insert candles in the database.

    Parameters
    ----------
    mt_conn: MetaTrader
        MetaTrader connection
    db_conn: Database
        Database connection
    symbol: Symbol
        Symbol to update
    update_from: Union[int, datetime]
        Start datetime or int(index) of the update
    update_to: Union[int, datetime]
        End datetime or int(index) of the update

    Returns
    -------
    None
    """
    update_from = parse_update_from(update_from, symbol, db_conn)
    update_to = parse_update_to(update_to)
    for batch in mt_conn.candle_generator(
        symbol.name, "M1", update_from, update_to, relativedelta(weeks=4), int_type=True
    ):
        await asyncio.sleep(0.01)
        batch["created_at"] = datetime.now()
        batch["updated_at"] = datetime.now()
        batch["symbol_id"] = symbol.index
        db_conn.insert_dataframe(batch, "candles", "rest-api")


def parse_update_from(
    update_from: Union[int, str, datetime], symbol: Symbol, db_conn: Database
) -> Union[int, datetime]:
    """
    Parse update_from parameter.

    Parameters
    ----------
    update_from: Union[int, str, datetime]
        Start of the update
    symbol: Symbol
        Symbol to update
    db_conn: Database
        Database connection

    Returns
    -------
    Union[int, datetime]
    """
    if isinstance(update_from, (int, datetime)):
        return update_from

    if isinstance(update_from, str) and update_from.lower() == "last":
        last_ts = db_conn.get_query(LAST_CANDLE_BY_SYMBOL(symbol))
        return (
            datetime.utcfromtimestamp(last_ts.squeeze())
            if not last_ts.empty
            else DEFAULT_UPDATE_FROM
        )

    raise ValueError(
        "Invalid update_from value. Either 'last' or datetime or int expected."
    )


def parse_update_to(update_to: Union[int, str, datetime]) -> Union[int, datetime]:
    """
    Parse update_to parameter.

    Parameters
    ----------
    update_to: Union[int, str, datetime]
        End of the update

    Returns
    -------
    Union[int, datetime]
    """
    if isinstance(update_to, (int, datetime)):
        return update_to

    if isinstance(update_to, str) and update_to.lower() == "now":
        return datetime.now()

    raise ValueError(
        "Invalid update_to value. Either 'now' or datetime or int expected."
    )


def get_symbols(rest_api_url: str = "http://localhost:8080/symbols"):
    """
    Get symbols from the rest-api.

    Parameters
    ----------
    rest_api_url: str
        Rest-api url

    Returns
    -------
    List[Symbol]
    """
    symbols = requests.get(rest_api_url, timeout=3).json()
    symbols = [Symbol.from_str(symbol.get("name")) for symbol in symbols]
    return symbols


if __name__ == "__main__":
    main(update_from="last", update_to="now")
