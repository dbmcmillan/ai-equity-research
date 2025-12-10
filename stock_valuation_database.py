#Use yahoofinance to download financial statement data and create a database in sqlite
import pandas as pd
import yfinance as yf
import sqlite3
db_name = "stock_valuation.db"
ticker_list = ["CROX", "DECK", "BIRK", "SKX", "LULU", "ONON", "NKE", "UAA", "RTX", "GD", "LMT", "NOC", "BA", "LHX", "NVDA", "AMD", "INTC", "AMZN", "MSFT", "SPY"]
def create_stock_valuation_database(ticker_list, db_name="stock_valuation.db"):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create a table for stock valuation data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_valuation (
            ticker TEXT PRIMARY KEY,
            market_cap REAL,
            trailing_pe_ratio REAL,
            forward_pe_ratio REAL,
            pb_ratio REAL,
            dividend_yield REAL,
            roe REAL,
            debt_to_equity REAL
        )
    ''')

    for ticker in ticker_list:
        stock = yf.Ticker(ticker)
        info = stock.info

        market_cap = info.get('marketCap', None)
        trailing_pe = info.get('trailingPE', None)
        forward_pe = info.get('forwardPE', None)

        pb_ratio = info.get('priceToBook', None)
        dividend_yield = info.get('dividendYield', None)
        roe = info.get('returnOnEquity', None)
        debt_to_equity = info.get('debtToEquity', None)

        # Insert or replace the stock valuation data into the database
        cursor.execute('''
            INSERT OR REPLACE INTO stock_valuation (ticker, market_cap, trailing_pe_ratio, forward_pe_ratio, pb_ratio, dividend_yield, roe, debt_to_equity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ticker, market_cap, trailing_pe, forward_pe, pb_ratio, dividend_yield, roe, debt_to_equity))

    # Commit changes and close the connection
    conn.commit()
    conn.close()