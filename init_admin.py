#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initialize database tables and create admin user
"""
from app.database import SessionLocal, engine
from app.models import Base, Admin
from app.auth import get_password_hash

def init_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("[OK] Tables created successfully!")
    
    db = SessionLocal()
    
    # Check if admin exists
    existing_admin = db.query(Admin).filter(Admin.email == "admin@example.com").first()
    
    if existing_admin:
        print("\n[OK] Admin already exists!")
        print("Email: admin@example.com")
        print("Password: admin123")
    else:
        # Create admin
        admin = Admin(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123")
        )
        db.add(admin)
        db.commit()
        print("\n[OK] Admin created successfully!")
        print("Email: admin@example.com")
        print("Password: admin123")
    
    db.close()
    print("\n[OK] Database initialization complete!")

if __name__ == "__main__":
    init_database()