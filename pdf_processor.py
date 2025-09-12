import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract


def read_pdf_text(pdf_path):
    """Try reading text directly from PDF pages."""
    reader = PdfReader(pdf_path)
    text_pages = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text and page_text.strip():
            text_pages.append(page_text)
    return "\n\n".join(text_pages)


def ocr_pdf(pdf_path, lang="ben+eng"):
    """Perform OCR on PDF pages."""
    print(f"No text found in {os.path.basename(pdf_path)}, performing OCR...")
    images = convert_from_path(pdf_path)
    text_pages = []
    for page in images:
        text = pytesseract.image_to_string(page, lang=lang)
        text_pages.append(text)
    return "\n\n".join(text_pages)


def split_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - overlap
    return chunks


def pdf_2_chunks(pdf_path, chunk_size=500, chunk_overlap=50, ocr_lang="ben+eng"):
    """Process a single PDF into text chunks."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # Step 1: Try reading PDF text
    text = read_pdf_text(pdf_path)

    # Step 2: If no text, use OCR
    if not text.strip():
        text = ocr_pdf(pdf_path, lang=ocr_lang)

    # Step 3: Split into chunks
    return split_text(text, chunk_size=chunk_size, overlap=chunk_overlap)


def process_pdfs_in_directory(pdf_directory, chunk_size=500, chunk_overlap=50, ocr_lang="ben+eng"):
    """Process all PDFs in a directory and return a dict of chunks per file."""
    pdf_chunks = []
    for filename in os.listdir(pdf_directory):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            print(f"\nProcessing {filename}...")
            chunks = pdf_2_chunks(pdf_path, chunk_size, chunk_overlap, ocr_lang)
            pdf_chunks.extend(chunks)
            print(f"Total chunks created for {filename}: {len(chunks)}")
    return pdf_chunks


if __name__ == '__main__':
    PDF_DIR = "./data"  # directory with PDFs
    all_chunks = process_pdfs_in_directory(PDF_DIR)

    # Example: print first 3 chunks of each file
    for fname, chunks in all_chunks.items():
        print(f"\n====== {fname} ======")
        for i, c in enumerate(chunks[:3]):
            print(f"\n--- Chunk {i+1} ---\n{c[:300]}...")
