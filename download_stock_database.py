#Download stock data from sqlite database
import pandas as pd
import sqlite3

DATABASE_FILE = "stock_prices.db"
TABLE_NAME = 'daily_prices'
OUTPUT_CSV_PATH = "reports/stock_price_database.csv"
conn = sqlite3.connect(DATABASE_FILE)
#Import stock price data from the last 5 years for all tickers
df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME} WHERE Date >= date('now', '-5 years')", conn)
conn.close()
df.to_csv(OUTPUT_CSV_PATH, index=False)
print(f"Stock price database exported to: {OUTPUT_CSV_PATH}")