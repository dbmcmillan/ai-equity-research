# Load projections table from file
import json
from venv import create
import pandas as pd
import numpy as np

from download_financials import download_financials_db
from forecast_from_projections import create_forecast_table
from project_cash_flow import calculate_valuation_metrics

ticker = "RHI"
projections_df = pd.read_csv(f'reports/Projections/RHI_Projections_Table.csv')
# Import all_financials from db
all_financials = download_financials_db(ticker)
print(all_financials['Free Cash Flow'])
forecast_table = create_forecast_table(projections_df, all_financials)

#Save forecast table to file
forecast_table.to_csv(f'reports/Forecast_Tables/RHI_Forecast_Table.csv', index=False)

#Create valuation metrics json file:
valuation_metrics = calculate_valuation_metrics(projections_df, 0.091, ticker, 102000000)
output_valuation_path = f"reports/Valuation_Metrics/{ticker}_Valuation_Metrics.json"
with open(output_valuation_path, "w", encoding="utf-8") as f:
    json.dump(valuation_metrics, f, indent=4)