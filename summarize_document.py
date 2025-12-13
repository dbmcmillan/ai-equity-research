import os
import json
import concurrent.futures
import summarizer  # your module
import parser      # your PDF/Word parsing module

def summarize_document(ticker, doc_type, file_path, checkpoint_dir="checkpoints", pages_per_chunk_map=None):
    """
    Summarizes a document (10K, 10Q, or earnings call) and saves an executive summary as a text file.

    ticker: string, stock ticker
    doc_type: "10K", "10Q", or "earnings"
    file_path: path to PDF (10K/10Q) or Word (earnings)
    checkpoint_dir: folder to save checkpoint JSON and summary
    pages_per_chunk_map: dict specifying chunk size per doc type
    """
    print(f"{doc_type} Agent Initialized")

    if pages_per_chunk_map is None:
        pages_per_chunk_map = {"10K": 3, "10Q": 2, "earnings": 1}

    # Correct functions for each doc type
    chunk_fn_map = {
        "10K": summarizer.summarize_chunk_10K,
        "10Q": summarizer.summarize_chunk_10Q,
        "earnings": summarizer.summarize_chunk_earnings
    }
    summary_fn_map = {
        "10K": summarizer.summarize_summaries_10K,
        "10Q": summarizer.summarize_summaries_10Q,
        "earnings": summarizer.summarize_summaries_earnings
    }

    if doc_type not in chunk_fn_map:
        raise ValueError(f"Unknown doc_type {doc_type}")

    chunk_fn = chunk_fn_map[doc_type]
    summary_fn = summary_fn_map[doc_type]

    checkpoint_file = os.path.join(checkpoint_dir, f"{doc_type}_Checkpoints/{ticker}_{doc_type}_checkpoint.json")
    output_txt = os.path.join(checkpoint_dir, f"{doc_type}_Summaries/{ticker}_{doc_type}_Summary.txt")
    os.makedirs(checkpoint_dir, exist_ok=True)

    # Extract pages
    if doc_type in ["10K", "10Q", "earnings"]:
        pages = parser.extract_text_by_page(file_path)
    else:
        pages = parser.extract_text_from_docx(file_path).split("\n\n")

    # Group pages/paragraphs into chunks
    pages_per_chunk = pages_per_chunk_map.get(doc_type, 1)
    page_groups = parser.group_pages_into_chunks(pages, pages_per_chunk=pages_per_chunk)

    # Load existing checkpoint
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r", encoding="utf-8") as f:
            flattened_summaries = json.load(f)
    else:
        flattened_summaries = []

    # Count total chunks of text (after safe splitting)
    total_chunks = sum(len(parser.safe_split(group)) for group in page_groups)

    # Start from however many chunks we already summarized
    current_chunk = 0

    try:
        for group in page_groups:
            safe_chunks = parser.safe_split(group)

            for chunk in safe_chunks:

                # Skip if already summarized
                if current_chunk < len(flattened_summaries):
                    current_chunk += 1
                    continue

                print(f"Summarizing chunk {current_chunk + 1}/{total_chunks}...")

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(chunk_fn, chunk)
                    try:
                        summary = future.result(timeout=90)
                    except concurrent.futures.TimeoutError:
                        print(f"Chunk {current_chunk + 1} timed out. Skipping...")
                        summary = "SUMMARY TIMED OUT"

                flattened_summaries.append(summary)
                current_chunk += 1

                # Save checkpoint immediately
                with open(checkpoint_file, "w", encoding="utf-8") as f:
                    json.dump(flattened_summaries, f, ensure_ascii=False, indent=2)

                if current_chunk >= total_chunks:
                    break

    except KeyboardInterrupt:
        print(f"\nStopped manually at chunk {current_chunk}. Progress saved.")

    # Combine summaries and produce final executive summary
    combined_text = "\n".join(flattened_summaries)
    executive_summary = summary_fn(combined_text)

    # Save final summary
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(executive_summary)

    print(f"Saved summary to: {output_txt}")
    print("Summarization complete.")
    return executive_summary

