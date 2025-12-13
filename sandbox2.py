from summarize_document import summarize_document
from parser import extract_text_by_page, extract_text_from_docx
import os
ticker = "LULU"
doc_type = "10Q"

summary_text_10Q = summarize_document(ticker, "10Q", f"reports/10Q/{ticker}_10Q.pdf")

#Store the summary in a text file called {ticker}_10Q_Update.txt in the reports/10Q_Summaries/ directory
with open(f"checkpoints/10Q_Summaries/{ticker}_10Q_Update.txt", "w") as f:
    f.write(summary_text_10Q)