# Data Management Guide

## Overview

This document explains how data is organized and managed in the Accounting RAG application.

## Data Storage Architecture

The application uses **3 distinct data storage systems**, each optimized for different purposes:

### 1. File Storage: `data/` Directory

**Purpose**: Raw files, generated reports, user uploads

**Location**: `agentic-langgraph-accounting/data/`

**Structure**:
```
data/
├── invoices/              # 250+ PDF invoice files
│   ├── INV-2022-001.pdf
│   ├── INV-2022-002.pdf
│   └── ...
├── reports/               # 20+ Markdown audit reports
│   ├── audit_report_2024_Q1.md
│   ├── vendor_analysis_report.md
│   ├── compliance_audit_report.md
│   └── ...
├── uploads/               # User-uploaded files (via frontend)
│   └── [user uploads go here]
├── hf_cache/              # HuggingFace dataset cache (optional)
│   └── [cached HF datasets]
└── invoice_summary.csv    # Master CSV (250 rows, 16 columns)
```

**Managed by**:
- `utils/generate_mock_data.py` - Creates invoices/ and CSV
- `utils/generate_reports.py` - Creates reports/
- `backend/main.py` - Reads for ETL processing
- `frontend/app.py` - Uploads go to uploads/

### 2. Vector Store: `chroma_db/` Directory

**Purpose**: Semantic search with embeddings

**Location**: `agentic-langgraph-accounting/chroma_db/`

**Technology**: ChromaDB with persistence

**Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)

**Content**: 
- Document chunks from PDFs and Markdown files
- Vector embeddings for semantic retrieval
- Metadata (file paths, timestamps, document type)

**Size**: ~10-50MB (depends on number of documents)

**Managed by**:
- `services/rag_service.py` - Initialize and query
- `backend/main.py` - Rebuild on startup from data/

**Rebuild**: 
```bash
# Delete and rebuild from scratch
rm -rf chroma_db/
python run_server.py  # Auto-rebuilds from data/
```

### 3. Relational Database: `accounting.db` File

**Purpose**: Structured invoice queries (SQL)

**Location**: `agentic-langgraph-accounting/accounting.db`

**Technology**: SQLite with SQLAlchemy async

**Schema**: 16 fields per invoice
- Core: invoice_id, vendor, amount, date, status
- Extended: due_date, payment_terms, po_number, category, department
- Financial: subtotal, tax_rate, tax_amount
- Workflow: approval_status, notes, created_at

**Size**: ~100KB for 250 invoices

**Managed by**:
- `models/database.py` - Schema definition
- `backend/main.py` - Sync from CSV on startup
- `agents/audit_agent.py` - SQL queries

**Rebuild**:
```bash
# Delete and rebuild from CSV
rm accounting.db
python run_server.py  # Auto-rebuilds from CSV
```

## Data Flow

### Generation Flow

```
utils/generate_mock_data.py
  ↓
1. Generate 250 invoices → data/invoices/*.pdf
2. Save metadata → data/invoice_summary.csv
  ↓
utils/generate_reports.py (auto-called)
  ↓
3. Analyze CSV data
4. Generate 20+ reports → data/reports/*.md
```

### Startup Flow

```
python run_server.py
  ↓
backend/main.py startup()
  ↓
1. ETL: Read data/ folder (PDFs + Markdown)
2. Chunk documents
3. Initialize ChromaDB → chroma_db/
4. Load CSV → SQLite → accounting.db
  ↓
Ready to serve queries
```

### Query Flow

```
User Query → Router (LangGraph)
  ↓
├─ SQL Path → accounting.db (structured data)
├─ RAG Path → chroma_db/ (semantic search)
└─ Both → Combine results
  ↓
Answer Generation
```

## Path Management Strategy

All paths now use `pathlib.Path` for cross-platform compatibility:

### ✅ Correct Pattern (Used throughout app)

```python
from pathlib import Path

# Get project root
project_root = Path(__file__).resolve().parent.parent

# Build paths
data_dir = project_root / "data"
csv_path = project_root / "data" / "invoice_summary.csv"
invoices_dir = project_root / "data" / "invoices"

# Use with libraries
df = pd.read_csv(str(csv_path))  # Convert to string for compatibility
```

### ❌ Avoid This (Old approach - removed)

```python
# Hardcoded paths - breaks when running from different directories
csv_path = "data/invoice_summary.csv"  # ❌ Without proper root resolution
output_dir = "data/reports"             # ❌
```

## Working Directory Requirements

**All scripts should be run from the project root:**

```bash
cd /path/to/agentic-langgraph-accounting

# Generate data
python utils/generate_mock_data.py      ✅

# Start server
python run_server.py                    ✅

# Start frontend
streamlit run frontend/app.py           ✅
```

**Don't run from parent directory** (no longer supported):
```bash
cd /path/to/  # Parent of agentic-langgraph-accounting
python agentic-langgraph-accounting/utils/generate_mock_data.py  # ❌ Will fail
```

## Data Management Tasks

### Generate Fresh Dataset

```bash
cd agentic-langgraph-accounting
python utils/generate_mock_data.py
```

**Output**:
- 250 PDFs in `data/invoices/`
- CSV with 16 fields in `data/invoice_summary.csv`
- 20+ reports in `data/reports/`

### Clean and Rebuild Everything

```bash
cd agentic-langgraph-accounting

# Delete all generated data
rm -rf data/invoices/*
rm -rf data/reports/*
rm data/invoice_summary.csv
rm -rf chroma_db/
rm accounting.db

# Regenerate
python utils/generate_mock_data.py
python run_server.py  # Rebuilds databases
```

### Load HuggingFace Datasets (Optional)

```bash
cd agentic-langgraph-accounting
python utils/load_hf_datasets.py
```

**Downloads to**: `data/hf_cache/`

### Backup Data

```bash
# Backup everything
tar -czf backup_$(date +%Y%m%d).tar.gz data/ chroma_db/ accounting.db

# Backup just source data
tar -czf data_backup.tar.gz data/invoice_summary.csv data/invoices/ data/reports/
```

### Restore from CSV Only

If you have `data/invoice_summary.csv` but lost the databases:

```bash
# Delete corrupted databases
rm -rf chroma_db/ accounting.db

# Regenerate invoices from CSV (optional)
python utils/generate_mock_data.py  # Skip if you have PDFs

# Regenerate reports
python -c "from utils.generate_reports import generate_all_reports; generate_all_reports()"

# Rebuild databases
python run_server.py
```

## Data Isolation Strategy

### Development vs Production

**Development** (current setup):
- All data in project directory
- SQLite for simplicity
- ChromaDB local persistence

**Production** (future):
- Separate data volumes
- PostgreSQL database
- ChromaDB cloud/remote
- S3/Azure Blob for files

### Configuration for Different Environments

Create `.env` files:

```bash
# .env.development
DATA_DIR=./data
CHROMA_DIR=./chroma_db
DATABASE_URL=sqlite+aiosqlite:///./accounting.db

# .env.production
DATA_DIR=/var/app/data
CHROMA_DIR=/var/app/vector_store
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
```

## Performance Considerations

### File Storage (`data/`)

**Current**: 250 PDFs (~5MB each) = ~1.25GB
- ✅ Fast local access
- ✅ Simple backup
- ⚠️ Doesn't scale beyond 10K files

**Optimization**:
- Move PDFs to S3/Azure Blob for production
- Keep CSV/reports locally
- Use CDN for frequently accessed files

### Vector Store (`chroma_db/`)

**Current**: ~20MB for 250 documents
- ✅ Fast semantic search (<200ms)
- ✅ Persistent local storage
- ⚠️ Memory usage grows with collection size

**Optimization**:
- Use ChromaDB cloud for >100K documents
- Implement collection sharding by year/category
- Enable compression for embeddings

### Database (`accounting.db`)

**Current**: SQLite ~100KB for 250 invoices
- ✅ Zero-config, file-based
- ✅ Fast for <100K rows
- ⚠️ Limited concurrency

**Optimization**:
- PostgreSQL for >10K invoices or concurrent users
- Add indexes on vendor, date, category, status
- Partition by year for historical data

## Monitoring Data Health

### Check Data Integrity

```bash
cd agentic-langgraph-accounting

# Count files
echo "Invoices: $(ls -1 data/invoices/*.pdf 2>/dev/null | wc -l)"
echo "Reports: $(ls -1 data/reports/*.md 2>/dev/null | wc -l)"

# Check CSV
python -c "import pandas as pd; df=pd.read_csv('data/invoice_summary.csv'); print(f'CSV rows: {len(df)}'); print(f'Total: \${df[\"amount\"].sum():,.2f}')"

# Check SQLite
sqlite3 accounting.db "SELECT COUNT(*), SUM(amount) FROM invoices;"

# Check ChromaDB
python -c "from services.rag_service import RAGService; r=RAGService(); print(f'Chroma exists: {r.persist_directory}')"
```

### Validate Sync

All three storages should have consistent data:

```python
# Verify sync
import pandas as pd
from sqlalchemy import create_engine

# Load CSV
csv_df = pd.read_csv('data/invoice_summary.csv')

# Load SQLite
engine = create_engine('sqlite:///accounting.db')
db_df = pd.read_sql_query('SELECT * FROM invoices', engine)

# Compare
print(f"CSV count: {len(csv_df)}")
print(f"DB count: {len(db_df)}")
print(f"Match: {len(csv_df) == len(db_df)}")
```

## Summary

### Quick Reference

| Storage | Location | Type | Purpose | Rebuild Command |
|---------|----------|------|---------|-----------------|
| **Files** | `data/` | PDFs, CSV, Markdown | Raw data & reports | `python utils/generate_mock_data.py` |
| **Vectors** | `chroma_db/` | Embeddings | Semantic search | `rm -rf chroma_db/ && python run_server.py` |
| **SQL** | `accounting.db` | SQLite | Structured queries | `rm accounting.db && python run_server.py` |

### Data Size Expectations

- **250 invoices**: ~1.5GB total (1.25GB PDFs + 200MB databases)
- **2,500 invoices**: ~15GB total
- **25,000 invoices**: ~150GB (recommend cloud storage)

### Best Practices

✅ **Do**:
- Run scripts from project root
- Use `Path()` for all file operations
- Keep CSV as source of truth
- Regular backups of `data/` folder
- Delete `chroma_db/` when changing embeddings

❌ **Don't**:
- Hardcode paths without proper root resolution
- Manually edit `accounting.db` (sync from CSV)
- Mix ChromaDB collections with different dimensions
- Run scripts from parent directory

---

**Last updated**: Feb 2026  
**Maintainer**: AI Development Team
