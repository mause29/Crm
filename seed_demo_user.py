#!/usr/bin/env python3
"""
Script to seed demo user for testing
"""
from backend.app.database_new import SessionLocal
from backend.app.models import User, Company
from backend.app.routes.users import get_password_hash
from sqlalchemy.orm import sessionmaker

def seed_demo_user():
    db = SessionLocal()

    try:
        # Check if demo company exists
        company = db.query(Company).filter(Company.name == "Demo Company").first()
        if not company:
            company = Company(name="Demo Company")
            db.add(company)
            db.commit()
            db.refresh(company)
            print("✅ Demo company created")

        # Check if demo user exists
        user = db.query(User).filter(User.email == "admin@crm.com").first()
        if not user:
            hashed_password = get_password_hash("admin123")
            demo_user = User(
                email="admin@crm.com",
                hashed_password=hashed_password,
                name="Admin User",
                role="admin",
                company_id=company.id,
                is_active=True
            )
            db.add(demo_user)
            db.commit()
            print("✅ Demo admin user created: admin@crm.com / admin123")
        else:
            print("ℹ️  Demo user already exists")

        # Also create a regular user for testing
        regular_user = db.query(User).filter(User.email == "user@crm.com").first()
        if not regular_user:
            hashed_password = get_password_hash("user123")
            test_user = User(
                email="user@crm.com",
                hashed_password=hashed_password,
                name="Test User",
                role="user",
                company_id=company.id,
                is_active=True
            )
            db.add(test_user)
            db.commit()
            print("✅ Demo regular user created: user@crm.com / user123")

    except Exception as e:
        print(f"❌ Error seeding demo users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_user()
    print("\n🎉 Demo users seeded successfully!")
    print("You can now login with:")
    print("- Admin: admin@crm.com / admin123")
    print("- User: user@crm.com / user123")
