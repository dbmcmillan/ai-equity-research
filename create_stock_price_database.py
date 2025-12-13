import pandas as pd
import yfinance as yf
import sqlite3
from datetime import datetime
import os

# --- Configuration ---
tickers = ["CROX", "DECK", "BIRK", "LULU", "ONON", "NKE", "UAA", 
           "RTX", "GD", "LMT", "NOC", "BA", "LHX", 
           "NVDA", "AMD", "INTC", "SPY", "AAPL", "MSFT", "GOOGL", "AMZN", "BA", "GD", "NET", "RHI", "MAN", "KFY", "KFRC"]

DATABASE_FILE = 'stock_prices.db'
TABLE_NAME = 'daily_prices'


def update_daily_prices(db_path, tickers):
    """
    Updates the daily_prices table with incremental updates for existing tickers
    and full history for newly added tickers.
    """
    print("Loading existing DB...")
    conn = sqlite3.connect(db_path)
    
    # Ensure the table exists with primary key
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        Date TEXT,
        Ticker TEXT,
        Close REAL,
        High REAL,
        Low REAL,
        Open REAL,
        Volume REAL,
        PRIMARY KEY (Date, Ticker)
    )
    """)
    conn.commit()

    # Load existing data
    existing_df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    print(f"Loaded {len(existing_df):,} existing rows.")
    #For each ticker, determine the last date we have data for
    final_dfs = []
    for ticker in tickers:
        print(f"\nProcessing ticker: {ticker}")
        ticker_existing = existing_df[existing_df['Ticker'] == ticker]
        if not ticker_existing.empty:
            last_date_str = ticker_existing['Date'].max()
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
            start_date = last_date + pd.Timedelta(days=1)
            print(f"Last date in DB for {ticker}: {last_date_str}. Fetching data from {start_date.date()} onwards.")
        else:
            start_date = None
            print(f"No existing data for {ticker}. Fetching full history.")

        # Fetch data using yfinance
        stock = yf.Ticker(ticker)
        if start_date:
            hist = stock.history(start=start_date.strftime("%Y-%m-%d"))
        else:
            hist = stock.history(period="max")

        if hist.empty:
            print(f"No new data fetched for {ticker}.")
            continue

        hist.reset_index(inplace=True)
        hist['Date'] = pd.to_datetime(hist['Date'], errors='coerce').dt.strftime("%Y-%m-%d")
        hist['Ticker'] = ticker
        hist = hist[['Date', 'Ticker', 'Close', 'High', 'Low', 'Open', 'Volume']]
        final_dfs.append(hist)
        print(f"Fetched {len(hist):,} new rows for {ticker}.")
    #Concatenate all new data
    if final_dfs:
        final_df = pd.concat([existing_df] + final_dfs, ignore_index=True)
        final_df.drop_duplicates(subset=['Date', 'Ticker'], keep='last', inplace=True)
    else:
        final_df = pd.DataFrame(columns=['Date', 'Ticker', 'Close', 'High', 'Low', 'Open', 'Volume'])
        print("No new data fetched for any ticker.")
    return final_df

def setup_initial_db(df: pd.DataFrame, database_file: str, table_name: str):
    """
    Creates the table from scratch and a UNIQUE index for deduplication.
    Only used on first ever run.
    """
    print(f"Setting up initial database table '{table_name}'...")
    conn = sqlite3.connect(database_file)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE UNIQUE INDEX IF NOT EXISTS idx_date_ticker
        ON {table_name} (Date, Ticker);
    ''')
    conn.commit()
    conn.close()
    print("Initial data save complete. UNIQUE index created on (Date, Ticker).")


# --- Execution Flow ---
final_df = update_daily_prices(DATABASE_FILE, tickers)

print("\n--- Checking for Duplicates in Returned Data (Date, Ticker) ---")
duplicates_mask = final_df.duplicated(subset=["Date", "Ticker"], keep=False)
if duplicates_mask.any():
    print("❌ FOUND DUPLICATES:")
    print(final_df[duplicates_mask])
else:
    print("✅ No duplicates inside returned data.")
print("------------------------------------------")

# On first run only
print(f"\nAbout to save final_df with {len(final_df):,} total rows")
print(f"AAPL rows in final_df: {len(final_df[final_df['Ticker']=='AAPL']):,}")

setup_initial_db(final_df, DATABASE_FILE, TABLE_NAME)

# Then immediately after, verify what got saved:
conn = sqlite3.connect(DATABASE_FILE)
check = pd.read_sql_query("SELECT Ticker, COUNT(*) as count FROM daily_prices GROUP BY Ticker", conn)
conn.close()
print("\nRows per ticker in DB after save:")
print(check)

setup_initial_db(final_df, DATABASE_FILE, TABLE_NAME)

print(f"\nFinal DataFrame shape: {final_df.shape}")
print(final_df[final_df['Ticker']=='AAPL'].head())
