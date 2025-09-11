import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(__file__))

from database_new import Base, engine
from models import *
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def init_database():
    """Initialize the database with all tables and sample data"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)

        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        # Check if we already have data
        if db.query(User).count() > 0:
            print("Database already initialized")
            db.close()
            return

        # Create a sample company
        company = Company(name="Sample Company")
        db.add(company)
        db.commit()
        db.refresh(company)

        # Create a sample user
        hashed_password = get_password_hash("test123")
        user = User(
            name="Test User",
            email="test@example.com",
            hashed_password=hashed_password,
            role="admin",
            company_id=company.id,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create sample achievements
        achievements_data = [
            {"name": "First Steps", "description": "Complete your first task", "points_required": 50, "badge_icon": "🎯"},
            {"name": "Task Master", "description": "Complete 10 tasks", "points_required": 100, "badge_icon": "📋"},
            {"name": "Client Builder", "description": "Add 5 clients", "points_required": 150, "badge_icon": "👥"},
            {"name": "Deal Closer", "description": "Close 3 deals", "points_required": 200, "badge_icon": "💰"},
            {"name": "CRM Champion", "description": "Earn 500 points", "points_required": 500, "badge_icon": "🏆"}
        ]

        for ach_data in achievements_data:
            achievement = Achievement(**ach_data)
            db.add(achievement)

        db.commit()
        print("Database initialized successfully with sample data")
        db.close()

    except Exception as e:
        print(f"Error initializing database: {e}")
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    init_database()
