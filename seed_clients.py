#!/usr/bin/env python3
"""
Script to seed demo clients and related data for testing
"""
from backend.app.database_new import SessionLocal
from backend.app.models import Client, Company, User
from datetime import datetime

def seed_demo_clients():
    db = SessionLocal()

    try:
        # Get demo company
        company = db.query(Company).filter(Company.name == "Demo Company").first()
        if not company:
            print("❌ Demo company not found. Please seed demo users first.")
            return

        # Get admin user
        admin_user = db.query(User).filter(User.email == "admin@crm.com").first()
        if not admin_user:
            print("❌ Admin user not found. Please seed demo users first.")
            return

        # Check if demo clients exist
        existing_client = db.query(Client).filter(Client.email == "client1@demo.com").first()
        if existing_client:
            print("ℹ️ Demo clients already exist")
            return

        # Create demo clients
        client1 = Client(
            name="Demo Client 1",
            email="client1@demo.com",
            phone="1234567890",
            company_id=company.id,
            created_by=admin_user.id,
            created_at=datetime.utcnow()
        )
        client2 = Client(
            name="Demo Client 2",
            email="client2@demo.com",
            phone="0987654321",
            company_id=company.id,
            created_by=admin_user.id,
            created_at=datetime.utcnow()
        )
        db.add_all([client1, client2])
        db.commit()
        print("✅ Demo clients created")

    except Exception as e:
        print(f"❌ Error seeding demo clients: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_clients()
    print("\n🎉 Demo clients seeded successfully!")
