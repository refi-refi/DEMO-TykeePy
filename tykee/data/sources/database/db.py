from datetime import datetime
from typing import Union

import pandas as pd
from sqlalchemy import create_engine

from tykee.config import DB_URL
from tykee.data.utils.common import standardize_datetime
from tykee.data.sources.database.queries import SYMBOL_HISTORY
from tykee.logging import logger
from tykee.market import Period, Symbol


class Database:
    """
    Wrapper class for database connection and operations,
    using sqlalchemy and pandas.

    Parameters
    ----------
    db_url: str
        Database URL, e.g. "postgresql://user:password@localhost:5432/mydatabase"

    Methods
    -------
    insert_dataframe(df, table_name, schema)
        Inserts a pandas dataframe into a table in a schema.

    insert_query(query)
        Executes a query.

    get_query(query)
        Returns a pandas dataframe from a query.

    close()
        Closes the connection.
    """

    def __init__(self, db_url=DB_URL):
        """
        Initializes the database connection.

        Parameters
        ----------
        db_url: str
            Database URL, e.g. "postgresql://user:password@localhost:5432/mydatabase"
        """
        self.engine = create_engine(db_url)
        self.conn = self.engine.connect()

    def get_symbol_history(
        self,
        symbol: Union[str, Symbol],
        period: Union[str, Period],
        date_from: Union[str, datetime],
        date_to: Union[str, datetime],
        int_type: bool = False,
    ):
        """
        Returns historical data for a symbol.

        Parameters
        ----------
        symbol: Symbol
            Symbol to get data for.
        period: Period
            Period to get data for.
        date_from: str or datetime
            Date from which to get data.
        date_to: str or datetime
            Date to which to get data.
        int_type: bool
            Whether to return the history data as an integer or a float.
        Returns
        -------
        historical_data: pandas.DataFrame
            Dataframe with symbol's historical prices.
        """
        symbol = symbol if isinstance(symbol, Symbol) else Symbol.from_str(symbol)
        period = period if isinstance(period, Period) else Period.from_str(period)
        date_from = int(standardize_datetime(date_from).timestamp())
        date_to = int(standardize_datetime(date_to).timestamp())
        logger.debug(f"Getting {symbol} {period} history from {date_from} to {date_to}")

        history_df = self.get_query(SYMBOL_HISTORY(symbol, period, date_from, date_to))
        if not int_type:
            history_df.insert(
                0, "start_dt", pd.to_datetime(history_df["start_ts_utc"], unit="s")
            )
            history_df.insert(
                1, "end_dt", pd.to_datetime(history_df["end_ts_utc"], unit="s")
            )
            for col in ("open", "high", "low", "close"):
                history_df[col] /= pow(10, symbol.digits)

        return history_df

    def insert_dataframe(self, dataframe: pd.DataFrame, table_name: str, schema: str):
        """
        Inserts a pandas dataframe into a table in a schema.
        Parameters
        ----------
        dataframe: pandas.DataFrame
            Dataframe to insert.
        table_name: str
            Name of the table to insert into.
        schema: str
            Name of the schema to insert into.

        Raises
        ------
        ValueError when duplicate data is found.
        """
        logger.info(f"""Inserting {len(dataframe)} rows into {schema}.{table_name}""")
        return dataframe.to_sql(
            table_name,
            self.conn,
            if_exists="append",
            index=False,
            schema=schema,
        )

    def insert_query(self, query):
        """
        Executes a query.

        Parameters
        ----------
        query: str
            Query to execute.
        """
        self.engine.execute(query)

    def get_query(self, query):
        """
        Returns a pandas dataframe from a query.

        Parameters
        ----------
        query: str
            Query to execute.

        Returns
        -------
        historical_data: pandas.DataFrame
            Dataframe with data from Database.
        """
        return pd.read_sql(query, self.conn)

    def close(self):
        """
        Closes the connection.
        """
        self.conn.close()
        self.engine.dispose()
