#!/usr/bin/env python3
"""
Simple test script to verify the CRM server can start
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    print("Testing imports...")
    from app.main import app
    print("✅ Main app imported successfully")

    from app.database_new import Base, engine
    print("✅ Database imported successfully")

    from app.routes import users, clientes, oportunidades, facturas
    print("✅ Routes imported successfully")

    print("\n🎉 All imports successful! Server should be ready to run.")
    print("You can start the server with:")
    print("cd backend && python main.py")
    print("Or with uvicorn:")
    print("cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")

except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
