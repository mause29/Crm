import sys
sys.path.append('backend')

try:
    from app.main import app
    print("✅ FastAPI app loaded successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")

try:
    from app.database import Base, engine
    print("✅ Database models loaded successfully")
except ImportError as e:
    print(f"❌ Database import error: {e}")

try:
    from app.models import User, Client, Opportunity, Task
    print("✅ SQLAlchemy models loaded successfully")
except ImportError as e:
    print(f"❌ Models import error: {e}")
