#Calculate P/E, P/S, P/B, EV/EBITDA multiples for competitor companies and return as a DataFrame
from turtle import down
import pandas as pd
from stock_history import fetch_stock_data_db
from download_financials import download_outstanding_shares
import sqlite3

def create_multiples_df(ticker, competitor_tickers):
    # Import latest prices from stock_prices.db
    stock_df = fetch_stock_data_db(ticker)
    prices = stock_df['Close'].iloc[-1]
    outstanding_shares_stock = download_outstanding_shares(ticker)
    prices = [{
        'Ticker': ticker,
        'Price': prices,
        'Outstanding Shares': outstanding_shares_stock
    }]
    for comp_ticker in competitor_tickers:
        competitors_df = fetch_stock_data_db(comp_ticker)
        latest_close_price_competitors = competitors_df['Close'].iloc[-1]
        outstanding_shares = download_outstanding_shares(comp_ticker)
        # Placeholder values for financial metrics; replace with actual data retrieval logic

        prices.append({
            'Ticker': comp_ticker,
            'Price': latest_close_price_competitors,
            'Outstanding Shares': outstanding_shares
        })
    prices = pd.DataFrame(prices)
    # Import financial metrics from reports/financial_database.csv
    financials_df = pd.read_csv(f"reports\\financials_database.csv", parse_dates=['Date'])
    # Filter financials_df to only include relevant tickers
    financials_df = financials_df[financials_df['Ticker'].isin([ticker] + competitor_tickers)]
    financials_df = financials_df[['Date', 'Ticker', 'Net Income', 'Total Revenue', 'Total Assets', 'Stockholders Equity', 'Total Debt', "Operating Cash Flow"]]
   
    #Make sure date/index column is formatted correctly
    financials_df['Date'] = pd.to_datetime(financials_df['Date'])
    #Set Date as index
    financials_df.set_index('Date', inplace=True)
     # Limit financials_df to only the most recent row for each ticker
    financials_df = financials_df.sort_values('Date').groupby('Ticker').tail(1)
    # Merge price and financials data
    multiples_df = pd.merge(prices, financials_df, on='Ticker')
    # Calculate multiples
    multiples_df['P/E'] = multiples_df['Price'] / (multiples_df['Net Income'] / multiples_df['Outstanding Shares'])
    multiples_df['P/S'] = multiples_df['Price'] / (multiples_df['Total Revenue'] / multiples_df['Outstanding Shares'])
    multiples_df['P/B'] = multiples_df['Price'] / (multiples_df['Stockholders Equity'] / multiples_df['Outstanding Shares'])
    multiples_df['EV/CFO'] = (multiples_df['Price']*multiples_df['Outstanding Shares'] + multiples_df['Total Debt'])/ multiples_df['Operating Cash Flow']
    multiples_df = multiples_df[['Ticker', 'P/E', 'P/S', 'P/B', 'EV/CFO']].transpose()
    return multiples_df
