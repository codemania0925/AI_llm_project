# RAG Sample Project

**User → Frontend → Backend API → Embeddings → Vector DB → LLM → Response → UI**

A minimal Retrieval Augmented Generation (RAG) demo: index documents, embed them, store in a vector DB, then answer questions using retrieved context and an LLM.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) with `llama3.2` (or another model)

## Setup

```bash
cd /home/md/work/Llm
pip install -r requirements.txt
```

Pull and run the LLM:

```bash
ollama run llama3.2
```

## Run

**1. Start the backend** (from project root):

```bash
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**2. Open the frontend**

Serve the `frontend` folder with any static server, or open `frontend/index.html` directly in a browser. For CORS to work when opening the file, you may need:

```bash
cd frontend && python -m http.server 3000
```

Then open http://localhost:3000

**3. Use the app**

1. Click **Index Sample Documents** to add sample docs to the vector DB.
2. Type a question (e.g. "What is Python used for?") and click **Query**.

## Project layout

```
backend/
  main.py              # FastAPI routes
  embeddings_service.py # sentence-transformers
  vector_db.py         # ChromaDB
  llm_service.py       # Ollama API
frontend/
  index.html
  app.js
  styles.css
```
