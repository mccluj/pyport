import pandas as pd
import pyodbc
from typing import Optional


def get_sql_server_connection(
    server: str, database: str, username: str, password: str, driver: str = "ODBC Driver 17 for SQL Server"
) -> pyodbc.Connection:
    """
    Establishes and returns a SQL Server connection using pyodbc.
    """
    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password}"
    )
    return pyodbc.connect(conn_str)


def get_third_friday_atm_options_df(conn: pyodbc.Connection) -> pd.DataFrame:
    """
    Executes SQL query to get ATM or nearest OTM call options expiring
    on the next third Friday after each current third Friday.
    """
    sql_query = """
    WITH ThirdFridays AS (
        SELECT DISTINCT TradeDate
        FROM SecurityPrices
        WHERE 
            DAY(TradeDate) BETWEEN 15 AND 21
            AND DATEPART(WEEKDAY, TradeDate) = 6 -- Friday
    ),
    ThirdFridaysWithNext AS (
        SELECT 
            TF.TradeDate AS CurrentDate,
            MIN(TF2.TradeDate) AS NextThirdFriday
        FROM ThirdFridays TF
        JOIN ThirdFridays TF2 ON TF2.TradeDate > TF.TradeDate
        GROUP BY TF.TradeDate
    ),
    ATMOptions AS (
        SELECT 
            tf.CurrentDate,
            tf.NextThirdFriday,
            sp.SecurityID,
            sp.ClosePrice,
            op.StrikePrice,
            op.OptionPrice,
            op.ExpirationDate
        FROM ThirdFridaysWithNext tf
        JOIN SecurityPrices sp
            ON sp.TradeDate = tf.CurrentDate
        JOIN OptionPrices op
            ON op.TradeDate = tf.CurrentDate
            AND op.ExpirationDate = tf.NextThirdFriday
            AND op.SecurityID = sp.SecurityID
            AND op.OptionType = 'C'
        WHERE op.StrikePrice >= sp.ClosePrice
    )
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY CurrentDate ORDER BY StrikePrice ASC) AS rn
        FROM ATMOptions
    ) ranked
    WHERE rn = 1
    ORDER BY CurrentDate;
    """
    return pd.read_sql(sql_query, conn)


def main():
    # 🔧 Update with your own credentials
    server = "your_server"
    database = "your_database"
    username = "your_username"
    password = "your_password"

    try:
        # Connect and run
        conn = get_sql_server_connection(server, database, username, password)
        df = get_third_friday_atm_options_df(conn)
        conn.close()

        # Output result
        print(df.head())

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
