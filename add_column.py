#!/usr/bin/env python3

import sys
import os
sys.path.append('backend')

from app.database import engine
from sqlalchemy import text

def add_badge_icon_column():
    try:
        with engine.connect() as conn:
            # Check if column already exists
            result = conn.execute(text("PRAGMA table_info(achievements)"))
            columns = [row[1] for row in result.fetchall()]

            if 'badge_icon' not in columns:
                conn.execute(text("ALTER TABLE achievements ADD COLUMN badge_icon VARCHAR"))
                conn.commit()
                print("✅ Column 'badge_icon' added successfully to achievements table")
            else:
                print("ℹ️ Column 'badge_icon' already exists in achievements table")

    except Exception as e:
        print(f"❌ Error adding column: {e}")

if __name__ == "__main__":
    add_badge_icon_column()
