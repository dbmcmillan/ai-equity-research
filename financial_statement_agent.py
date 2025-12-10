# financial_statement_agent.py 
# Create a Gemini agent to analyze financial statement information and provide insights/summaries
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

# Create the client using your API key from .env
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
def summarize_financials(all_financials:pd.DataFrame):
    all_financials_str = all_financials.to_string()
    """
    Provides material information from a set of financial statements.
    """

    config = types.GenerateContentConfig(
    
    )

    prompt = f"""
    You are a research assistant to a senior equity research analyst. Your job is to extract financially material information from the following document or dataset. Focus on facts that could influence forecasts or investment decisions. Note both risks and positive indicators, and summarize your findings in a bulleted list of 1/2 to 1 page. Do not provide opinions, recommendations, or editorialize; stick to verifiable information.
    {all_financials_str}

    Summary:
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )

    return response.text.strip() # type: ignore

def summarize_drivers(drivers_df:pd.DataFrame):
    drivers_str = drivers_df.to_string()
    """
    Provides information on financial drivers.
    """

    config = types.GenerateContentConfig(
    
    )

    prompt = f"""
    You are a research assistant to a senior equity research analyst. Your job is to extract financially material information from the following dataset of financial drivers for a company. Focus on facts that could influence forecasts or investment decisions. Note both risks and positive indicators, and summarize your findings in a bulleted list of 1/2 to 1 page. Do not provide opinions, recommendations, or editorialize; stick to verifiable information.
    {drivers_str}

    Summary:
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )

    return response.text.strip() # type: ignore