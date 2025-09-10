from backend.app.database_new import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Check alembic version
    result = conn.execute(text('SELECT * FROM alembic_version'))
    print('Alembic version:', result.fetchone())

    # Check users table schema
    result = conn.execute(text("PRAGMA table_info(users)"))
    print('\nUsers table columns:')
    for row in result:
        print(f"  {row[1]}: {row[2]}")

    # Check clients table schema
    result = conn.execute(text("PRAGMA table_info(clients)"))
    print('\nClients table columns:')
    for row in result:
        print(f"  {row[1]}: {row[2]}")
