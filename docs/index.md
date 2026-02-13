# Agentic LangGraph Accounting - Documentation

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/🦜_LangChain-Framework-green)](https://python.langchain.com/)
[![LangGraph](https://img.shields.io/badge/🕸️_LangGraph-StateGraph-orange)](https://langchain-ai.github.io/langgraph/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-teal)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to the documentation for **Agentic LangGraph Accounting** - an AI-powered accounting auditor built with DeepSeek LLM, LangGraph StateGraph, and Retrieval-Augmented Generation (RAG).

## 🚀 Quick Start

This project demonstrates a production-ready agentic AI system that intelligently routes queries between SQL database, RAG vector search, or hybrid approaches using LangGraph's StateGraph architecture.

**Repository:** [github.com/williamjxj/agentic-langgraph-accounting](https://github.com/williamjxj/agentic-langgraph-accounting)

---

## 🎯 Quick Start Tips

**New to the application?** Start here:

1. **📖 Read the [Query Guide & FAQ](qa.md)** - Learn what questions you can ask with 50+ examples
2. **🔍 Understand Route Visibility** - Every response shows which path was taken (SQL, RAG, or Hybrid)
3. **💡 Try the Example Queries** - Copy-paste ready queries to explore the dataset
4. **🐛 Check Troubleshooting** - Common issues and solutions

**Key Features to Explore:**
- Ask about **250 invoices** across 50 vendors, 12 categories, 11 departments
- Query **20+ audit reports** (quarterly, vendor analysis, compliance)
- Watch the **route visualization** show exactly how your query was processed
- Test **hybrid search** by mixing SQL and RAG keywords

---

## 📚 Documentation Index

### Quick Start & Usage
- **[Query Guide & FAQ](qa.md)** - 📊 **Comprehensive guide with 50+ example queries, tips, and troubleshooting** (NEW!)

### Project Overview & Analysis
- **[Technical Estimation](estimation.md)** - Comprehensive project analysis, architecture decisions, and implementation roadmap
- **[技术评估 (中文版)](estimation-zh.md)** - Chinese translation of the technical estimation document

### Development Phases & Improvements
- **[Phase 1: Real Embeddings & LangGraph](improvement-1.md)** - Migration from fake embeddings to Sentence Transformers, implementation of true StateGraph routing
- **[Phase 2: Rich Dataset & HuggingFace Integration](improvement-2.md)** - 250 invoices, 50 vendors, 20+ audit reports, real-world dataset integration
- **[Phase 3: Cross-Platform Compatibility](improvement-3.md)** - Zero hardcoded paths, dynamic package detection, production-ready deployment

### Architecture & Implementation
- **[Data Management Guide](data-management.md)** - Complete overview of the three data storage systems (SQLite, ChromaDB, file-based)
- **[Cross-Platform Validation Report](cross-platform-validation.md)** - Validation results, testing matrix, and compatibility guarantees

## 🏗️ Architecture Overview

### Core Components

**1. LangGraph StateGraph (5-Node Routing)**
```
route_query → [query_sql | query_rag | query_both] → generate_answer
```
- Intelligent query classification
- Conditional routing logic
- Hybrid search capability

**2. Triple Data Architecture**
- **SQLite Database**: 250 invoices with 16-field schema
- **ChromaDB Vector Store**: 384-dimensional semantic embeddings
- **File Storage**: 250 PDF invoices + 20+ audit reports

**3. Technology Stack**
- **LLM**: DeepSeek via OpenAI-compatible API
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Backend**: FastAPI with async operations
- **Frontend**: Streamlit interactive UI
- **Data Source**: HuggingFace datasets integration

## 🎯 Key Features

### ✅ Production-Ready
- Zero hardcoded paths - fully cross-platform
- Dynamic package detection
- Comprehensive error handling
- Clean startup with zero warnings

### ✅ Rich Dataset
- 250 invoices across 5 years (2020-2024)
- 50 vendors, 12 categories, 11 departments
- Realistic amounts ($100 - $50,000)
- Multiple payment statuses and terms

### ✅ Advanced AI Capabilities
- Semantic search with Sentence Transformers
- Hybrid retrieval (ChromaDB + BM25)
- Intelligent query routing
- Context-aware answer generation

### ✅ Comprehensive Reporting
- Quarterly audit reports
- Vendor analysis reports
- Compliance summaries
- Dynamic PDF generation

## 📖 Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/williamjxj/agentic-langgraph-accounting.git
cd agentic-langgraph-accounting

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export OPENAI_API_KEY="your-deepseek-api-key"
export OPENAI_BASE_URL="https://api.deepseek.com"
```

### Running the Application

```bash
# Start the backend server
python run_server.py

# In another terminal, start the frontend
streamlit run frontend/app.py --server.port 8501
```

### Generating Mock Data

```bash
# Generate 250 invoices with rich metadata
python -m accounting_rag_app.utils.generate_mock_data

# Load HuggingFace dataset samples
python -m accounting_rag_app.utils.load_hf_datasets
```

## 🔍 Development Phases

### Phase 1: Foundation (Real Embeddings & StateGraph)
**What Changed:**
- Migrated from `FakeEmbeddings` to `HuggingFaceEmbeddings`
- Implemented true LangGraph StateGraph with conditional routing
- Added SQL query tool integration
- Extended database schema from 6 to 16 fields

**Impact:** Enabled semantic search and intelligent query routing

[Read detailed changelog →](improvement-1.md)

### Phase 2: Rich Dataset & Integration
**What Changed:**
- Generated 250 realistic invoices (was 5)
- Created 50 vendors with varied metadata
- Generated 20+ audit reports
- Integrated HuggingFace datasets library

**Impact:** Realistic testing environment with production-scale data

[Read detailed changelog →](improvement-2.md)

### Phase 3: Cross-Platform & Production
**What Changed:**
- Eliminated all hardcoded paths
- Implemented dynamic package detection
- Fixed ChromaDB dimension mismatch
- Resolved LangChain deprecation warnings
- Created comprehensive documentation

**Impact:** True cross-platform compatibility, production deployment ready

[Read detailed changelog →](improvement-3.md)

## 🛠️ Technical Details

### Data Storage Systems

| System | Purpose | Technology | Location |
|--------|---------|------------|----------|
| Relational DB | Structured invoice data | SQLite + SQLAlchemy | `accounting.db` |
| Vector Store | Semantic embeddings | ChromaDB (384-dim) | `chroma_db/` |
| File Storage | PDFs and reports | Filesystem | `data/invoices/`, `data/reports/` |

[Learn more about data architecture →](data-management.md)

### LangGraph Routing Logic

The StateGraph intelligently routes queries:

- **SQL Node**: Structured queries (dates, amounts, statuses)
- **RAG Node**: Semantic queries (descriptions, patterns)
- **Both Node**: Complex queries requiring both approaches

[See complete implementation →](improvement-1.md#langgraph-stategraph-implementation)

## 📊 Project Statistics

- **Total Files**: 28 modified/created
- **Lines of Code Added**: 4,150+
- **Documentation Pages**: 7 comprehensive guides
- **Test Invoices**: 250 realistic records
- **Audit Reports**: 20+ generated reports
- **Zero**: Hardcoded paths or folder names

## 🔗 External Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Guide](https://langchain-ai.github.io/langgraph/)
- [DeepSeek API](https://platform.deepseek.com/)
- [HuggingFace Datasets](https://huggingface.co/datasets)
- [Sentence Transformers](https://www.sbert.net/)

## 🤝 Contributing

This project follows modern Python best practices:
- Type hints throughout
- Async/await patterns
- Cross-platform compatibility
- Comprehensive documentation

## 📝 License

This project is licensed under the MIT License - see the repository for details.

## 🔧 Troubleshooting

### Common Issues

**ChromaDB Dimension Mismatch**
- Delete `chroma_db/` and regenerate
- Ensure langchain-huggingface is installed
- Verify embeddings use all-MiniLM-L6-v2 (384-dim)

**Server Won't Start**
- Check Python 3.12+ is installed
- Verify all dependencies: `pip install -r requirements.txt`
- Set OPENAI_API_KEY and OPENAI_BASE_URL

**Cross-Platform Path Issues**
- Project uses pathlib.Path throughout
- No hardcoded paths exist (validated)
- Works on macOS, Windows, Linux

[See complete validation report →](cross-platform-validation.md)

---

**Last Updated**: February 2026  
**Documentation Version**: 1.0  
**Project Status**: Production-Ready ✅
