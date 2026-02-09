#!/usr/bin/env python3
"""
Launcher for the Accounting AI Auditor API. Run from the project root so that
the accounting_rag_app package is on PYTHONPATH without needing to cd to the parent.
"""
import sys
from pathlib import Path

# Add parent directory so "accounting_rag_app" package resolves
_project_root = Path(__file__).resolve().parent
_parent = _project_root.parent
if str(_parent) not in sys.path:
    sys.path.insert(0, str(_parent))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "accounting_rag_app.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
