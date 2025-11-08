"""
Test script to verify the FastAPI server can start.
"""

import sys
import traceback

print("Testing FastAPI app import...")
try:
    from app.main import app
    print("[OK] App imported successfully")
except Exception as e:
    print(f"[ERROR] Error importing app: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\nTesting database initialization...")
try:
    from app.database.db_init import init_db
    init_db()
    print("[OK] Database initialized successfully")
except Exception as e:
    print(f"[ERROR] Error initializing database: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n[OK] All checks passed! Server should start correctly.")
print("\nTo start the server, run:")
print("  python run_server.py")
print("or")
print("  python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")

