# summarizer.py

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Create the client using your API key from .env
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

# -------------------------------
# Chunk-level summarization
# -------------------------------

def summarize_chunk_10K(chunk_text):
    """
    Summarizes a chunk of a 10-K into a concise extractive summary.
    """

    config = types.GenerateContentConfig(
        
    )

    prompt = f"""
Your role is to extract the financially material information from this section of a 10-K.
Focus on risks, opportunities, revenue drivers, cost structure, segment performance,
legal issues, and management commentary. Any numerical values cited should include a page number reference to the original 10-K, if possible.
Produce a concise paragraph (4–6 sentences) containing only the essential facts.

Text to summarize:
{chunk_text}

Summary:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )

    return response.text.strip() # type: ignore

def summarize_chunk_10Q(chunk_text):
    """
    Summarizes a chunk of a 10-Q into a concise extractive summary.
    """

    config = types.GenerateContentConfig(
    
    )

    prompt = f"""
Your role is to extract the financially material information from this section of a 10-Q.
Focus on risks, opportunities, revenue drivers, cost structure, segment performance,
legal issues, and management commentary. Any numerical values cited should include a page number reference to the original 10-Q, if possible.
Produce a concise paragraph (4–6 sentences) containing only the essential facts.

Text to summarize:
{chunk_text}

Summary:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )

    return response.text.strip() # type: ignore

# -------------------------------
# Global executive summary
# -------------------------------

def summarize_chunk_earnings(chunk_text):
    """
    Summarizes a chunk of a 10-K into a concise extractive summary.
    """

    config = types.GenerateContentConfig(
    
    )

    prompt = f"""
Your role is to extract the financially material information from this section of an earnings call transcript.
Focus on risks, opportunities, revenue drivers, cost structure, segment performance,
legal issues, and management commentary. Any numerical values cited should include a page number reference to the original earnings call, if possible.
Produce a concise paragraph (4–6 sentences) containing only the essential facts.

Text to summarize:
{chunk_text}

Summary:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )

    return response.text.strip() # type: ignore
def summarize_summaries_10K(summaries_text):
    """
    Produces a 1–2 page executive investment summary.
    """

    config = types.GenerateContentConfig(
    
    )

    prompt = f"""
You are an equity research analyst preparing a briefing for a senior equity research analyst. Your assistants have summarized a company's 10-K into concise sections.
Using the summarized sections below, produce a 1–2 page investment brief covering:

- key risks
- key opportunities
- business model & revenue drivers
- competitive positioning
- material legal or regulatory issues
- financial health and capital allocation
- outlook

The tone should be analytical and fact-based. Your job is to give the senior analyst the information needed to forecast the company's future performance and write an analysis report to provide to the Portfolio Manager.
Avoid repeating text verbatim. Prioritize what matters for investment decisions. Output the brief in markdown format.

Summarized Sections:
{summaries_text}

Executive 10K Summary:
"""

    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=prompt,
        config=config
    )

    return response.text.strip() # type: ignore

def summarize_summaries_10Q(summaries_text):
    """
    Produces a 1–2 page executive investment summary of a company's 10Q.
    """

    config = types.GenerateContentConfig(
    
    )

    prompt = f"""
You are an equity research analyst preparing a briefing for a senior equity research analyst. Your assistants have summarized a company's 10-Q into concise sections.
Using the summarized sections below, produce a 1–2 page investment brief covering:

- key risks
- key opportunities
- business model & revenue drivers
- competitive positioning
- material legal or regulatory issues
- financial health and capital allocation
- outlook

The tone should be analytical and fact-based. Your job is to give the senior analyst the information needed to forecast the company's future performance and write an analysis report to provide to the Portfolio Manager.
Avoid repeating text verbatim. Prioritize what matters for investment decisions. Output the brief in markdown format.

Summarized Sections:
{summaries_text}

Executive 10K Summary:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )

    return response.text.strip() # type: ignore

def summarize_summaries_earnings(summaries_text):
    """
    Produces a 1–2 page executive investment summary of a company's earnings call transcript.
    """

    config = types.GenerateContentConfig(
    
    )

    prompt = f"""
You are an equity research analyst preparing a briefing for a senior equity research analyst. Your assistants have summarized a company's earnings call transcript into concise sections.
Using the summarized sections below, produce a 1–2 page investment brief covering:

- key risks
- key opportunities
- business model & revenue drivers
- competitive positioning
- material legal or regulatory issues
- financial health and capital allocation
- outlook

The tone should be analytical and fact-based. Your job is to give the senior analyst the information needed to forecast the company's future performance and write an analysis report to provide to the Portfolio Manager.
Avoid repeating text verbatim. Prioritize what matters for investment decisions. Output the brief in markdown format.

Summarized Sections:
{summaries_text}

Executive 10K Summary:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )

    return response.text.strip() # type: ignore