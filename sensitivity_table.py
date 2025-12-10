# Function that creates a sensitivity table based on base case assumptions for WACC and Terminal Growth Rate. Terminal Growth rate is in the projections table and WACC is calculated as a standalone variable.
import numpy as np
import pandas as pd

def create_sensitivity_table(projections_table, all_financials, wacc, outstanding_shares):
    # Filter to Base Case and exclude TV row
    base_case = projections_table[
        (projections_table['Case'] == 'Base') & 
        (projections_table['Year'] != 'TV')
    ].copy()
    
    # Get TV row separately
    tv_row = projections_table[
        (projections_table['Case'] == 'Base') & 
        (projections_table['Year'] == 'TV')
    ]
    base_tg = tv_row['Free Cash Flow Growth (%)'].iloc[0] / 100  # 3.0% → 0.03
    
    # Project FCF for years 1-5
    initial_fcf = all_financials['Free Cash Flow'].iloc[-1]
    fcf_values = []
    current_fcf = initial_fcf
    
    for growth_rate in base_case['Free Cash Flow Growth (%)']:
        current_fcf = current_fcf * (1 + growth_rate / 100)  # 5.2% → 0.052
        fcf_values.append(current_fcf)
    
    # Now fcf_values has [FY26_FCF, FY27_FCF, FY28_FCF, FY29_FCF, FY30_FCF]
    
    # Create WACC and TG ranges
    wacc_values = np.arange(wacc - 0.02, wacc + 0.025, 0.005)  # +0.025 to include upper bound
    tg_values = np.arange(base_tg - 0.02, base_tg + 0.025, 0.005)
    
    # Initialize sensitivity table
    sensitivity_table = pd.DataFrame(
        index=[f"{tg*100:.1f}%" for tg in tg_values],
        columns=[f"{w*100:.1f}%" for w in wacc_values]
    )
    
    # Calculate enterprise value for each combo
    for w in wacc_values:
        for tg in tg_values:
            if w <= tg:
                sensitivity_table.at[f"{tg*100:.1f}%", f"{w*100:.1f}%"] = np.nan
                continue
            
            # Discount years 1-5 FCF
            pv_fcf = sum([fcf / ((1 + w) ** (i + 1)) for i, fcf in enumerate(fcf_values)])
            
            # Terminal value based on Year 5 FCF
            terminal_value = fcf_values[-1] * (1 + tg) / (w - tg)
            pv_terminal = terminal_value / ((1 + w) ** len(fcf_values))
            
            enterprise_value = pv_fcf + pv_terminal
            sensitivity_table.at[f"{tg*100:.1f}%", f"{w*100:.1f}%"] = enterprise_value
    
    # Convert to numeric
    sensitivity_table = sensitivity_table.astype(float)
    sensitivity_table.index.name = "Terminal Growth Rate"
    sensitivity_table.columns.name = "Weighted Average Cost of Capital (WACC)"
    # Convert the Enterprise Values in the table to Fair Stock Prices
    total_debt = all_financials['Total Debt'].iloc[-1]
    cash = all_financials['Cash And Cash Equivalents'].iloc[-1]
    net_debt = total_debt - cash
    for col in sensitivity_table.columns:
        for idx in sensitivity_table.index:
            ev = sensitivity_table.at[idx, col]
            if pd.isna(ev):
                continue
            equity_value = ev - net_debt
            fair_stock_price = equity_value / outstanding_shares
            sensitivity_table.at[idx, col] = fair_stock_price
    return sensitivity_table
    
