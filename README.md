# 📑 Accounting AI Auditor (Agentic RAG)

A cutting-edge AI application for automated accounting audits and invoice processing. Built with the latest tech stack for AI agents.

## 🚀 Tech Stack
- **Orchestration**: [LangGraph](https://github.com/langchain-ai/langgraph) for agentic workflows.
- **Framework**: [LangChain](https://github.com/langchain-ai/langchain) for RAG and tool integration.
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) with `asyncio` for high-performance API.
- **Database**: [SQLAlchemy](https://www.sqlalchemy.org/) (Async) with SQLite for structured invoice data.
- **Vector Store**: [ChromaDB](https://www.trychroma.com/) for document retrieval.
- **Frontend**: [Streamlit](https://streamlit.io/) for a professional demo UI.
- **ETL & OCR**: `PyPDF`, `Pytesseract`, and `pdf2image` for document parsing.
- **Hybrid Retrieval**: Combines Semantic Search (embeddings) with Keyword Search (BM25).

## 🛠️ Features
1. **Agentic Audit**: An AI agent that can choose between querying a SQL database or searching through audit reports to answer complex questions.
2. **Hybrid RAG**: High-accuracy retrieval combining vector embeddings and BM25.
3. **Automated ETL**: Automatically parses PDFs (with OCR fallback) and Markdown files.
4. **Tool Calling**: The agent uses specific tools to fetch data, ensuring grounded and accurate responses.
5. **Real-time Processing**: Upload a new invoice via the UI, and it's instantly indexed for retrieval.

## 🏃 How to Run

### 1. Set Environment Variables
Ensure you have your DeepSeek API key set (e.g. in `.env` or export):
```bash
export DEEPSEEK_API_KEY='your-api-key'
```

### 2. Install Dependencies (from project root)
```bash
cd accounting_rag_app
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Start the Backend
From inside the project directory (`accounting_rag_app`):
```bash
python run_server.py
```
Or from the **parent** of `accounting_rag_app`:
```bash
python -m uvicorn accounting_rag_app.backend.main:app --host 0.0.0.0 --port 8000
```

### 4. Start the Frontend (New Terminal)
From inside the project directory:
```bash
streamlit run frontend/app.py
```

## 📂 Project Structure
- `agents/`: LangGraph agent definitions and tools.
- `backend/`: FastAPI application and endpoints.
- `frontend/`: Streamlit UI.
- `services/`: ETL and RAG logic.
- `models/`: SQLAlchemy and Pydantic schemas.
- `data/`: Mock invoices and reports.
- `utils/`: Data generation scripts.
