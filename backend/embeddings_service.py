"""Embeddings service - converts text to vectors."""

from sentence_transformers import SentenceTransformer

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a list of texts."""
    model = _get_model()
    embeddings = model.encode(texts)
    return [e.tolist() for e in embeddings]
