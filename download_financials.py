import pandas as pd
import numpy as np
import yfinance as yf

#Create a function to download financials from financials_database.db rather than through API calls
def download_financials_db(ticker, db_path="financials_database.db"):
    """
    Download financial statements from local SQLite database.
    Returns a DataFrame with financial statement data.
    """
    import sqlite3
    conn = sqlite3.connect(db_path)
    query = f"""
    SELECT *
    FROM financials
    WHERE Ticker = '{ticker}'
    ORDER BY Date ASC
    """
    df = pd.read_sql_query(query, conn, parse_dates=['Date'], index_col='Date')
    for col in df.columns:
        if col != 'Ticker':
            df[col] = pd.to_numeric(df[col], errors='coerce')
    conn.close()
    for col in df.columns:
        if col != 'Ticker':
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.sort_index(ascending=True)
    return df
def calculate_drivers(all_financials):
    """
    Calculate key financial ratios and drivers from combined financial statements.
    """
    drivers_df = pd.DataFrame(index=all_financials.index)
    
    # Growth metrics
    if 'Total Revenue' in all_financials.columns:
        drivers_df['Total Revenue YoY Growth'] = all_financials['Total Revenue'].pct_change()
    if 'EBIT' in all_financials.columns:
        drivers_df['EBIT YoY Growth'] = all_financials['EBIT'].pct_change()
    if 'Free Cash Flow' in all_financials.columns:
        drivers_df['Free Cash Flow YoY Growth'] = all_financials['Free Cash Flow'].pct_change()
            
    # Margins and leverage
    drivers_df['Net Debt'] = all_financials['Total Debt'] - all_financials['Cash And Cash Equivalents']
    drivers_df['EBIT Margin'] = all_financials['EBIT'] / all_financials['Total Revenue']
    drivers_df['Net Income Margin'] = all_financials['Net Income'] / all_financials['Total Revenue']
    drivers_df['FCF Margin'] = all_financials['Free Cash Flow'] / all_financials['Total Revenue']
    drivers_df['Capex as % of Revenue'] = all_financials['Capital Expenditure'] / all_financials['Total Revenue']
    drivers_df['Net Debt to EBIT'] = drivers_df['Net Debt'] / all_financials['EBIT'].replace(0, np.nan)
    if 'Interest Expense' in all_financials.columns and 'EBIT' in all_financials.columns:
        drivers_df['Interest Coverage Ratio'] = (
            all_financials['EBIT'] / all_financials['Interest Expense'].replace(0, np.nan)
        )
    else:
        drivers_df['Interest Coverage Ratio'] = np.nan
    drivers_df['Effective Tax Rate'] = all_financials['Tax Provision'] / all_financials['Pretax Income'].replace(0, np.nan)
    
    return drivers_df

def download_outstanding_shares(ticker):
    """
    Download the number of outstanding shares for a given ticker.
    """
    ticker_object = yf.Ticker(ticker)
    outstanding_shares = ticker_object.info['sharesOutstanding']
    return outstanding_shares

