#!/usr/bin/env python3
"""
Simple script to seed demo users
"""
from backend.app.database_new import SessionLocal
from backend.app.models import User, Company
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def seed_demo_users():
    db = SessionLocal()

    try:
        # Create demo company
        company = db.query(Company).filter(Company.name == "Demo Company").first()
        if not company:
            company = Company(name="Demo Company")
            db.add(company)
            db.commit()
            db.refresh(company)
            print("✅ Demo company created")

        # Create admin user
        admin = db.query(User).filter(User.email == "admin@crm.com").first()
        if not admin:
            hashed_password = get_password_hash("admin123")
            admin_user = User(
                name="Admin User",
                email="admin@crm.com",
                hashed_password=hashed_password,
                role="admin",
                company_id=company.id,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Admin user created: admin@crm.com / admin123")

        # Create regular user
        user = db.query(User).filter(User.email == "user@crm.com").first()
        if not user:
            hashed_password = get_password_hash("user123")
            regular_user = User(
                name="Test User",
                email="user@crm.com",
                hashed_password=hashed_password,
                role="user",
                company_id=company.id,
                is_active=True
            )
            db.add(regular_user)
            db.commit()
            print("✅ Regular user created: user@crm.com / user123")

        print("\n🎉 Demo users seeded successfully!")
        print("Login credentials:")
        print("- Admin: admin@crm.com / admin123")
        print("- User: user@crm.com / user123")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_users()
