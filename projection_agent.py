# Create an agent that reads the summaries of 10K, 10Q, and earnings call documents, and produces a table of projections for years 1-5, and year 6+ (terminal value) in tabular format.
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()
# Create the client using your API key from .env
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
def projection_agent(summary_text_10K, summary_text_10Q, summary_text_earnings, financials_summary, drivers_summary):
    """
    Creates financial projections based on summaries of 10K, 10Q, and earnings call documents.
    Outputs a table of projections for years 1-5 and year 6+ (terminal value).
    """
    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.HIGH)
    )

    prompt = f"""You are a senior equity research analyst. Your team has provided you with executive summaries from the company's latest 10-K, 10-Q, and earnings call documents. They have also provided you with tables of time series financial information and historical values for financial drivers, obtained from the company's financial statements.
    Take note of the dates of the documents and tables to gain understanding of the timeline of events.
    Using this information, create a detailed financial projection table for the next 5 years and a terminal value for year 6+. For each year, include growth/decline projections for:
- Revenue
- EBIT
- Net Income
- Free Cash Flow
Create a projection for 3 scenarios: bull case, bear case, and base case. Provide a 1-2 sentence rationale for each year's projections in each scenario.
Format the output as a markdown table with the following columns:
- Year
- Bear/Base/Bull Case
- Revenue Growth (%)
- EBIT Growth (%)
- Net Income Growth (%)
- Free Cash Flow Growth (%)
- Rationale
Use the following summaries to inform your projections:
--- 10-K Summary ---
{summary_text_10K}
--- 10-Q Summary ---
{summary_text_10Q}
--- Earnings Call Summary ---
{summary_text_earnings}
--- Financials Summary ---
{financials_summary}
--- Financial Drivers Summary ---
{drivers_summary}
Format the table in csv format. Do not include any text outside the table. Every row must have a value in every column. Use 'TV' as the value in the year column for terminal value rows. Output the table strictly in csv format, with these columns, in this order:
Year, Case, Revenue Growth (%), EBIT Growth (%), Net Income Growth (%), Free Cash Flow Growth (%), Rationale. In the Case column, use only the values 'Bear', 'Base', or 'Bull'. Think carefully about the numbers you choose and ensure that the three cases are not overly disparate from each other.
"""
    response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents=prompt,
    config=config
    )

    return response.text.strip() # type: ignore