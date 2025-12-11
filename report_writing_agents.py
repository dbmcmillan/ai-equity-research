# Next steps - document the internal thoughts and reasoning of each agent for transparency and debugging.
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from datetime import date

load_dotenv()
# Create the client using your API key from .env
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

# Create a date variable


# Create a date variable
def introduction_agent(summary_text_10K, summary_text_10Q, summary_text_earnings, financials_summary, drivers_summary, projections_table, valuation_metrics, important_stock_metrics, additional_notes):
    """
    Creates an introduction to an equity research report based on summaries of 10K, 10Q, earnings call, financial statements, and projections.
    """
    config = types.GenerateContentConfig(
        
    )

    prompt = f"""You are a senior equity research analyst. Your team has provided you with executive summaries from the company's latest 10-K, 10-Q, and earnings call documents. They have also provided you with tables of time series financial information and historical values for financial drivers, obtained from the company's financial statements. Finally, they have provided you with a detailed financial projection table for the next 5 years and a terminal value for year 6+.
    Your job is to write the first two sections of a comprehensive equity research report covering the following sections:
    1. Basic Information (ticker symbol, primary exchange, sector and industry, investment recommendation, current stock price, target price, and risk level).
    2. Business Description (summary of the company's business model, detailed description of products/services, clear description of the company's economics, including a discussion of key drivers of revenues and expenses). This section should be approximately 1-2 pages in length (400-700 words).
    Use the following summaries, projections table, and metrics to inform your report:
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
--- Financial Projections Table ---
{projections_table}
-- Valuation Metrics --
{valuation_metrics}
-- Important Stock Metrics --
{important_stock_metrics}
-- Additional Analyst Notes: The analysts' core thesis is found at the start of these notes, and should thread through the entire report. --
{additional_notes}
Format the report in markdown format with appropriate headings and subheadings. Ensure clarity and professionalism throughout the report. Explain your reasoning and analysis in detail.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )

    return response.text.strip() # type: ignore

def industry_investment_agent(summary_text_10K, summary_text_10Q, summary_text_earnings, financials_summary, drivers_summary, projections_table, valuation_metrics, important_stock_metrics, additional_notes, first_two_sections, multiples_table_str):
    """
    Creates an introduction to an equity research report based on summaries of 10K, 10Q, earnings call, financial statements, and projections.
    """
    config = types.GenerateContentConfig(
    
    )

    prompt = f"""You are a senior equity research analyst. Your team has provided you with executive summaries from the company's latest 10-K, 10-Q, and earnings call documents. They have also provided you with tables of time series financial information and historical values for financial drivers, obtained from the company's financial statements. Finally, they have provided you with a detailed financial projection table for the next 5 years and a terminal value for year 6+.
    Your collegue has already written the first two sections of a comprehensive equity research report, which have been provided. Your job is to write the third and fourth sections of the report covering the following sections (Each section should be 1-2 pages in length, approximately 400-700 words each):
    3. Industry Overview and Competitive Positioning (analysis of the industry landscape, key competitors/peer companies, and the company's competitive advantages/disadvantages). Include a section rating the company's competitive "moat". Include another section using "Porter's Five Forces" framework to analyze the industry's competitive dynamics. Also consider production capacity levels, pricing, distribution, and stability of market share.
    4. Investment Summary (brief description of the company, significant recent developments, forecast table, valuation summary, and investment thesis). Include a clear and concise explanation as to why the security is deemed to be mispriced relative to its intrinsic value. What is the market not properly discounting, and what will prompt the market to re-price the security?
    Use the following summaries, projections table, and metrics to inform your report:
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
--- Financial Projections Table ---
{projections_table}
-- Valuation Metrics --
{valuation_metrics}
-- Important Stock Metrics --
{important_stock_metrics}
-- Additional Analyst Notes. The analysts' core thesis is found at the start of these notes, and should thread through the entire report. --
{additional_notes}
-- First Two Sections --
{first_two_sections}
-- Include this table of multiples for the stock and comparable companies, in markdown format --
{multiples_table_str}
Format the report in markdown format with appropriate headings and subheadings. Ensure clarity and professionalism throughout the report. Explain your reasoning and analysis in detail. Return only the sections you were instructed to write, without including the previously written sections.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )

    return response.text.strip() # type: ignore

def financials_risks_agent(summary_text_10K, summary_text_10Q, summary_text_earnings, financials_summary, drivers_summary, projections_table, valuation_metrics, important_stock_metrics, additional_notes, first_two_sections, second_two_sections, sensitivity_table_str, forecast_text):
    """
    Creates an introduction to an equity research report based on summaries of 10K, 10Q, earnings call, financial statements, and projections.
    """
    config = types.GenerateContentConfig(
    
    )

    prompt = f"""You are a senior equity research analyst. Your team has provided you with executive summaries from the company's latest 10-K, 10-Q, and earnings call documents. They have also provided you with tables of time series financial information and historical values for financial drivers, obtained from the company's financial statements. Finally, they have provided you with a detailed financial projection table for the next 5 years and a terminal value for year 6+.
    Your collegues have already written the first four sections of a comprehensive equity research report, which have been provided. Your job is to write the third and fourth sections of the report covering the following sections (Each section should be 1-2 pages in length, approximately 400-700 words each):
    5. Financial Analysis (detailed analysis of the company's historical financial performance and a forecast of future performance, key financial metrics, and trends). Show sufficient skepticism toward management's guidance and forecasts. Highlight any discrepancies between management's statements and the data from financial statements. Identify any unusual accounting practices or one-time items that may distort the true financial health of the company.
    6. Investment Risks (key risks to the investment thesis and potential mitigants. Make note of risks that are operational, finacial, legal, or regulatory). Note any red flag in disclosures, footnotes, or MD&A sections of financial statements (such as "qualified opinions" from auditors or weakness in internal control over financial reporting). Consider industry-specific risks as well as broader macroeconomic risks that could impact the company's performance.
    Use the following summaries, projections table, and metrics to inform your report:
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
--- Financial Projections Table ---
{projections_table}
-- Valuation Metrics --
{valuation_metrics}
-- Important Stock Metrics --
{important_stock_metrics}
-- Additional Analyst Notes. The analysts' core thesis is found at the start of these notes, and should thread through the entire report. --
{additional_notes}
-- First Two Sections --
{first_two_sections}
-- Second Two Sections --
{second_two_sections}
-- Include this sensitivity table for the stock valuation. Format the values within the table as currency in dollars, and return the table in markdown format --
{sensitivity_table_str}
-- Include this forecast table for Revenue, EBIT, Net Income, and Free Cash Flow for our base case scenario. Format the values within the table as currency in dollars, and return the table in markdown format --
{forecast_text}
Format the report in markdown format with appropriate headings and subheadings. Ensure clarity and professionalism throughout the report. Explain your reasoning and analysis in detail. Return only the sections you were instructed to write, without including the previously written sections.

"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )

    return response.text.strip() # type: ignore

def esg_appendices_agent(summary_text_10K, summary_text_10Q, summary_text_earnings, financials_summary, drivers_summary, projections_table, valuation_metrics, important_stock_metrics, additional_notes, first_two_sections, second_two_sections, third_two_sections):
    """
    Creates an introduction to an equity research report based on summaries of 10K, 10Q, earnings call, financial statements, and projections.
    """
    config = types.GenerateContentConfig(
    
    )

    prompt = f"""You are a senior equity research analyst. Your team has provided you with executive summaries from the company's latest 10-K, 10-Q, and earnings call documents. They have also provided you with tables of time series financial information and historical values for financial drivers, obtained from the company's financial statements. Finally, they have provided you with a detailed financial projection table for the next 5 years and a terminal value for year 6+.
    Your collegues have already written the first four sections of a comprehensive equity research report, which have been provided. Your job is to complete the remainder of the report by writing the following remaining sections (Each section should be 1-2 pages in length, approximately 400-700 words each):
    7. Environmental, Social, and Governance (ESG) Considerations (analysis of the company's ESG practices and their impact on the investment thesis).
    8. Analyst Note on the most recent earnings call (key takeaways and implications for the investment thesis).
    9. Appendices (financial projection table and any other relevant data or charts).
    Use the following summaries, projections table, and metrics to inform your report:
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
--- Financial Projections Table ---
{projections_table}
-- Valuation Metrics --
{valuation_metrics}
-- Important Stock Metrics --
{important_stock_metrics}
-- Additional Analyst Notes. The analysts' core thesis is found at the start of these notes, and should thread through the entire report. --
{additional_notes}
-- First and Second Sections --
{first_two_sections}
-- Third and Fourth Sections --
{second_two_sections}
-- Fifth and Sixth Sections --
{third_two_sections}
Format the report in markdown format with appropriate headings and subheadings. Ensure clarity and professionalism throughout the report. Explain your reasoning and analysis in detail. Return only the sections you were instructed to write, without including the previously written sections.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )

    return response.text.strip()  # type: ignore



def master_agent(first_two_sections, second_two_sections, third_two_sections, remaining_sections, additional_notes, today_date):
    """
    Creates an introduction to an equity research report based on summaries of 10K, 10Q, earnings call, financial statements, and projections.
    """
    config = types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.HIGH)
    )

    prompt = f"""You are the Director of Equity Research for a large asset management company. Your senior equity research team has put together a comprehensive equity research report on a particular stock, split into four main sections plus appendices, which have been provided.
    Your job is to function as the Editor-in-Chief and combine all the sections into a single cohesive report. Ensure smooth transitions between sections, consistent tone and style, and overall clarity and professionalism. Do not make any major changes to the content of each section, but feel free to make minor edits for flow and coherence. 
    Ensure that the investment thesis is clear and well-supported throughout the report. Remove any unnecessary repetition, redundancy, and rephrase anything that sound like unnatural "LLM-speak", but do not delete any unique information or abbreviate any tables you were provided. Ensure that that the final report communicates the thesis (provided at the beginning of additional analyst notes) FORCEFULLY.
    Format the final report in markdown format with appropriate headings and subheadings.
-- First and Second Sections --
{first_two_sections}
-- Third and Fourth Sections --
{second_two_sections}
-- Fifth and Sixth Sections --
{third_two_sections}
-- 7th, 8th, and 9th Sections --
{remaining_sections}
--{additional_notes}--
Take note of today's date at the beginning of the report: {today_date}. Format the report in markdown format with appropriate headings and subheadings.
"""

    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=prompt,
        config=config
    )

    return response.text.strip()  # type: ignore