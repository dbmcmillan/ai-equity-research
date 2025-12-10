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
ai-equity-research/
├── main.py                          # Main orchestration script
├── requirements.txt                 # Python dependencies
├── .env                            # API keys (not tracked)
├── .gitignore                      # Git ignore rules
│
├── parser.py                       # PDF/Word document parsing
├── summarizer.py                   # LLM-based summarization
├── summarize_document.py           # Document processing pipeline
├── financial_statement_agent.py    # Financial data extraction
├── projection_agent.py             # Forward projection generation
├── report_writing_agents.py        # Report section generation
│
├── download_financials.py          # Financial data retrieval
├── financial_metrics.py            # WACC, Beta calculation
├── project_cash_flow.py            # DCF valuation logic
├── sensitivity_table.py            # Valuation sensitivity analysis
├── calculate_multiples.py          # Peer comparable multiples
│
├── create_stock_price_database.py  # Build price database
├── create_financials_database.py   # Build financials database
├── stock_history.py                # Stock price utilities
│
├── checkpoints/                    # Intermediate summaries (not tracked)
├── reports/                        # Input docs & output reports
└── README.md                       # This file
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

- [ ] Add relative valuation methods (P/E, EV/Sales comparables)
- [ ] Integrate real-time news sentiment analysis
- [ ] Build web interface for non-technical users
- [ ] Add Monte Carlo simulation for valuation ranges
- [ ] Incorporate ESG scoring APIs
- [ ] Support international companies (non-US exchanges)

## 📫 Contact

**David McMillan**
- Email: dbmcmillan@gmail.com
- LinkedIn: [your-linkedin-url]
- GitHub: [your-github-username]

---

**Built with:** Python 3.12 | Google Gemini | Pandas | yfinance | Scikit-learn

**License:** MIT (or choose another - MIT is most permissive)