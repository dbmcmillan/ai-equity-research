# AI-Powered Equity Research System

An automated machine learning pipeline that generates institutional-quality equity research reports by analyzing SEC filings (10-Ks, 10-Qs) and earnings call transcripts.

## 🎯 Project Overview

This system automates the fundamental equity research workflow that typically takes analysts 40+ hours per report. By leveraging large language models (LLMs) and financial modeling techniques, it produces comprehensive 20-page investment analyses in under 2 hours.

### Key Features

- **Automated Document Analysis**: Extracts material information from 10-Ks, 10-Qs, and earnings transcripts using AI-powered summarization
- **DCF Valuation Models**: Builds discounted cash flow models with sensitivity analysis across multiple scenarios (Bull/Base/Bear)
- **Financial Projections**: Generates 5-year forward projections for revenue, EBIT, net income, and free cash flow
- **Comprehensive Reporting**: Produces professional markdown reports including:
  - Business description and competitive analysis (Porter's Five Forces)
  - Investment thesis with price targets
  - Risk assessment and ESG considerations
  - Peer comparable analysis (P/E, P/B, EV/EBITDA multiples)

### Sample Output

📊 **[Lockheed Martin (LMT) Equity Research Report](reports/LMT_Equity_Research_Report.md)** - Full analysis demonstrating system capabilities

## Research Process & Methodology

### Automated Pipeline Architecture

This system demonstrates a production-quality research workflow:

1. **Document Ingestion** → Parse 10-Ks, 10-Qs, earnings transcripts (see `parser.py`)
2. **Financial Analysis** → Extract metrics from databases (see `download_financials.py`)
3. **AI Summarization** → Generate executive summaries with checkpoint recovery (see `summarize_document.py`)
4. **Projection Modeling** → Create DCF scenarios (see `projection_agent.py`)
5. **Report Generation** → Automated multi-section writing (see `report_writing_agents.py`)

**Key Features:**
- Checkpoint system enables recovery from any pipeline stage
- Parallel processing for efficiency
- Modular architecture allows component-level iteration
- Production error handling and logging

## 🛠️ Technology Stack

- **Python 3.12**: Core programming language
- **Google Gemini API**: LLM for document summarization and report generation
- **Pandas/NumPy**: Financial data manipulation and analysis
- **yfinance**: Historical stock price and financial statement data
- **SQLite**: Local storage for price/financials databases
- **Scikit-learn/Statsmodels**: Time-series forecasting and statistical modeling

## 📦 Installation

### Prerequisites

- Python 3.12 or higher
- Google Gemini API key ([get one here](https://makersuite.google.com/app/apikey))

### Setup

1. **Clone the repository**
```bash
   git clone https://github.com/[dbmcmillan]/ai-equity-research.git
   cd ai-equity-research
```

2. **Create virtual environment**
```bash
   python -m venv venv
   
   # Activate (Windows)
   venv\Scripts\activate
   
   # Activate (Mac/Linux)
   source venv/bin/activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Configure API keys**
   
   Create a `.env` file in the project root:
```
   GENAI_API_KEY=your_google_gemini_api_key_here
```

5. **Build local databases** (optional - enables faster runs)
```bash
   python create_stock_price_database.py
   python create_financials_database.py
```

## 🚀 Usage

### Generate an Equity Research Report

1. **Prepare input documents** in the `reports/` folder:
   - `[TICKER]_10K.pdf` - Annual report
   - `[TICKER]_10Q.pdf` - Quarterly report  
   - `[TICKER]_earnings.docx` - Earnings call transcript

2. **Run the pipeline**:
```bash
   python main.py
```

3. **Follow the prompts** to:
   - Enter the stock ticker (e.g., "LMT")
   - Review/adjust calculated WACC and Beta
   - Wait for checkpoint completion (~2 hours total)

4. **Output**: Find your report at `reports/[TICKER]_Equity_Research_Report.md`

### Architecture Overview
```
Input Documents (10-K, 10-Q, Earnings)
    ↓
Document Parsing & Chunking (parser.py)
    ↓
AI Summarization (summarizer.py, financial_statement_agent.py)
    ↓
Financial Metrics Calculation (financial_metrics.py, download_financials.py)
    ↓
Projection Generation (projection_agent.py)
    ↓
DCF Valuation (project_cash_flow.py, sensitivity_table.py)
    ↓
Report Writing (report_writing_agents.py)
    ↓
Final Report (Markdown)
```

## 📁 Project Structure
```
markdownai-equity-research/
├── main.py                          # Pipeline orchestration - coordinates all agents
├── requirements.txt                 # Python dependencies
├── .env                            # API keys (not tracked)
├── .gitignore                      # Git ignore rules
│
├── Document Processing
│   ├── parser.py                    # PDF/Word extraction (pymupdf, python-docx)
│   ├── summarizer.py                # LLM-based chunk summarization (Gemini)
│   ├── summarize_document.py        # Multi-document pipeline with checkpointing
│   └── financial_statement_agent.py # Extract material facts from financials
│
├── Financial Analysis
│   ├── download_financials.py       # Retrieve statements from local SQLite DB
│   ├── financial_metrics.py         # Calculate WACC, Beta, cost of capital
│   ├── projection_agent.py          # Generate 5-year forecasts (3 scenarios)
│   ├── project_cash_flow.py         # DCF valuation engine
│   ├── sensitivity_table.py         # Terminal growth × WACC sensitivity
│   └── calculate_multiples.py       # Peer comparable analysis (P/E, EV/EBITDA)
│
├── Data Infrastructure
│   ├── create_stock_price_database.py   # Build/update price history DB
│   ├── create_financials_database.py    # Build/update financials DB
│   └── stock_history.py                 # Price data utilities
│
├── Report Generation
│   └── report_writing_agents.py     # Multi-agent report writer (intro, thesis, risks, etc.)
│
├── checkpoints/                     # Intermediate processing stages
│   ├── 10K_Checkpoints/            # Chunked 10-K summaries (JSON)
│   ├── 10Q_Checkpoints/            # Chunked 10-Q summaries (JSON)
│   ├── Earnings_Checkpoints/       # Chunked earnings summaries (JSON)
│   ├── 10K_Summaries/              # Final 10-K executive summaries
│   ├── 10Q_Summaries/              # Final 10-Q executive summaries
│   ├── Earnings_Summaries/         # Final earnings executive summaries
│   ├── Financials_Summaries/       # Financials analysis summaries
│   ├── Drivers_Summaries/          # Financial drivers analysis
│   ├── Report_Sections/            # Individual report sections (pre-merge)
│   └── Sensitivity_Tables/         # Valuation sensitivity matrices
│
├── reports/                         # Source documents & outputs
│   ├── 10K/                        # Input: Annual reports
│   ├── 10Q/                        # Input: Quarterly reports
│   ├── Earnings/                   # Input: Earnings call transcripts
│   ├── Analyst_Notes/              # Input: Manual analyst commentary
│   ├── showcase/                   # Output: Final equity research reports
│   │   ├── RHI_Equity_Research_Report.md
│   │   ├── CROX_Equity_Research_Report.md
│   │   └── LULU_Equity_Research_Report.md
│   ├── Projections/                # Generated forecast tables
│   ├── Forecast_Tables/            # Base/Bull/Bear scenarios
│   ├── Valuation_Metrics/          # DCF output (JSON)
│   ├── Competitor_Multiples/       # Peer analysis (CSV)
│   └── Visualizations/             # Charts (HTML, PNG)
│
└── README.md                        # Documentation

```

## 🎓 Background & Motivation

This project was developed as part of my transition from business intelligence/data analysis into equity research and investment analysis. Key objectives:

1. **Demonstrate financial modeling expertise** (CFA Level II candidate)
2. **Showcase Python/ML engineering skills** for quantitative finance roles
3. **Automate repetitive research tasks** to focus on high-value analysis
4. **Build portfolio piece** for buy-side/sell-side analyst applications

## ⚠️ Limitations & Disclaimers

- **Not investment advice**: This system is for educational/demonstration purposes only
- **AI-generated content**: Reports require human review for accuracy and reasonableness
- **API costs**: Gemini API calls cost ~$2-5 per report depending on document size
- **Data quality**: Relies on yfinance data, which may have gaps or inaccuracies
- **Model assumptions**: DCF valuations are sensitive to WACC and terminal growth rate inputs

## 🔮 Future Enhancements

- [ ] Integrate real-time news sentiment analysis
- [ ] Build web interface for non-technical users
- [ ] Add Monte Carlo simulation for valuation ranges
- [ ] Incorporate ESG scoring APIs
- [ ] Support international companies (non-US exchanges)

## 📫 Contact

**David McMillan**
- Email: dbmcmillan@gmail.com
- LinkedIn: [www.linkedin.com/in/david-mcmillan-51674018a]
- GitHub: [dbmcmillan]

---

**Built with:** Python 3.12 | Google Gemini | Pandas | yfinance | Scikit-learn

**License:** MIT