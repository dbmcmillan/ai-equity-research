# Use the created projections table and most recent values of Revenue, EBIT, Net Income, and Free Cash Flow to create a forecast table. Projections table has columns with projected annual growth rates for each of these metrics.
import pandas as pd
from download_financials import download_financials_db
ticker = "CROX"
def create_forecast_table(projections_table, all_financials):
    projections_table = projections_table[projections_table["Case"]=="Base"]
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
