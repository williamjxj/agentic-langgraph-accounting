# Agentic LangGraph Accounting

[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://williamjxj.github.io/agentic-langgraph-accounting/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🤖 AI-powered accounting auditor built with DeepSeek LLM, LangGraph StateGraph, and Retrieval-Augmented Generation (RAG)

## 📖 Full Documentation

**[Visit the complete documentation site →](https://williamjxj.github.io/agentic-langgraph-accounting/)**

The documentation includes:
- 📊 **[Query Guide & FAQ](https://williamjxj.github.io/agentic-langgraph-accounting/qa.html)** - 50+ example queries
- 🏗️ **[Technical Architecture](https://williamjxj.github.io/agentic-langgraph-accounting/estimation.html)** - Design decisions and roadmap
- 💾 **[Data Management](https://williamjxj.github.io/agentic-langgraph-accounting/data-management.html)** - Triple data architecture guide
- 🔄 **[Development Phases](https://williamjxj.github.io/agentic-langgraph-accounting/improvement-1.html)** - Evolution and improvements

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/williamjxj/agentic-langgraph-accounting.git
cd agentic-langgraph-accounting

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your DEEPSEEK_API_KEY

# Run the application
python run_server.py
```

Visit `http://localhost:8501` for the Streamlit UI.

## ✨ Key Features

- **🧠 Intelligent Query Routing**: LangGraph StateGraph automatically routes queries to SQL, RAG, or hybrid search
- **📊 Rich Dataset**: 250 invoices across 50 vendors, 12 categories, and 11 departments
- **🔍 Semantic Search**: Sentence Transformers with 384-dimensional embeddings
- **📄 Document Analysis**: 20+ audit reports with full-text search
- **🎯 Production-Ready**: Zero hardcoded paths, cross-platform compatible

## 🏗️ Architecture

```
route_query → [query_sql | query_rag | query_both] → generate_answer
```

**Triple Data Architecture:**
- **SQLite Database**: Structured invoice data with 16-field schema
- **ChromaDB Vector Store**: Semantic embeddings for intelligent search
- **File Storage**: PDF invoices and audit reports

## 🛠️ Technology Stack

- **LLM**: DeepSeek via OpenAI-compatible API
- **Framework**: LangGraph StateGraph
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Database**: SQLite + ChromaDB

## 📊 Example Queries

```
"Show me all unpaid invoices"
"What are the top 5 vendors by total spending?"
"Summarize the Q4 2023 audit report"
"Find invoices from Acme Corp over $10,000"
```

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**[📖 Read the full documentation](https://williamjxj.github.io/agentic-langgraph-accounting/)** to learn more about this project.
