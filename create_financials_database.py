# Start with simply downloading financial statement information for a few tickers using yfinance
import pandas as pd
import yfinance as yf
import sqlite3
db_name = "financials_database.db"
ticker_list = ["CROX", "DECK", "BIRK", "LULU", "ONON", "NKE", "UAA", 
           "RTX", "GD", "LMT", "NOC", "BA", "LHX", 
           "NVDA", "AMD", "INTC", "SPY", "AAPL", "MSFT", "GOOGL", "AMZN", "BA", "GD", "NET"]
def create_financials_dataframe(ticker_list):
    financials = pd.DataFrame()
    for ticker in ticker_list:
        stock = yf.Ticker(ticker)
        # Fetch financial statements
        income_stmt = stock.financials.transpose()
        balance_sheet = stock.balance_sheet.transpose()
        cash_flow = stock.cashflow.transpose()
        #Combine into a single DataFrame for simplicity
        financials_df = pd.concat([income_stmt, balance_sheet, cash_flow], axis=1)
        financials_df.reset_index(inplace=True)
        financials_df.rename(columns={'index': 'Date'}, inplace=True)
        financials_df['Ticker'] = ticker
        # Keep only certain columns for simplicity and financial analysis
        cols = ['Total Revenue', 'Cost Of Revenue', 'Selling General And Administrative', 'Operating Expense', 
            'EBIT', 'Interest Expense', 'Pretax Income', 'Tax Provision', 'Net Income', 'Diluted Average Shares', 
            'Depreciation And Amortization In Income Statement', 'Cash And Cash Equivalents', 'Accounts Receivable', 
            'Inventory', 'Accounts Payable', 'Working Capital', 'Net PPE', 'Gross PPE', 'Accumulated Depreciation', 
            'Stock Based Compensation', 'Total Debt', 'Long Term Debt', 'Current Debt', 'Operating Cash Flow', 
            'Capital Expenditure', 'Free Cash Flow', 'Change In Working Capital', 'Stockholders Equity', 
            'Invested Capital', 'Total Assets']
        existing_cols = [c for c in cols if c in financials_df.columns]
        financials_df = financials_df[['Date', 'Ticker'] + existing_cols]
        for col in existing_cols:
            financials_df[col] = pd.to_numeric(financials_df[col], errors='coerce')
        financials = pd.concat([financials, financials_df], ignore_index=True)
    return financials
def create_financials_database(financials, db_name="financials_database.db"):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create a table for financial statement data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS financials (
            Date TEXT,
            Ticker TEXT,
            Total_Revenue REAL,
            Cost_Of_Revenue REAL,
            Selling_General_And_Administrative REAL,
            Operating_Expense REAL,
            EBIT REAL,
            Interest_Expense REAL,
            Pretax_Income REAL,
            Tax_Provision REAL,
            Net_Income REAL,
            Diluted_Average_Shares REAL,
            Depreciation_And_Amortization_In_Income_Statement REAL,
            Cash_And_Cash_Equivalents REAL,
            Accounts_Receivable REAL,
            Inventory REAL,
            Accounts_Payable REAL,
            Working_Capital REAL,
            Net_PPE REAL,
            Gross_PPE REAL,
            Accumulated_Depreciation REAL,
            Stock_Based_Compensation REAL,
            Total_Debt REAL,
            Long_Term_Debt REAL,
            Current_Debt REAL,
            Operating_Cash_Flow REAL,
            Capital_Expenditure REAL,
            Free_Cash_Flow REAL,
            Change_In_Working_Capital REAL,
            Stockholders_Equity REAL,
            Invested_Capital REAL,
            Total_Assets REAL,
            PRIMARY KEY (Date, Ticker)
        )
    ''')

    # Insert financial statement data into the database
    financials.to_sql('financials', conn, if_exists='replace', index=False)

    # Commit changes and close the connection
    conn.commit()
    conn.close()


financials = create_financials_dataframe(ticker_list)
create_financials_database(financials, db_name)
# Print confirmation
print(f"Financials database created and populated in: {db_name}")

#Save to CSV for verification
financials.to_csv("reports/financials_database.csv", index=False)
print("Financials database exported to: reports/financials_database.csv")

def fetch_financials_for_ticker(ticker, db_name="financials_database.db"):
    conn = sqlite3.connect(db_name)
    query = f"SELECT * FROM financials WHERE Ticker = '{ticker}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df