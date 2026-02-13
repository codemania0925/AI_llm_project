"""LLM service - generates response from context."""

import httpx

LLM_BASE = "http://localhost:11434"  # Ollama default


def generate_response(question: str, context: str) -> str:
    """Generate LLM response using question and retrieved context."""
    prompt = f"""Use the following context to answer the question. If the context doesn't help, say so briefly.

Context:
{context}

Question: {question}

Answer:"""
    try:
        with httpx.Client(timeout=60.0) as c:
            r = c.post(
                f"{LLM_BASE}/api/generate",
                json={"model": "llama3.2", "prompt": prompt, "stream": False},
            )
            r.raise_for_status()
            return r.json().get("response", "No response generated.")
    except httpx.ConnectError:
        return (
            "LLM (Ollama) is not running. Start it with: ollama run llama3.2\n"
            "Or set OLLAMA_BASE_URL if using a different host."
        )
    except Exception as e:
        return f"LLM error: {e}"
