# TheUltimateRAG User Manual

Welcome to **TheUltimateRAG**, a modular, agentic, and self-correcting RAG system. This manual will guide you through installation, configuration, and using its advanced features.

---

## 🚀 1. Installation

You can install the package directly or use it as a source project.

### Option A: From Source (Developers)

```bash
git clone https://github.com/Matrixxboy/TheUnltimateRAG.git
cd TheUnltimateRAG
pip install -e .
```

### Option B: As a Package

If distributed, you can install it via pip:

```bash
pip install theultimaterag
```

---

## ⚙️ 2. Configuration

The system uses a `.env` file for configuration. Copy `.env.example` to `.env`.

**LLM Provider** (`LLM_PROVIDER`):

- `openai`: Uses GPT-3.5/4 (Default)
- `ollama`: Uses local models (e.g., Llama 3)
- `anthropic`: Uses Claude models

**Embedding Provider** (`EMBEDDING_PROVIDER`):

- `openai`: Uses text-embedding-ada-002
- `ollama`: Uses local embeddings
- `huggingface`: Uses generic HuggingFace models

**Vector Store** (`VECTOR_DB_TYPE`):

- `postgres`: Production-grade (Requires PGVector)
- `chroma`: Simple local file-based (Default)

---

## 🏃 3. Running the System

### Method A: CLI (Recommended)

After installation, use the command line:

```bash
theultimaterag start
```

### Method B: Legacy / Dev

Run the wrapper script:

```bash
python app.py
```

Or use uvicorn directly:

```bash
uvicorn app:app --reload
```

---

## 📚 4. Features Guide

### A. Document Retrieval (RAG)

**Endpoint**: `POST /api/v1/chat`

Standard RAG chat. The system remembers your session context.
**Params**:

- `include_visualization`: Set `true` to get 3D vector coordinates data.
- `include_sources`: Set `true` to see which documents were used.

### B. Agentic Tools

**Endpoint Group**: `/api/v1/agent`

Designed for other AI agents to use this system as a tool.

- **GET /agent/tools**: Returns exact function definitions (JSON schema) that an OpenAI Agent can use to call this API.
- **POST /agent/search**: Perform a raw vector search (no chat) to get document chunks.
- **POST /agent/summarize**: Summarize any text.

### C. Advanced Self-Correcting Workflows

**Endpoint**: `POST /api/v1/agent/workflow`

For complex queries where standard search fails. This triggers a "reasoning loop":

1.  **Retrieve**: Fetches docs.
2.  **Grade**: Checks if docs are relevant.
3.  **Rewrite**: If irrelevant, the AI _rewrites your query_ and tries again.
4.  **Answer**: Generates the final answer.

**Usage**:

```json
{
  "query": "Explain quantum entanglement in simple terms",
  "workflow_type": "self-correcting"
}
```

---

## 🛠️ 5. Integration in Your Project

To use TheUltimateRAG as a library in your own Python code:

```python
from theultimaterag.core.container import rag_engine

# 1. Ingest a file
rag_engine.ingest_file("my_document.pdf", user_id="user123")

# 2. Query
response = rag_engine.query(
    session_id="session_1",
    query_text="What does the document say?",
    user_id="user123"
)

print(response["content"])
```
