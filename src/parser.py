import os
from pypdf import PdfReader

def extract_and_chunk_pdf(pdf_path, chunk_size=500, overlap=100):
    """
    Reads a PDF and splits it into overlapping text chunks.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Could not find PDF at {pdf_path}")
        
    reader = PdfReader(pdf_path)
    full_text = ""
    
    # Extract text from each page
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
            
    # Simple character-based sliding window chunking
    chunks = []
    start = 0
    while start < len(full_text):
        end = start + chunk_size
        chunk = full_text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
        
    return chunks

if __name__ == "__main__":
    # Test the parser
    sample_path = "data/sample.pdf"
    # Ensure you put a dummy PDF in data/sample.pdf to test
    try:
        chunks = extract_and_chunk_pdf(sample_path)
        print(f"Successfully split PDF into {len(chunks)} chunks.")
        print(f"Sample Chunk 1:\n{chunks[0][:150]}...")
    except FileNotFoundError:
        print(f"Please place a sample PDF at '{sample_path}' to test.")