"""AI Compliance Shield - Entry Point.

Run the EU AI Act compliance audit tool server.
"""

import uvicorn
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.main import app

if __name__ == "__main__":
    # Production-safe: reload is disabled by default and enabled only
    # when APP_ENV=development is set.
    reload_enabled = os.environ.get("APP_ENV", "").lower() == "development"
    # Use the platform-assigned PORT (e.g. Railway, Render) or default to 8000.
    port = int(os.environ.get("PORT", "8000"))

    print("=" * 60)
    print("  AI Compliance Shield - EU AI Act Compliance Tool")
    print("=" * 60)
    print()
    print(f"  Starting server at http://0.0.0.0:{port}")
    print(f"  Reload: {reload_enabled}")
    print("  Press Ctrl+C to stop")
    print()
    print("=" * 60)

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=port,
        reload=reload_enabled,
    )
