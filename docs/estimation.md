# Tech Implementation: Estimation & Analysis

Research and analysis of the **Accounting AI Auditor** app’s technical implementation, with pros and cons by component and overall.

---

## 1. Architecture Overview

| Layer        | Technology              | Role |
|-------------|--------------------------|------|
| **API**     | FastAPI + Uvicorn        | REST backend, async request handling |
| **Orchestration** | LangGraph (minimal) | Agent state; no real graph topology |
| **RAG**     | LangChain + ChromaDB + BM25 | Document load, chunk, embed, hybrid retrieval |
| **LLM**     | DeepSeek (OpenAI-compatible API) | Answer generation with RAG context |
| **Vector DB** | ChromaDB (local)      | Persisted embeddings; in-memory BM25 |
| **Structured DB** | SQLAlchemy + SQLite (async) | Invoice table, CSV seed on startup |
| **ETL**     | PyPDF, pdf2image, pytesseract | PDF/MD load, OCR fallback, chunking |
| **Frontend**| Streamlit               | Chat UI, file upload, calls backend HTTP |

Data flow: **User query → FastAPI `/query` → AuditAgent retrieves RAG docs → DeepSeek LLM → response**. Uploads go to `/upload`, ETL runs in background, RAG store is updated.

---

## 2. Component Analysis

### 2.1 Backend (FastAPI)

| Aspect | Implementation |
|--------|----------------|
| App entry | `backend/main.py`; `.env` loaded from project root |
| Startup | `init_db()`, full ETL over `data/`, RAG init, CSV seed if DB empty, agent build |
| Endpoints | `POST /query` (agent), `POST /upload` (file + background ETL) |
| State | Global singletons: `etl_service`, `rag_service`, `audit_agent_graph` |

**Pros**

- Async endpoints and async agent/LLM calls fit I/O-bound workload.
- Paths derived from `_PROJECT_ROOT` work regardless of CWD.
- Background tasks for uploads avoid blocking the request.
- Pydantic models for request/response; type hints throughout.

**Cons**

- No dependency injection: services are globals, harder to test and swap (e.g. RAG/DB).
- Startup runs full ETL on every process start; no incremental or lazy load.
- No auth, rate limiting, or request validation beyond Pydantic.
- `thread_id` in `/query` is accepted but not used (no conversation or DB persistence).

---

### 2.2 RAG Service

| Aspect | Implementation |
|--------|----------------|
| Embeddings | `FakeEmbeddings(size=1536)` — deterministic, no API |
| Vector store | ChromaDB, `persist_directory="chroma_db"` |
| Keyword | BM25Okapi on in-memory list of docs |
| Retrieval | `hybrid_retrieve`: vector top-k + BM25 top-k, dedupe by content, return up to k |

**Pros**

- Hybrid retrieval (vector + BM25) improves robustness to exact terms and synonyms.
- ChromaDB persistence survives restarts.
- Simple, readable API: `initialize_vector_store`, `hybrid_retrieve`, `add_documents`.
- No embedding API cost or key in default setup (FakeEmbeddings).

**Cons**

- **FakeEmbeddings**: no real semantic similarity; vector search is effectively random for meaning.
- BM25 corpus held in memory and **rebuilt on every `add_documents`** — O(n) and no incremental index.
- Chroma `persist_directory` is relative to CWD; can differ by run context (see run_server).
- No metadata filtering (e.g. by source or date) or reranking.
- Fixed chunk size (1000) and overlap (100); no multi-vector or sentence-window strategy.

---

### 2.3 Audit Agent

| Aspect | Implementation |
|--------|----------------|
| Framework | LangChain messages; `ChatOpenAI` with DeepSeek base URL and API key |
| Graph | `build_graph()` returns `self`; no LangGraph nodes/edges, single step |
| Flow | Get last user message → RAG retrieve (k=5) → build system + user messages → LLM → append AIMessage |
| Fallback | If no `DEEPSEEK_API_KEY`: hardcoded mock answers by keyword |

**Pros**

- DeepSeek via OpenAI-compatible client: one client, configurable base URL and key.
- Graceful fallback when key is missing (demo mode).
- RAG context injected via system message; clear separation of context vs user query.
- Async `ainvoke` used correctly from FastAPI.

**Cons**

- **No real agentic behavior**: no tools, no SQL, no routing; single RAG + LLM call (not “agent that chooses between SQL vs documents” as in README).
- **SQL DB unused**: Invoice table and CSV seed are never queried by the agent.
- LangGraph is nominal only; no graph structure, cycles, or tool nodes.
- No conversation history: each request is stateless; `thread_id` ignored.
- No streaming; response returned only after full generation.

---

### 2.4 ETL Service

| Aspect | Implementation |
|--------|----------------|
| PDF | PyPDFLoader; if extracted text length &lt; 50, switch to OCR |
| OCR | pdf2image → pytesseract per page |
| Markdown | TextLoader + same splitter |
| Chunking | RecursiveCharacterTextSplitter (1000 chars, 100 overlap, standard separators) |
| Pipeline | `run_pipeline(data_dir)`: walk tree, dispatch by extension |

**Pros**

- OCR fallback for scanned/image PDFs.
- Async interface (`process_pdf`, `process_markdown`, `run_pipeline`).
- Single splitter config for all doc types; consistent chunk format for RAG.

**Cons**

- Document loaders (PyPDF, TextLoader) are **synchronous**; async methods still block on I/O.
- No retries, no size limits; large or malformed PDFs can slow or crash the process.
- OCR runs in process; CPU-heavy and can block the event loop.
- Only `.pdf` and `.md`; no Excel, HTML, or other office formats.
- Errors only logged (e.g. `print`); no structured logging or metrics.

---

### 2.5 Database (SQLite + SQLAlchemy)

| Aspect | Implementation |
|--------|----------------|
| Engine | `sqlite+aiosqlite:///./accounting.db` (relative path) |
| Model | `Invoice`: id, invoice_id, vendor, amount, date, status, created_at |
| Startup | Tables created; if invoice count is 0, seed from `data/invoice_summary.csv` |

**Pros**

- Async engine and session; fits FastAPI async style.
- Simple schema; Pydantic schema for API use.
- CSV seed gives repeatable demo data without manual DB setup.

**Cons**

- **Not used by the agent**: no tool or query path from agent to DB.
- Single file path `./accounting.db`; location depends on CWD (same as Chroma).
- No migrations (e.g. Alembic); schema changes are manual.
- SQLite only; scaling to Postgres would require config and possibly connection pooling.

---

### 2.6 Frontend (Streamlit)

| Aspect | Implementation |
|--------|----------------|
| UI | Chat messages in session state; sidebar file upload |
| Backend | `requests.post` to `http://localhost:8000` for `/query` and `/upload` |

**Pros**

- Fast to build; chat and upload in one file.
- Session state keeps conversation in memory for the session.
- File upload triggers backend processing and gives feedback.

**Cons**

- **Hardcoded `localhost:8000`**: fails when backend is elsewhere or in Docker.
- No env-based API URL or config.
- CSV paths assume CWD; breaks when running from other directories.
- No auth; anyone with access can query and upload.
- Synchronous `requests`; no streaming or progress for long answers.

---

### 2.7 Run / Packaging

| Aspect | Implementation |
|--------|----------------|
| Server | `run_server.py` adds parent dir to `sys.path`, runs uvicorn with module string |
| Paths | Backend uses `_PROJECT_ROOT`; RAG/DB still use relative `chroma_db` and `./accounting.db` |

**Pros**

- Run from project root without `cd` to parent; simpler for local dev.
- Single command: `python run_server.py`.

**Cons**

- Path manipulation in `run_server.py` is brittle; depends on repo layout.
- No `reload` in launcher; code changes require manual restart.
- requirements.txt has no version pins; builds can drift over time.

---

## 3. Summary: Pros vs Cons

### Overall strengths

- **Stack is modern and coherent**: FastAPI, async SQLAlchemy, LangChain, ChromaDB, DeepSeek.
- **Hybrid RAG design** (vector + BM25) is sound; implementation is clear.
- **DeepSeek integration** is minimal and key-based; fallback when key is missing.
- **ETL** supports PDF + OCR and markdown; good for internal docs and reports.
- **Project layout** (backend, agents, services, models, frontend) is clear and maintainable.

### Main gaps and risks

| Area | Issue | Impact |
|------|--------|--------|
| RAG | FakeEmbeddings | No real semantic search; retrieval quality is weak. |
| RAG | BM25 in memory, full reindex on add | Doesn’t scale; slow for large doc sets. |
| Agent | No tools, no SQL | README promises “query SQL or documents” but only RAG is used. |
| Agent | No conversation memory | No multi-turn or thread use. |
| Data | SQL DB unused | Structured invoice data never influences answers. |
| Ops | Paths (Chroma, DB) relative to CWD | Different behavior by run context. |
| Frontend | Hardcoded API URL | Not deployable without code change. |
| Ops | Full ETL on every startup | Slow and redundant for large data dirs. |
| Deploy | No version pins | Reproducibility and supply-chain risk. |

---

## 4. Recommendations (Prioritised)

1. **Replace FakeEmbeddings** with a real embedding model (e.g. DeepSeek embedding if available, or a small open-source model) so hybrid retrieval is meaningful.
2. **Wire the agent to the SQL DB** via a read-only tool (e.g. “query invoices by vendor/date”) and add a simple router or tool-calling step so the agent can choose between RAG and SQL.
3. **Make API URL configurable** in the frontend (env or config) and fix data paths to use a project root or config.
4. **Resolve RAG/DB paths** from `_PROJECT_ROOT` (or a single config) so Chroma and SQLite paths are consistent across runs.
5. **Add optional conversation persistence** using `thread_id` (e.g. in-memory or DB) so the agent can use recent history.
6. **Pin dependency versions** in `requirements.txt` (or use a lockfile) for reproducible builds.
7. **Defer full ETL** on startup: load from existing Chroma only, or run ETL in a separate job/script and keep API startup light.

This document reflects the implementation as of the current codebase and can be updated as the app evolves.
