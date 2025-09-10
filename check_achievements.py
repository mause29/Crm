from backend.app.database_new import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Check if achievements table exists
    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='achievements'"))
    if result.fetchone():
        print("Achievements table exists")
        # Check achievements table schema
        result = conn.execute(text("PRAGMA table_info(achievements)"))
        print('Achievements table columns:')
        for row in result:
            print(f"  {row[1]}: {row[2]}")
    else:
        print("Achievements table does not exist")
