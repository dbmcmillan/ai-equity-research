import pandas as pd
import requests
import os
import yfinance as yf
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")  # Set your API key in environment variables

#Fetch Stock Data from stock_prices.db rather than through API calls. Only 5 years of data is needed.
def fetch_stock_data_db(ticker, db_path="stock_prices.db"):
    """
    Fetch historical daily stock prices from local SQLite database.
    Returns a DataFrame with Open, High, Low, Close, Volume.
    """
    import sqlite3
    conn = sqlite3.connect(db_path)
    query = f"""
    SELECT Date, Open, Close, Volume
    FROM daily_prices
    WHERE Ticker = '{ticker}' AND Date >= date('now', '-5 years')
    ORDER BY Date ASC
    """
    df = pd.read_sql_query(query, conn, parse_dates=['Date'], index_col='Date')
    df = df.astype(float)
    conn.close()
    return df