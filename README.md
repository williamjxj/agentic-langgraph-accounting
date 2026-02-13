# 📑 Accounting AI Auditor (Agentic RAG)

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-latest-green)
![LangGraph](https://img.shields.io/badge/LangGraph-agentic-purple)
![FastAPI](https://img.shields.io/badge/FastAPI-modern-teal)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A cutting-edge AI application for automated accounting audits and invoice processing. Built with the latest tech stack for AI agents **with true agentic workflows and intelligent routing**.

## 🚀 Tech Stack
- **Orchestration**: [LangGraph](https://github.com/langchain-ai/langgraph) with `StateGraph` for real agentic workflows
- **Framework**: [LangChain](https://github.com/langchain-ai/langchain) for RAG and tool integration
- **Embeddings**: [Sentence Transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`) for semantic search
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) with `asyncio` for high-performance API
- **Database**: [SQLAlchemy](https://www.sqlalchemy.org/) (Async) with SQLite for structured invoice data
- **Vector Store**: [ChromaDB](https://www.trychroma.com/) for document retrieval
- **LLM**: [DeepSeek](https://www.deepseek.com/) via OpenAI-compatible API
- **Frontend**: [Streamlit](https://streamlit.io/) for a professional demo UI
- **ETL & OCR**: `PyPDF`, `Pytesseract`, and `pdf2image` for document parsing
- **Hybrid Retrieval**: Combines Semantic Search (embeddings) with Keyword Search (BM25)

## ✨ Key Features

### 1. **Rich Production Dataset** 📊
- **250 diverse invoices** across 2022-2026 (vs 5 in original demo)
- **50 unique vendors** from various industries
- **12 categories** (IT, Legal, Marketing, HR, Finance, etc.)
- **11 departments** for organizational tracking
- **7 approval statuses** (Pending, Approved, Paid, Overdue, Rejected, etc.)
- **Rich metadata**: payment terms, PO numbers, tax tracking, due dates
- **20+ comprehensive audit reports** (quarterly, vendor analysis, compliance)

### 2. **HuggingFace Dataset Integration** 🤗
- Load real-world invoice datasets from HuggingFace Hub
- Support for 2,000+ invoice datasets
- Optional integration (works without HF library)
- Recommended datasets:
  - `mychen76/invoices-and-receipts_ocr_v1` (2,238 invoices)
  - `katanaml-org/invoices-donut-data-v1` (500 invoices)
  - `sujet-ai/Sujet-Finance-Vision-10k` (9,800 documents)

### 3. **True Agentic Workflow** 🧠
The AI agent intelligently routes queries to the appropriate data source:
- **SQL Queries**: For structured invoice data (amounts, vendors, counts, status, categories, departments)
- **RAG Queries**: For unstructured documents (audit reports, compliance docs)
- **Combined Queries**: Seamlessly merges both sources for comprehensive answers

**LangGraph Workflow:**
```
User Query → Router → [SQL | RAG | Both] → Answer Generation
```

### 4. **Intelligent Query Routing** 🎯
- Analyzes keywords and intent
- Routes to SQL database for transactional queries
- Routes to document store for analytical queries
- Combines both when needed

### 5. **Cross-Platform Compatibility** 🌍
- **Zero hardcoded paths** - works on Windows, macOS, Linux
- **Dynamic package detection** - folder can be renamed freely
- **Platform-independent file handling** - uses `pathlib.Path` throughout
- **Portable deployment** - works from any directory structure

### 6. **Real Semantic Search** 🔍
- Uses `sentence-transformers/all-MiniLM-L6-v2` (not fake embeddings!)
- 384-dimensional embeddings for meaningful similarity
- Hybrid retrieval: Vector (semantic) + BM25 (keyword)
- Free and runs locally

### 7. **Multi-Source Intelligence** 📊
- **SQL Tool**: Queries invoice database for structured data
  - Total amounts by vendor/category/department
  - Invoice counts and status
  - Pending/paid/overdue filtering
  - Payment term analysis
- **RAG Tool**: Searches through 20+ audit reports
  - Quarterly revenue analysis
  - Vendor performance reviews
  - Compliance information
  - Historical trends

### 8. **Automated ETL Pipeline** 🔄
- Automatically parses PDFs (with OCR fallback for scanned docs)
- Processes Markdown documents
- Real-time indexing on file upload
- Background processing for non-blocking UX

### 9. **Production-Ready Architecture** 🏗️
- Async FastAPI for high concurrency
- Proper state management with TypedDict
- Graceful fallbacks (works without API key in demo mode)
- Clean separation of concerns

## 🛠️ Features

1. **Agentic Audit**: An AI agent that intelligently chooses between querying a SQL database or searching through audit reports to answer complex questions.
2. **Rich Dataset**: 250+ invoices with comprehensive metadata (categories, departments, payment terms, taxes) across 5 years (2022-2026).
3. **Hybrid RAG**: High-accuracy retrieval combining vector embeddings (Sentence Transformers) and BM25.
4. **Automated ETL**: Automatically parses PDFs (with OCR fallback) and Markdown files.
5. **Tool Calling**: The agent uses specific tools to fetch data, ensuring grounded and accurate responses.
6. **Real-time Processing**: Upload a new invoice via the UI, and it's instantly indexed for retrieval.
7. **Intelligent Routing**: Queries are automatically routed to SQL, RAG, or both based on intent.
8. **Comprehensive Reports**: 20+ audit reports (quarterly, vendor analysis, compliance) generated from real data.
9. **HuggingFace Integration**: Load real-world invoice datasets (2,000+ invoices) for testing and training.
10. **Cross-Platform**: Zero hardcoded paths, works on Windows/macOS/Linux, folder can be renamed freely.

## 📊 Dataset Overview

### Mock Data (Included)
- **250 invoices** across 50 vendors
- **Time range**: 2022-2026 (5 years of history)
- **16 metadata fields**: vendor, amount, date, status, due_date, payment_terms, po_number, category, department, subtotal, tax_rate, tax_amount, approval_status, notes, etc.
- **12 categories**: IT, Legal, Marketing, Operations, HR, Finance, Facilities, Consulting, R&D, Compliance, Travel, Supplies
- **11 departments**: Engineering, Sales, Finance, Marketing, HR, Operations, Legal, IT, Executive, Customer Service, R&D
- **7 statuses**: Pending, Approved, Rejected, Paid, Overdue, On Hold, Cancelled
- **20+ reports**: Quarterly audits, vendor analysis, compliance reports

### Generate Mock Data
```bash
cd accounting_rag_app
python utils/generate_mock_data.py
```

This creates:
- 250 PDF invoices in `data/invoices/`
- Comprehensive CSV in `data/invoice_summary.csv`
- 20+ audit reports in `data/reports/`

### HuggingFace Datasets (Optional)

For additional real-world data:

```bash
# Install optional dependencies (already in requirements.txt)
pip install datasets transformers pillow

# Run demo to load sample data (downloads 10 sample invoices)
python utils/load_hf_datasets.py
```

**Demo output**: Creates `data/hf_sample_invoices.csv` with 10 real invoices from HuggingFace

**Available datasets:**
- `mychen76/invoices-and-receipts_ocr_v1` - 2,238 invoices with OCR
- `katanaml-org/invoices-donut-data-v1` - 500 structured invoices
- `sujet-ai/Sujet-Finance-Vision-10k` - 9,800 financial documents

See [docs/improvement-2.md](docs/improvement-2.md) for detailed dataset information.

## 🏃 How to Run

### 1. Set Environment Variables
Ensure you have your DeepSeek API key set (e.g. in `.env` or export):
```bash
export DEEPSEEK_API_KEY='your-api-key'
```
**Note:** The app works in demo mode without an API key (pre-scripted responses).

### 2. Install Dependencies (from project root)
```bash
cd accounting_rag_app
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**First run note:** The sentence-transformers model (~80MB) will download automatically.

### 3. Start the Backend
From inside the project directory (`accounting_rag_app`):
```bash
python run_server.py
```
Or from the **parent** of `accounting_rag_app`:
```bash
python -m uvicorn accounting_rag_app.backend.main:app --host 0.0.0.0 --port 8000
```

The backend will:
- Initialize the database
- Run ETL on existing documents
- Build the agentic workflow graph
- Start the API server on port 8000

### 4. Start the Frontend (New Terminal)
From inside the project directory:
```bash
streamlit run frontend/app.py
```

Access the UI at `http://localhost:8501`

## 💬 Example Queries

**📚 For a comprehensive query guide with 50+ examples, tips, and best practices, see [docs/qa.md](docs/qa.md)**

### SQL-Routed Queries (Structured Data)
```
"What's the total amount by vendor?"
"How many pending invoices do we have?"
"Show me all invoices from Legal Associates"
"What's our IT spending this year?"
"Which invoices are overdue?"
"Show me department breakdown for Engineering"
"What's the total by category?"
```

### RAG-Routed Queries (Documents & Reports)
```
"What does the 2024 audit report say about growth?"
"What were the Q4 revenues?"
"Is the company GAAP compliant?"
"What does  the vendor analysis report say?"
"Show me compliance findings"
```

### Combined Queries (SQL + RAG)
```
"Which vendor has the highest invoices and what does the audit say about them?"
"Show me invoice totals and the audit report's compliance findings"
"What are our top IT vendors and what does the quarterly report say about tech spending?"
```

### Enhanced Queries (New Capabilities)
```
# Category-based
"Show me all Marketing expenses"
"What's our total Legal spending?"

# Department-based
"How much did Engineering spend in Q3?"
"Show Sales department invoices"

# Status/Due Date tracking
"Which invoices are overdue and when were they due?"
"Show me paid invoices from last month"

# Payment Terms
"Which vendors have Net 30 terms?"
"Show invoices with payment terms Net 60 or longer"
```

### Combined Queries
```
"Which vendor has the highest invoices and what does the audit say about them?"
"Show me invoice totals and the audit report's compliance findings"
```

## 📂 Project Structure
```
accounting_rag_app/
├── agents/           # LangGraph agent with StateGraph
│   └── audit_agent.py   # Router, SQL tool, RAG tool, answer generation
├── backend/          # FastAPI application and endpoints
│   └── main.py          # API server, startup ETL
├── frontend/         # Streamlit UI
│   └── app.py           # Chat interface, file upload
├── services/         # ETL and RAG logic
│   ├── etl_service.py   # PDF/MD parsing, OCR
│   └── rag_service.py   # Hybrid retrieval (Sentence Transformers + BM25)
├── models/           # SQLAlchemy and Pydantic schemas
│   └── database.py      # Invoice model (16 fields), async session
├── data/             # Mock invoices and reports (250+ items)
│   ├── invoices/        # 250 PDF invoices (was 5)
│   ├── reports/         # 20+ audit reports (was 1)
│   ├── invoice_summary.csv  # 250 rows, 16 columns
│   └── uploads/         # User-uploaded documents
├── utils/            # Data generation and loading scripts
│   ├── generate_mock_data.py   # Generate 250 invoices with rich metadata
│   ├── generate_reports.py     # Auto-generate audit reports  
│   └── load_hf_datasets.py     # HuggingFace dataset integration
├── docs/             # Documentation
│   ├── estimation.md        # Technical analysis
│   ├── estimation-zh.md     # Chinese version
│   ├── improvement-1.md     # Phase 1: Real embeddings + LangGraph
│   ├── improvement-2.md     # Phase 2: Rich dataset + HF integration
│   └── data-management.md   # Data storage & path guide
├── chroma_db/        # ChromaDB vector store (384-dim embeddings)
├── accounting.db     # SQLite database (16-field invoice schema)
├── run_server.py     # Server launcher
└── requirements.txt  # Dependencies
```

## 🎯 How It Works

### Agentic Workflow (LangGraph)

1. **User submits query** via Streamlit or API
2. **Router node** analyzes the query:
   - Scores SQL keywords (invoice, vendor, total, sum, etc.)
   - Scores RAG keywords (report, audit, growth, compliance, etc.)
   - Decides routing: SQL, RAG, or Both
3. **Query execution**:
   - **SQL Node**: Queries database with intelligent query generation
   - **RAG Node**: Hybrid retrieval (vector + BM25) from documents
   - **Both Node**: Executes both and combines context
4. **Answer generation**:
   - LLM receives context from SQL and/or RAG
   - Synthesizes coherent, grounded answer
   - Returns response to user

### State Management
```python
class AgentState(TypedDict):
    messages: List[BaseMessage]  # Conversation history
    context: str                 # RAG context
    sql_results: str            # SQL query results
    next_action: str            # Router decision
```

## 🔧 Configuration

### Embedding Model
Default: `sentence-transformers/all-MiniLM-L6-v2`
- Free and open-source
- 384 dimensions
- ~80MB model size
- Runs on CPU (or GPU if available)

To change, edit `services/rag_service.py`:
```python
self.embeddings = HuggingFaceEmbeddings(
    model_name="your-model-name",
    model_kwargs={'device': 'cpu'},  # or 'cuda'
    encode_kwargs={'normalize_embeddings': True}
)
```

### LLM
Default: DeepSeek Chat via OpenAI-compatible API

Set in `.env`:
```bash
DEEPSEEK_API_KEY=your-key-here
```

## 📊 Performance

- **Embedding inference**: ~70ms per query (CPU)
- **Hybrid retrieval**: ~100-200ms for k=5 documents
- **LLM response**: 1-3 seconds (depends on DeepSeek API)
- **Total latency**: 1.5-4 seconds end-to-end

## 🆕 Recent Improvements

### Phase 3: Cross-Platform Compatibility & Path Management (Latest)

See [docs/improvement-3.md](docs/improvement-3.md) and [docs/cross-platform-validation.md](docs/cross-platform-validation.md) for detailed reports.

**Summary:**
- ✅ **Zero hardcoded paths** - removed all `"accounting_rag_app/"` references
- ✅ **Dynamic package detection** - `run_server.py` auto-detects folder name
- ✅ **Portable Path handling** - all scripts use `pathlib.Path` for cross-platform compatibility
- ✅ **Folder rename support** - works if project folder renamed (e.g., `my_accounting_app`)
- ✅ **Platform-independent** - tested on macOS, expected to work on Windows/Linux
- ✅ **Working directory agnostic** - paths resolved relative to script location
- ✅ **Fixed HF demo** - `load_hf_datasets.py` now actually loads sample data
- ✅ **Comprehensive validation** - grep search confirms zero hardcoded paths

### Phase 2: Rich Dataset & HuggingFace Integration

See [docs/improvement-2.md](docs/improvement-2.md) for detailed changelog.

**Summary:**
- ✅ **250 invoices** with rich metadata (was 5)
- ✅ **50 vendors** across 12 categories and 11 departments
- ✅ **5-year history** (2022-2026) with diverse statuses
- ✅ **20+ audit reports** (quarterly, vendor, compliance)
- ✅ **16 metadata fields** (payment terms, PO numbers, taxes, due dates)
- ✅ **HuggingFace integration** for loading real invoice datasets
- ✅ **Enhanced SQL queries** (category, department, overdue tracking)
- ✅ **Automated report generation** from invoice data

### Phase 1: Real Embeddings & Agentic Workflow

See [docs/improvement-1.md](docs/improvement-1.md) for detailed changelog.

**Summary:**
- ✅ Replaced `FakeEmbeddings` with real Sentence Transformers
- ✅ Implemented proper LangGraph `StateGraph` with routing
- ✅ Added SQL query tool for database access
- ✅ Intelligent query routing (SQL vs RAG vs Both)
- ✅ Enhanced state management
- ✅ True agentic behavior with multi-step reasoning

## 📚 Documentation

- **[docs/qa.md](docs/qa.md)** - 📊 **Comprehensive Query Guide & FAQ** (50+ example queries, tips, troubleshooting)
- [docs/cross-platform-validation.md](docs/cross-platform-validation.md) - **Cross-platform compatibility validation**
- [docs/data-management.md](docs/data-management.md) - Data storage architecture & path management
- [docs/improvement-3.md](docs/improvement-3.md) - Phase 3: Cross-platform compatibility & path management
- [docs/improvement-2.md](docs/improvement-2.md) - Phase 2: Rich dataset & HF integration
- [docs/improvement-1.md](docs/improvement-1.md) - Phase 1: Real embeddings & agentic workflow
- [docs/estimation.md](docs/estimation.md) - Technical analysis and architecture
- [docs/estimation-zh.md](docs/estimation-zh.md) - Chinese version of technical analysis

## 🚦 Next Steps (Phase 4 Roadmap)

1. **Fine-tune Embeddings**
   - Use 250+ invoices for domain-specific fine-tuning
   - Improve semantic search accuracy
   - Custom embedding model for accounting domain

2. **Advanced Analytics**
   - Anomaly detection (duplicate invoices, unusual amounts)
   - Spending trend analysis
   - Predictive overdue alerts

3. **Enhanced NL2SQL**
   - Natural language to SQL conversion
   - Complex join queries  
   - Date range filtering with natural language
   - Multi-turn dialogue support
   - Context window management

3. **Advanced RAG**
   - Metadata filtering
   - Reranking with cross-encoder
   - Multi-vector retrieval strategies

4. **Observability**
   - Structured logging
   - Performance metrics
   - LangGraph visualization

5. **Deployment**
   - Docker containerization
   - Environment configurations
   - CI/CD pipeline

## 🤝 Contributing

This is a demo application showcasing agentic RAG patterns. Feel free to:
- Add new agent nodes (e.g., web search, calculations)
- Improve routing logic
- Add more sophisticated SQL query generation
- Implement conversation memory
- Enhance the UI

## 📄 License

MIT License - See LICENSE file for details.

---

**Built with ❤️ using LangGraph, LangChain, and Sentence Transformers**
