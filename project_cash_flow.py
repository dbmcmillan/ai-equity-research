# Take the agent's projection table, turn it into a DataFrame, and calculate valuation metrics based on the projections.
import pandas as pd
from download_financials import download_financials_db as download_financials

def parse_projections_table(projections_table):
    """
    Parse the markdown projections table into a pandas DataFrame.
    """
    from io import StringIO
    df = pd.read_csv(StringIO(projections_table), skipinitialspace=True)
    return df

def calculate_valuation_metrics(projections_df, wacc, ticker, outstanding_shares):
    """
    Calculate valuation metrics based on the projections DataFrame.
    Assumes projections_df has columns: Year, Case, Revenue Growth (%), EBIT Growth (%), Net Income Growth (%), Free Cash Flow Growth (%)
    """
    all_financials = download_financials(ticker)
    total_debt = all_financials['Total Debt'].iloc[-1]
    cash = all_financials['Cash And Cash Equivalents'].iloc[-1]
    net_debt = total_debt - cash

    valuation_metrics = {}
    for case in ['Bear', 'Base', 'Bull']:
        case_df = projections_df[projections_df['Case'] == case]

        # Exclude TV from FCF projection
        forecast_df = case_df[case_df['Year'] != 'TV']

        # Calculate projected Free Cash Flows
        fcf_growth_rates = forecast_df['Free Cash Flow Growth (%)'] / 100
        fcf_values = all_financials['Free Cash Flow'].iloc[-1:].values.tolist()  # Start with the latest FCF
        for growth in fcf_growth_rates:
            fcf_values.append(fcf_values[-1] * (1 + growth))
        fcf_values = fcf_values[1:]  # Remove the initial base value

        # Calculate Terminal Value using Gordon Growth Model
        tg = projections_df.loc[
            (projections_df['Case'] == case) & (projections_df['Year'] == 'TV'),
            'Free Cash Flow Growth (%)'
        ].iloc[0] / 100

        terminal_value = fcf_values[-1] * (1 + tg) / (wacc - tg)

        # Discount FCFs and Terminal Value to Present Value
        discount_factors = [(1 + wacc) ** year for year in range(1, len(fcf_values) + 1)]  # end-of-year cash flows
        pv_fcf = sum(fcf / df for fcf, df in zip(fcf_values, discount_factors))
        pv_terminal_value = terminal_value / discount_factors[-1]


        # Enterprise Value
        total_valuation = pv_fcf + pv_terminal_value

        # Equity Value and Fair Stock Price
        equity_value = total_valuation - net_debt
        fair_stock_price = equity_value / outstanding_shares

        # Store results in dictionary
        valuation_metrics[case] = {
            "Enterprise Value": total_valuation,
            "Equity Value": equity_value,
            "Fair Stock Price": fair_stock_price
        }

    return valuation_metrics
