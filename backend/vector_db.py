"""Vector DB - ChromaDB for storing and retrieving document embeddings."""

import chromadb
from chromadb.config import Settings

from embeddings_service import get_embeddings

client = chromadb.Client(
    Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="./chroma_data",
        anonymized_telemetry=False,
    )
)
collection = client.get_or_create_collection(name="docs", metadata={"hnsw:space": "cosine"})


def add_documents(texts: list[str], metadatas: list[dict] | None = None):
    """Add documents to vector DB."""
    metadatas = metadatas or [{}] * len(texts)
    embeddings = get_embeddings(texts)
    ids = [f"doc_{i}" for i in range(len(texts))]
    collection.add(embeddings=embeddings, documents=texts, metadatas=metadatas, ids=ids)


def query_similar(query_vector: list[float], top_k: int = 5):
    """Query similar documents by embedding vector."""
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas"],
    )
    out = []
    docs = results["documents"][0] if results["documents"] else []
    metas = results["metadatas"][0] if results["metadatas"] else []
    for d, m in zip(docs, metas):
        out.append({"text": d, "metadata": m})
    return out
