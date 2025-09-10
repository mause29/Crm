from backend.app.database_new import engine, Base
from sqlalchemy import text

# Import models before creating tables to register them with Base
from backend.app.models import Achievement, Company, User, Client, Opportunity, Invoice, Task, Notification, Points, UserAchievement, Note

print("Dropping all tables...")
with engine.connect() as conn:
    # Get all table names
    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
    tables = [row[0] for row in result if row[0] != 'sqlite_sequence']

    # Drop all tables
    for table in tables:
        conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
        print(f"Dropped table: {table}")

    conn.commit()

print("Recreating all tables...")
Base.metadata.create_all(bind=engine)
print("Database reset complete!")

from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Create default company
    try:
        if not db.query(Company).first():
            default_company = Company(name="Default Company")
            db.add(default_company)
            db.commit()
            print("Default company created")
    except Exception as e:
        print(f"Error creating default company: {e}")
        db.rollback()

    # Seed achievements
    try:
        if not db.query(Achievement).first():
            achievements = [
                Achievement(name="Primer Vendedor", description="Completa tu primera venta", points_required=50, badge_icon="🏆"),
                Achievement(name="Vendedor Estrella", description="Alcanza 1000 puntos", points_required=1000, badge_icon="⭐"),
                Achievement(name="Maestro de Ventas", description="Cierra 10 oportunidades", points_required=500, badge_icon="👑"),
                Achievement(name="Cliente Builder", description="Añade 5 clientes", points_required=150, badge_icon="👥"),
                Achievement(name="Task Master", description="Completa 10 tareas", points_required=200, badge_icon="✅"),
            ]
            for ach in achievements:
                db.add(ach)
            db.commit()
            print("Sample achievements seeded successfully")
    except Exception as e:
        print(f"Error seeding achievements: {e}")
        db.rollback()
finally:
    db.close()
