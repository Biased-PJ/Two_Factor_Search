import os
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer, CrossEncoder
from dotenv import load_dotenv

# Load configurations
load_dotenv()

# Initialize MongoDB client
mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["faq_db"]
collection = db["embedded_chunks"]

# Load local models
print("Loading local embedding model (Stage 1)...")
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("Loading local Cross-Encoder model (Stage 2)...")
reranker = CrossEncoder("mixedbread-ai/mxbai-rerank-xsmall-v1")


def get_embedding(text):
    """Generates a local vector embedding for the search query."""
    return embedding_model.encode(text).tolist()


def stage_1_vector_search(query, limit=20):
    """Queries MongoDB Atlas Vector Search using our local 384-dim vector."""
    query_vector = get_embedding(query)
    
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": limit * 5,
                "limit": limit
            }
        },
        {
            "$project": {
                "_id": 0,
                "text": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]
    
    results = list(collection.aggregate(pipeline))
    return [doc["text"] for doc in results]


def stage_2_rerank(query, candidate_chunks, top_k=3):
    """Deep attention cross-encoding filter."""
    if not candidate_chunks:
        return []
        
    pairs = [[query, chunk] for chunk in candidate_chunks]
    scores = reranker.predict(pairs)
    scored_chunks = sorted(zip(scores, candidate_chunks), key=lambda x: x[0], reverse=True)
    return [chunk for score, chunk in scored_chunks[:top_k]]


def smart_search(query):
    """Executes the complete local-to-local Two-Stage search pipeline."""
    print(f"\n[User Query]: {query}")
    
    candidates = stage_1_vector_search(query, limit=20)
    print(f"-> Stage 1: Retreived {len(candidates)} candidates from MongoDB Atlas.")
    
    if not candidates:
        return []
        
    final_chunks = stage_2_rerank(query, candidates, top_k=3)
    print(f"-> Stage 2: Reranked and narrowed down to the top {len(final_chunks)} chunks.")
    
    return final_chunks


if __name__ == "__main__":
    # Test query relative to whatever your sample PDF contains
    test_query = "What is the primary topic or policy discussed?"
    results = smart_search(test_query)
    
    print("\n--- Top Reranked Context Results ---")
    for i, res in enumerate(results):
        print(f"\n[Rank {i+1}]:\n{res}\n")