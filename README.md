# 🔍 High-Precision Two-Stage Retrieval Engine with Local LLM Generation

> A production-ready semantic search system that combines **dense vector retrieval**, **cross-encoder reranking**, and **local LLM generation** to deliver highly accurate, context-aware answers with zero recurring inference costs.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-REST%20API-black)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas%20Vector%20Search-green)
![Ollama](https://img.shields.io/badge/Ollama-Llama%203.2-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## 📖 Overview

Traditional Retrieval-Augmented Generation (RAG) pipelines often struggle with semantic drift, irrelevant document retrieval, and excessive token consumption. A simple vector search can retrieve loosely related passages that dilute answer quality and waste LLM context space.

This project addresses those challenges through a **Two-Stage Retrieval Architecture** inspired by modern production search systems.

Instead of sending raw vector search results directly to the language model, retrieved documents undergo an additional **cross-encoder reranking phase** that evaluates the exact relationship between the user's query and each candidate document chunk.

The result is:

* Higher retrieval precision
* Reduced hallucinations
* Lower token consumption
* Faster generation
* Fully local answer synthesis
* Zero API inference costs

---

# ✨ Features

- 🔍 Dense Vector Retrieval using Sentence Transformers
- 🎯 Cross-Encoder Reranking for precision search
- 🦙 Local LLM inference using Llama 3.2
- ☁️ MongoDB Atlas Vector Search integration
- 📄 Automatic PDF ingestion and chunking
- ⚡ Low-latency semantic search API
- 🔒 Fully local answer generation
- 💰 Zero recurring inference costs
- 🚀 Production-ready REST API

# 🚀 System Architecture

## 🏗️ Architecture Diagram

```mermaid
flowchart LR

    A[User Query]
    --> B[all-MiniLM-L6-v2<br/>Bi-Encoder]

    B --> C[(MongoDB Atlas<br/>Vector Search)]

    C --> D[Top 20 Candidate Chunks]

    D --> E[mxbai-rerank-xsmall-v1<br/>Cross-Encoder Reranker]

    E --> F[Top 3 Ranked Chunks]

    F --> G[Llama 3.2<br/>via Ollama]

    G --> H[Generated Response]
```

The retrieval pipeline consists of three independent stages:

## Stage 1 — Dense Vector Retrieval

The incoming query is embedded using the lightweight Sentence Transformer model:

```text
all-MiniLM-L6-v2
```

The generated 384-dimensional embedding is used to query a MongoDB Atlas Vector Search index and retrieve the top candidate document chunks.

```text
User Query
      │
      ▼
Bi-Encoder Embedding
      │
      ▼
MongoDB Atlas Vector Search
      │
      ▼
Top 20 Candidate Chunks
```

### Why This Stage?

Dense retrieval provides:

* Semantic matching
* Fast approximate nearest-neighbor search
* Scalability to millions of documents

However, vector similarity alone cannot always determine true relevance.

---

## Stage 2 — Cross-Encoder Reranking

The retrieved candidates are passed through:

```text
mxbai-rerank-xsmall-v1
```

Unlike a bi-encoder, the cross-encoder jointly evaluates the question and document chunk, producing significantly more accurate relevance scores.

```text
Top 20 Candidates
        │
        ▼
Cross Encoder
(mxbai-rerank-xsmall-v1)
        │
        ▼
Top 3 Most Relevant Chunks
```

### Why This Stage?

This layer removes:

* Semantic noise
* Vocabulary mismatch errors
* Weak vector matches
* Irrelevant contextual fragments

Only the most relevant information survives.

---

## Stage 3 — Local LLM Synthesis

The highest-ranked document fragments are injected into a local:

```text
Llama 3.2
```

instance running through:

```text
Ollama
```

The model synthesizes the retrieved information into a concise, coherent, production-quality answer.

```text
Top 3 Chunks
      │
      ▼
Llama 3.2 via Ollama
      │
      ▼
Final Answer
```

### Benefits

✅ No external AI APIs

✅ Fully offline generation

✅ Lower latency

✅ Zero token costs

✅ Data privacy preserved

---

# 🏗️ Repository Structure

```text
Two_Factor_Search/
│
├── data/
│   └── sample.pdf
│
├── src/
│   ├── parser.py
│   ├── database.py
│   ├── search_engine.py
│   └── app.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

# 🎯 Design Objectives

This system was built to solve four common problems in traditional RAG pipelines:

- Reduce semantic drift during retrieval
- Minimize irrelevant context sent to the LLM
- Lower token consumption and inference costs
- Improve answer precision without using paid APIs

The two-stage retrieval architecture ensures that only the most relevant document fragments reach the generation layer.

### File Breakdown

| File               | Purpose                                      |
| ------------------ | -------------------------------------------- |
| `parser.py`        | Extracts text from PDFs and creates chunks   |
| `database.py`      | Generates embeddings and seeds MongoDB Atlas |
| `search_engine.py` | Handles vector retrieval and reranking       |
| `app.py`           | Flask API server and LLM orchestration       |
| `sample.pdf`       | Source knowledge base document               |

---

# ⚙️ Technology Stack

## Backend

* Python
* Flask

## Vector Database

* MongoDB Atlas Vector Search

## Retrieval Models

* Sentence Transformers
* all-MiniLM-L6-v2

## Reranking

* mxbai-rerank-xsmall-v1

## LLM Layer

* Ollama
* Llama 3.2

## Document Processing

* PyPDF

## ML Ecosystem

* Hugging Face
* SentenceTransformers

---

# 📦 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Biased-PJ/Two_Factor_Search.git

cd Two_Factor_Search
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Install Ollama

Download and install Ollama:

https://ollama.com

Pull the required model:

```bash
ollama pull llama3.2
```

Verify installation:

```bash
ollama run llama3.2
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
MONGO_URI="mongodb+srv://username:password@cluster.mongodb.net/?appName=Cluster0"
```

---

# 🚀 Running the Pipeline

## Step 1 — Index Your Documents

Place your source PDF inside:

```text
data/sample.pdf
```

Generate embeddings and upload vectors:

```bash
python src/database.py
```

---

## Step 2 — Launch the API Server

```bash
python src/app.py
```

The API will start locally on:

```text
http://127.0.0.1:5000
```

---

## Step 3 — Query the System

### PowerShell

```powershell
(Invoke-RestMethod `
-Uri "http://127.0.0.1:5000/api/ask" `
-Method Post `
-ContentType "application/json" `
-Body '{"question":"What benefits does an OCI get regarding visiting India?"}'
).answer
```

### cURL

```bash
curl -X POST http://127.0.0.1:5000/api/ask \
-H "Content-Type: application/json" \
-d '{"question":"What benefits does an OCI get regarding visiting India?"}'
```

---

# 🎯 Example Output

### Query

```text
What benefits does an OCI get regarding visiting India?
```

### Response

```text
An Overseas Citizen of India (OCI) receives significant travel and legal benefits when visiting India, including a lifelong multiple-entry visa and exemption from police registration requirements regardless of duration of stay. OCI cardholders are also granted parity with Non-Resident Indians across various economic, financial, and educational domains, although restrictions remain on the purchase of agricultural and plantation properties.
```

---

# 📈 Why This Architecture Works

| Traditional RAG         | This Project              |
| ----------------------- | ------------------------- |
| Vector search only      | Vector search + reranking |
| More irrelevant context | Highly filtered context   |
| Higher token usage      | Lower token usage         |
| More hallucinations     | Reduced hallucinations    |
| Often cloud-hosted      | Fully local generation    |
| Ongoing API costs       | Zero inference cost       |

---

# 🔮 Future Enhancements

* Multi-document ingestion
* Hybrid search (BM25 + Dense Retrieval)
* Streaming LLM responses
* Conversation memory
* Multi-user authentication
* Docker deployment
* Kubernetes scaling
* Evaluation metrics dashboard
* PDF upload interface
* React frontend

---

# 🤝 Contributing

Contributions, feature requests, and pull requests are welcome.

If you'd like to improve retrieval quality, optimize latency, or extend model support, feel free to open an issue or submit a PR.

---

# 📜 License

This project is licensed under the MIT License.

---

## ⭐ If you found this project useful, consider giving it a star on GitHub!

It helps others discover the project and supports future development.