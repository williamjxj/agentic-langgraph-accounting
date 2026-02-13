#!/usr/bin/env python3
"""
Launcher for the Accounting AI Auditor API.
Automatically detects the package name for cross-platform compatibility.
"""
import sys
from pathlib import Path

# Get project info dynamically
_project_root = Path(__file__).resolve().parent
_package_name = _project_root.name  # Auto-detect package name
_parent = _project_root.parent

if str(_parent) not in sys.path:
    sys.path.insert(0, str(_parent))

if __name__ == "__main__":
    import uvicorn
    # Use dynamic package name instead of hardcoded folder name
    app_path = f"{_package_name}.backend.main:app"
    uvicorn.run(
        app_path,
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
