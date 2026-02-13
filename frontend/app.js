const API_BASE = "http://localhost:8000";

const indexBtn = document.getElementById("indexBtn");
const indexStatus = document.getElementById("indexStatus");
const questionInput = document.getElementById("questionInput");
const queryBtn = document.getElementById("queryBtn");
const answerEl = document.getElementById("answer");

const sampleDocs = [
  { title: "Python", content: "Python is a high-level programming language known for readability and versatility. It's used for web dev, data science, ML, automation, and scripting." },
  { title: "Vector DB", content: "Vector databases store embeddings (numerical vectors) and support similarity search. Used for semantic search, RAG, and recommendation systems." },
  { title: "RAG", content: "Retrieval Augmented Generation (RAG) combines vector search with LLMs. You retrieve relevant docs, then pass them as context to the LLM for grounded answers." },
];

async function indexDocuments() {
  indexStatus.textContent = "";
  indexBtn.disabled = true;
  try {
    const res = await fetch(`${API_BASE}/index`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ documents: sampleDocs }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Index failed");
    indexStatus.textContent = `Indexed ${data.indexed} docs`;
    indexStatus.classList.add("success");
  } catch (e) {
    indexStatus.textContent = e.message || "Index failed";
    indexStatus.classList.add("error");
  } finally {
    indexBtn.disabled = false;
  }
}

async function query() {
  const q = questionInput.value.trim();
  if (!q) return;
  queryBtn.disabled = true;
  answerEl.textContent = "Loading...";
  answerEl.classList.remove("empty");
  try {
    const res = await fetch(`${API_BASE}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Query failed");
    answerEl.textContent = data.answer || "(no answer)";
  } catch (e) {
    answerEl.textContent = "Error: " + (e.message || "Request failed");
  } finally {
    queryBtn.disabled = false;
  }
}

indexBtn.addEventListener("click", indexDocuments);
queryBtn.addEventListener("click", query);
questionInput.addEventListener("keydown", (e) => e.key === "Enter" && query());
