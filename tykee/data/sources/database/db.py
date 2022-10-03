from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine

from tykee.config import DB_URL
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
        symbol: Symbol,
        period: Period,
        date_from: datetime,
        date_to: datetime,
    ):
        """
        Returns historical data_frame for a symbol.

        Parameters
        ----------
        symbol: Symbol
            Symbol to get data_frame for.
        period: Period
            Period to get data_frame for.
        date_from: datetime
            Date from which to get data_frame.
        date_to: datetime
            Date to which to get data_frame.
        Returns
        -------
        historical_data: pandas.DataFrame
            Dataframe with symbol's historical prices.
        """
        ts_from = int(date_from.timestamp())
        ts_to = int(date_to.timestamp())
        logger.debug(
            f"Getting {symbol} ({symbol.index}) {period} ({period.index}) "
            f"history from {date_from} ({ts_from}) to {date_to} ({ts_to})"
        )
        return self.get_query(SYMBOL_HISTORY(symbol, period, ts_from, ts_to))

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
        ValueError when duplicate data_frame is found.
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
            Dataframe with data_frame from Database.
        """
        return pd.read_sql(query, self.conn)

    def close(self):
        """
        Closes the connection.
        """
        self.conn.close()
        self.engine.dispose()
