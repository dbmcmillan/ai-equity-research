# Use the created projections table and most recent values of Revenue, EBIT, Net Income, and Free Cash Flow to create a forecast table. Projections table has columns with projected annual growth rates for each of these metrics.
import pandas as pd
from download_financials import download_financials_db
ticker = "CROX"
def create_forecast_table(projections_table, all_financials):
    revenue = all_financials['Total Revenue'].iloc[-1]
    ebit = all_financials['EBIT'].iloc[-1]
    net_income = all_financials['Net Income'].iloc[-1]
    free_cash_flow = all_financials['Free Cash Flow'].iloc[-1]
    forecast_years = projections_table.index.tolist()
    forecast_data = {
        'Total Revenue': [],
        'EBIT': [],
        'Net Income': [],
        'Free Cash Flow': []
    }
    for year in forecast_years:
        revenue_growth = projections_table.loc[year, 'Revenue Growth (%)']/100
        ebit_growth = projections_table.loc[year, 'EBIT Growth (%)']/100
        net_income_growth = projections_table.loc[year, 'Net Income Growth (%)']/100
        fcf_growth = projections_table.loc[year, 'Free Cash Flow Growth (%)']/100
        revenue *= (1 + revenue_growth)
        ebit *= (1 + ebit_growth)
        net_income *= (1 + net_income_growth)
        free_cash_flow *= (1 + fcf_growth)
        forecast_data['Total Revenue'].append(revenue)
        forecast_data['EBIT'].append(ebit)
        forecast_data['Net Income'].append(net_income)
        forecast_data['Free Cash Flow'].append(free_cash_flow)
    forecast_table = pd.DataFrame(forecast_data, index=forecast_years)
    return forecast_table

# Test the function
#Load projections table from csv file
projections_table = pd.read_csv(f"reports/{ticker}_Projections_Table.csv", index_col=0)
# Only keep rows where "Case" column is "Base"
projections_table = projections_table[projections_table['Case'] == 'Base']
projections_table = projections_table.drop(columns=['Case'])
projections_table = projections_table[projections_table.index != 'TV']

#Load all financials 
all_financials = download_financials_db(ticker)
print(projections_table)
forecast_table = create_forecast_table(projections_table, all_financials)
print(forecast_table)
#Save forecast table to CSV for verification
forecast_table.to_csv(f"reports/{ticker}_Forecast_Table.csv")
print(f"Forecast table exported to: reports/{ticker}_Forecast_Table.csv")