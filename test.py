
import csv
from stock_history import fetch_stock_data_db
from download_financials import download_financials_db, calculate_drivers
from calculate_multiples import create_multiples_df
from sensitivity_table import create_sensitivity_table
import pandas as pd
ticker = "LULU"
projections_table = pd.read_csv(f"reports\\LULU_Projections_Table.csv")
all_financials = download_financials_db(ticker)
drivers_df = calculate_drivers(all_financials)
print(drivers_df.head(20))