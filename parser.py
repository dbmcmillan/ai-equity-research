# Create function extract_text_from_pdf using pymupdf
import pymupdf as fitz
from docx import Document

def extract_text_from_docx(file_path):
    """
    Extract all text from a Word (.docx) file and return as a single string.
    """
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        if para.text.strip():  # skip empty lines
            full_text.append(para.text.strip())
    return "\n".join(full_text)

# 1. Extract each page
def extract_text_by_page(pdf_path):
    """
    Returns a list of page texts.
    """
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        text = page.get_text("text").replace("\u200b", "")
        pages.append(text)
    return pages


# 2. Group pages into multi-page chunks
def group_pages_into_chunks(pages, pages_per_chunk=2):
    """
    Groups N pages together so you can process 2–3 pages at a time.
    Returns a list of large text blocks, each containing multiple pages.
    """
    chunks = []
    for i in range(0, len(pages), pages_per_chunk):
        group = pages[i:i + pages_per_chunk]
        combined = "\n\n".join(group).strip()
        chunks.append(combined)
    return chunks

def safe_split(chunk_text, max_chars=15000):
    """
    Ensures each chunk stays within token limits.
    Only triggers occasionally if a section is extremely dense.
    """
    if len(chunk_text) <= max_chars:
        return [chunk_text]

    subchunks = []
    for i in range(0, len(chunk_text), max_chars):
        sub = chunk_text[i:i + max_chars].strip()
        if sub:
            subchunks.append(sub)
    return subchunks



