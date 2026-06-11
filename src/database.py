import os
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from parser import extract_and_chunk_pdf

# Load environment variables from .env
load_dotenv()

# Initialize MongoDB Client
mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["faq_db"]
collection = db["embedded_chunks"]

# Load a highly popular, free, local embedding model
print("Loading local embedding model (all-MiniLM-L6-v2)...")
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def get_embedding(text):
    """Generates a local vector embedding (384 dimensions)."""
    # Convert numpy array output to a standard Python float list for MongoDB
    return embedding_model.encode(text).tolist()

def upload_documents_to_atlas(pdf_path):
    """Parses a PDF, embeds the chunks locally, and uploads them to MongoDB Atlas."""
    print(f"Parsing document: {pdf_path}...")
    chunks = extract_and_chunk_pdf(pdf_path)
    
    documents_to_insert = []
    
    print(f"Generating local embeddings for {len(chunks)} chunks...")
    for i, chunk in enumerate(chunks):
        try:
            vector = get_embedding(chunk)
            doc = {
                "chunk_id": f"chunk_{i}",
                "text": chunk,
                "embedding": vector
            }
            documents_to_insert.append(doc)
        except Exception as e:
            print(f"Failed to embed chunk {i}: {e}")

    if documents_to_insert:
        collection.delete_many({})
        collection.insert_many(documents_to_insert)
        print(f"\nSuccessfully uploaded {len(documents_to_insert)} chunks to MongoDB Atlas locally!")
    else:
        print("No documents found to upload.")

if __name__ == "__main__":
    sample_pdf = "data/sample.pdf"
    if os.path.exists(sample_pdf):
        upload_documents_to_atlas(sample_pdf)
    else:
        print(f"Put a sample PDF into '{sample_pdf}' to test the pipeline.")