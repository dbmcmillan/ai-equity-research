import pandas as pd
from create_charts import create_stock_vs_spy_chart
from forecast_from_projections import create_forecast_table
import parser
import sensitivity_table
import summarizer
import pypandoc
import json
import os
import concurrent.futures
import summarize_document
from download_financials import download_financials_db
from download_financials import calculate_drivers, download_outstanding_shares
from financial_statement_agent import summarize_financials
from financial_statement_agent import summarize_drivers
from projection_agent import projection_agent
from financial_metrics import FinancialMetrics
from stock_history import fetch_stock_data_db
from project_cash_flow import parse_projections_table, calculate_valuation_metrics
from report_writing_agents import master_agent, introduction_agent, industry_investment_agent, financials_risks_agent, esg_appendices_agent
from calculate_multiples import create_multiples_df
from sensitivity_table import create_sensitivity_table
import time
from datetime import date

# region Initialization and loading tickers 
print("Agent initialization complete. Starting summarization process...")
ticker = "RHI"
competitors_tickers = ["MAN", "KFY", "KFRC"]
# endregion

# region Summarizing 10-Q, 10-K, and Earnings Call Documents
if os.path.exists(f"checkpoints/10Q_Summaries/{ticker}_10Q_Summary.txt"):
    with open(f"checkpoints/10Q_Summaries/{ticker}_10Q_Summary.txt", "r", encoding="utf-8") as f:
        summary_text_10Q = f.read()
    print("10-Q summary loaded from existing file.")
else:
    summary_text_10Q = summarize_document.summarize_document(ticker, "10Q", f"reports/10Q/{ticker}_10Q.pdf")
    time.sleep(120)
    print("10-Q summarization complete. Taking a 2-minute break...")

if os.path.exists(f"checkpoints/10K_Summaries/{ticker}_10K_Summary.txt"):
    with open(f"checkpoints/10K_Summaries/{ticker}_10K_Summary.txt", "r", encoding="utf-8") as f:
        summary_text_10K = f.read()
    print("10-K summary loaded from existing file.")
else:
    summary_text_10K = summarize_document.summarize_document(ticker, "10K", f"reports/10K/{ticker}_10K.pdf")
    time.sleep(120) 
    print("10-K summarization complete. Taking a 2-minute break...")
if os.path.exists(f"checkpoints/Earnings_Summaries/{ticker}_earnings_Summary.txt"):
    with open(f"checkpoints/Earnings_Summaries/{ticker}_earnings_Summary.txt", "r", encoding="utf-8") as f:
        summary_text_earnings = f.read()
    print("Earnings call summary loaded from existing file.")
else:
    summary_text_earnings = summarize_document.summarize_document(ticker, "earnings", f"reports/Earnings/{ticker}_earnings.pdf")
    print("Earnings call summarization complete. Taking a 2-minute break...")
    time.sleep(60)
# endregion

# region Uploading financials, drivers, outstanding shares
all_financials = download_financials_db(ticker)
drivers_df = calculate_drivers(all_financials)
outstanding_shares = download_outstanding_shares(ticker)
print(all_financials)
print("Financial data downloaded and parsed. Taking a 2-minute break...")
# endregion

# region Summarizing financials and drivers
if os.path.exists(f"checkpoints/Financials_Summaries/{ticker}_Financials_Summary.txt"):
    with open(f"checkpoints/Financials_Summaries/{ticker}_Financials_Summary.txt", "r", encoding="utf-8") as f:
        financials_summary = f.read()
    print("Financials summary loaded from existing file.")
else:
    financials_summary = summarize_financials(all_financials)
    #Save financials summary
    output_financials_path = f"checkpoints/Financials_Summaries/{ticker}_Financials_Summary.txt"
    with open(output_financials_path, "w", encoding="utf-8") as f:
        f.write(financials_summary)
print("Financial data summarized. Taking a 2-minute break...")
#Check if drivers summary already exists and use it if so
if os.path.exists(f"checkpoints/Drivers_Summaries/{ticker}_Drivers_Summary.txt"):
    with open(f"checkpoints/Drivers_Summaries/{ticker}_Drivers_Summary.txt", "r", encoding="utf-8") as f:
        drivers_summary = f.read()
    print("Drivers summary loaded from existing file.")
else:
    drivers_summary = summarize_drivers(drivers_df)
    #Save drivers summary
    output_drivers_path = f"checkpoints/Drivers_Summaries/{ticker}_Drivers_Summary.txt"
    with open(output_drivers_path, "w", encoding="utf-8") as f:
        f.write(drivers_summary)
    time.sleep(60)  # 120 seconds = 2 minutes
print("Drivers data summarized. Taking a 2-minute break...")
# endregion

# region Creating Projections and Forecast Tables
if os.path.exists(f"reports/Projections/{ticker}_Projections_Table.csv"):
    with open(f"reports/Projections/{ticker}_Projections_Table.csv", "r", encoding="utf-8") as f:
        projections_table = f.read()
    #Return Projections table as a string
    print("Projections table loaded from existing file.")
else:
    projections_table = projection_agent(summary_text_10K, summary_text_10Q, summary_text_earnings, financials_summary, drivers_summary)
    # Save the projections table
    output_projections_path = f"reports/Projections/{ticker}_Projections_Table.csv"
    with open(output_projections_path, "w", encoding="utf-8") as f:
        f.write(projections_table)
    print(f"Projections table saved to: {output_projections_path}")
print("Projections table created. Taking a 2-minute break...")
#Check if forecast table already exists and use it if so
if os.path.exists(f"reports/Forecast_Tables/{ticker}_Forecast_Table.csv"):
    with open(f"reports/Forecast_Tables/{ticker}_Forecast_Table.csv", "r", encoding="utf-8") as f:
        forecast_table = f.read()
    print("Forecast table loaded from existing file.")
    forecast_text = forecast_table
else:
    forecast_table = create_forecast_table(projections_table, all_financials)
    # Save the forecast table
    output_forecast_path = f"reports/Forecast_Tables/{ticker}_Forecast_Table.csv"
    with open(output_forecast_path, "w", encoding="utf-8") as f:
        f.write(forecast_table.to_csv())
    print(f"Forecast table saved to: {output_forecast_path}")
    forecast_text = forecast_table.to_csv()
print("Forecast table created. Taking a 2-minute break...")
# endregion

# region Download stock data and calculating financial metrics

ticker_df = fetch_stock_data_db(ticker)
spy_df = fetch_stock_data_db("SPY")
print("Stock data downloaded.")

# Create the financial metrics instance:
stock_metrics = FinancialMetrics(ticker_df, spy_df, risk_free_rate=0.041, all_financials=all_financials)
# Calculate financial metrics
projections_df = parse_projections_table(projections_table)
stock_metrics.calculate_wacc()
time.sleep(60)
important_stock_metrics = {
    "Beta": stock_metrics.beta,
    "WACC": stock_metrics.wacc,
    "Current Price": ticker_df['Close'].iloc[-1]
}
print("Important stock metrics:", important_stock_metrics)
# endregion

# region Custom Stock Metrics Input
#Give the user option to use custom stock metrics
print("Do you want to input custom stock metrics? (y/n)")
user_input = input().strip().lower()
if user_input == 'y':
    print("Enter custom Beta (or press Enter to keep calculated value):")
    beta_input = input().strip()
    if beta_input:
        stock_metrics.beta = float(beta_input)
        important_stock_metrics['Beta'] = float(beta_input)
    print("Enter custom WACC (or press Enter to keep calculated value):")
    wacc_input = input().strip()
    if wacc_input:
        stock_metrics.wacc = float(wacc_input)
        important_stock_metrics['WACC'] = float(wacc_input)
    print("Enter custom Current Price (or press Enter to keep calculated value):")
    price_input = input().strip()
    if price_input:
        important_stock_metrics["Current Price"] = float(price_input)
else:
    print("Using calculated stock metrics.")
# endregion

# region Valuation Metrics
#Check if valuation metrics already exists and use it if so
if os.path.exists(f"reports/{ticker}_Valuation_Metrics.json"):
    with open(f"reports/{ticker}_Valuation_Metrics.json", "r", encoding="utf-8") as f:
        valuation_metrics = json.load(f)
    print("Valuation metrics loaded from existing file.")
else:
    valuation_metrics = calculate_valuation_metrics(projections_df, stock_metrics.wacc, ticker, outstanding_shares)
#Save valuation metrics
output_valuation_path = f"reports/Valuation_Metrics/{ticker}_Valuation_Metrics.json"
with open(output_valuation_path, "w", encoding="utf-8") as f:
    json.dump(valuation_metrics, f, indent=4)
print(f"Valuation metrics saved to: {output_valuation_path}")
print("Financial metrics calculated. Taking a 1-minute break...")
time.sleep(60)
# Load additional analyst notes from word document if exists
analyst_notes_path = f"reports/Analyst_Notes/{ticker}_Analyst_Notes.docx"
if os.path.exists(analyst_notes_path):
    additional_notes = parser.extract_text_from_docx(analyst_notes_path)
    print("Additional analyst notes loaded.")
# endregion

# region Creating Multiples Table and Sensitivity Table
# Create multiples table for stock and comparable companies
multiples_df = create_multiples_df(ticker, competitors_tickers)
multiples_output_path = f"reports/Competitor_Multiples/{ticker}_and_Competitors_Multiples.csv"
multiples_df.to_csv(multiples_output_path)
#Store it as a string for later inclusion in the report
multiples_table_str = multiples_df.to_csv(index=False)
print(f"Multiples table saved to: {multiples_output_path}")
print(multiples_table_str)
#Check if sensitivity table already exists and use it if so
if os.path.exists(f"checkpoints/Sensitivity_Tables/{ticker}_Sensitivity_Table.csv"):
    with open(f"checkpoints/Sensitivity_Tables/{ticker}_Sensitivity_Table.csv", "r", encoding="utf-8") as f:
        sensitivity_table = pd.read_csv(f, index_col=0)
    print("Sensitivity table loaded from existing file.")
else:
    sensitivity_table = create_sensitivity_table(projections_df, all_financials, stock_metrics.wacc, outstanding_shares)
    print("Sensitivity table created:")
#Format sensitivity table as string csv for later inclusion in the report
sensitivity_table_str = sensitivity_table.to_csv(index=True)
#Save sensitivity table in checkpoints folder
sensitivity_output_path = f"checkpoints/Sensitivity_Tables/{ticker}_Sensitivity_Table.csv"
sensitivity_table.to_csv(sensitivity_output_path)
print(f"Sensitivity table saved to: {sensitivity_output_path}")
# endregion

# region Creating Report Sections
#Check if the introduction section already exists and use it if so
if os.path.exists(f"checkpoints/Report_Sections/{ticker}_Introduction_Section.txt"):
    with open(f"checkpoints/Report_Sections/{ticker}_Introduction_Section.txt", "r", encoding="utf-8") as f:
        first_two_sections = f.read()
    print("Introduction section loaded from existing file.")
else:
    first_two_sections = introduction_agent(summary_text_10K, summary_text_10Q, summary_text_earnings, financials_summary, drivers_summary, projections_table, valuation_metrics, important_stock_metrics, additional_notes)
    with open(f"checkpoints/Report_Sections/{ticker}_Introduction_Section.txt", "w", encoding="utf-8") as f:
        f.write(first_two_sections)
        time.sleep(120)
print("First two sections of the report completed. Taking a 1-minute break...")

# Check if the second two sections already exists and use it if so
if os.path.exists(f"checkpoints/Report_Sections/{ticker}_Industry_Investment_Section.txt"):
    with open(f"checkpoints/Report_Sections/{ticker}_Industry_Investment_Section.txt", "r", encoding="utf-8") as f:
        second_two_sections = f.read()
    print("Industry and Investment section loaded from existing file.")
else:
    second_two_sections = industry_investment_agent(summary_text_10K, summary_text_10Q, summary_text_earnings, financials_summary, drivers_summary, projections_table, valuation_metrics, important_stock_metrics, additional_notes, first_two_sections, multiples_table_str)
    with open(f"checkpoints/Report_Sections/{ticker}_Industry_Investment_Section.txt", "w", encoding="utf-8") as f:
        f.write(second_two_sections)
        time.sleep(120)
print("Second two sections of the report completed. Taking a 1-minute break...")
#Check if the third two sections already exists and use it if so
if os.path.exists(f"checkpoints/Report_Sections/{ticker}_Financials_Risks_Section.txt"):
    with open(f"checkpoints/Report_Sections/{ticker}_Financials_Risks_Section.txt", "r", encoding="utf-8") as f:
        third_two_sections = f.read()
    print("Financials and Risks section loaded from existing file.")
else:
    third_two_sections = financials_risks_agent(summary_text_10K, summary_text_10Q, summary_text_earnings, financials_summary, drivers_summary, projections_table, valuation_metrics, important_stock_metrics, additional_notes, first_two_sections, second_two_sections, sensitivity_table_str, forecast_text)
    with open(f"checkpoints/Report_Sections/{ticker}_Financials_Risks_Section.txt", "w", encoding="utf-8") as f:  
        f.write(third_two_sections)
        time.sleep(120)
print("Third two sections of the report completed. Taking a 1-minute break...")
#Check if the remaining sections already exists and use it if so
if os.path.exists(f"checkpoints/Report_Sections/{ticker}_ESG_Appendices_Section.txt"):
    with open(f"checkpoints/Report_Sections/{ticker}_ESG_Appendices_Section.txt", "r", encoding="utf-8") as f:
        remaining_sections = f.read()
    print("ESG and Appendices section loaded from existing file.")
else:
    remaining_sections = esg_appendices_agent(summary_text_10K, summary_text_10Q, summary_text_earnings, financials_summary, drivers_summary, projections_table, valuation_metrics, important_stock_metrics, additional_notes, first_two_sections, second_two_sections, third_two_sections)
    with open(f"checkpoints/Report_Sections/{ticker}_ESG_Appendices_Section.txt", "w", encoding="utf-8") as f:
        f.write(remaining_sections)
        time.sleep(120)
print("Remaining sections of the report completed. Taking a 1-minute break...")
today_date = date.today()
equity_report = master_agent(first_two_sections, second_two_sections, third_two_sections, remaining_sections, additional_notes, today_date)
# Save the final equity research report
output_report_path = f"reports/Equity_Research_Reports/{ticker}_Equity_Research_Report.md"
with open(output_report_path, "w", encoding="utf-8") as f:
    f.write(equity_report)
print(f"Equity research report saved to: {output_report_path}")
print("Equity research report generation complete.")
# endregion

"""
# region Creating and Saving Visualizations

chart = create_stock_vs_spy_chart(ticker_df, spy_df, ticker)
#Save the chart as HTML
chart_output_path = f"reports/Visualizations/{ticker}_vs_SPY_chart.html"
chart.write_html(chart_output_path)
print(f"Stock vs SPY chart saved to: {chart_output_path}")

# Combine the full Equity Report and the stock chart into a single html file and then convert to PDF
combined_html_path = f"reports/Equity_Research_Reports/{ticker}_Equity_Research_Report.html"

with open(combined_html_path, "w", encoding="utf-8") as f:
    # Convert markdown report to HTML
    report_html = pypandoc.convert_file(output_report_path, 'html')
    f.write(report_html)
    # Append the chart HTML
    with open(chart_output_path, "r", encoding="utf-8") as chart_file:
        chart_html = chart_file.read()
        f.write("<h2>Stock vs SPY Chart</h2>")
        f.write(chart_html)
pdf_output_path = f"reports/Equity_Research_Reports/{ticker}_Equity_Research_Report.pdf"
pypandoc.convert_file(combined_html_path, 'pdf', outputfile=pdf_output_path)
print(f"Final Equity Research Report with chart saved to: {pdf_output_path}")
# endregion
"""
