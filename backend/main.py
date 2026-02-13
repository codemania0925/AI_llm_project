"""FastAPI backend - User → API → Embeddings → Vector DB → LLM → Response."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from embeddings_service import get_embeddings
from vector_db import add_documents, query_similar
from llm_service import generate_response

app = FastAPI(title="RAG Sample API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


class IndexRequest(BaseModel):
    documents: list[dict[str, str]]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/index")
def index_documents(req: IndexRequest):
    """Index documents into vector DB for retrieval."""
    try:
        docs = [f"{d.get('title', '')}\n{d.get('content', '')}" for d in req.documents]
        metas = [{"title": d.get("title", "")} for d in req.documents]
        add_documents(docs, metas)
        return {"indexed": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
def query(req: QueryRequest):
    """Query: embed question → vector search → LLM with context → response."""
    try:
        question = req.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Empty question")

        # 1. Get embeddings for question
        query_vector = get_embeddings([question])[0]

        # 2. Vector DB retrieval
        results = query_similar(query_vector, top_k=3)
        context = "\n\n".join(r["text"] for r in results) if results else "No relevant context."

        # 3. LLM generates response
        answer = generate_response(question, context)

        return {
            "question": question,
            "answer": answer,
            "sources": [r.get("metadata", {}) for r in results],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
