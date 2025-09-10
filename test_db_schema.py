#!/usr/bin/env python3
"""
Simple script to test database schema and fix issues
"""
import sys
import os
sys.path.append('backend')

from sqlalchemy import create_engine, inspect
from backend.app.database_new import Base, engine
from backend.app.models import Achievement

def test_database_schema():
    """Test if database schema matches models"""
    print("Testing database schema...")

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")

    # Check if achievements table exists and has correct columns
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")

    if 'achievements' in tables:
        columns = inspector.get_columns('achievements')
        column_names = [col['name'] for col in columns]
        print(f"Achievements table columns: {column_names}")

        if 'icon' in column_names:
            print("✓ 'icon' column exists in achievements table")
        else:
            print("✗ 'icon' column missing in achievements table")

        if 'badge_icon' in column_names:
            print("✓ 'badge_icon' column exists in achievements table")
        else:
            print("✗ 'badge_icon' column missing in achievements table")
    else:
        print("✗ achievements table does not exist")

    # Test creating an achievement
    try:
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        achievement = Achievement(
            name="Test Achievement",
            description="Test description",
            points_required=50,
            icon="🏆"
        )
        db.add(achievement)
        db.commit()
        print("✓ Successfully created achievement with 'icon' column")

        db.close()
    except Exception as e:
        print(f"✗ Error creating achievement: {e}")

if __name__ == "__main__":
    test_database_schema()
