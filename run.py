"""AI Compliance Shield - Entry Point.

Run the EU AI Act compliance audit tool server.
"""

import uvicorn
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from backend.main import app

if __name__ == "__main__":
    print("=" * 60)
    print("  AI Compliance Shield - EU AI Act Compliance Tool")
    print("=" * 60)
    print()
    print("  Starting server at http://localhost:8000")
    print("  Press Ctrl+C to stop")
    print()
    print("=" * 60)

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
