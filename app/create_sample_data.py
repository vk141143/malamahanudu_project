#!/usr/bin/env python3
"""
Sample data generator for dashboard testing
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Member, Donation, Complaint, DonationStatus, ComplaintStatus
from app.auth import get_password_hash
from app.models import Admin
from datetime import datetime, timedelta
import random

def create_sample_data():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Create admin if not exists
    existing_admin = db.query(Admin).first()
    if not existing_admin:
        admin = Admin(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123")
        )
        db.add(admin)
        print("Admin created: admin@example.com / admin123")
    
    # Sample districts
    districts = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad"]
    
    # Create sample members
    for i in range(1, 201):
        member = Member(
            name=f"Member {i}",
            district=random.choice(districts),
            is_active=random.choice([True, False]),
            id_card_generated=random.choice([True, False]),
            created_at=datetime.now() - timedelta(days=random.randint(1, 180))
        )
        db.add(member)
    
    # Create sample donations
    for i in range(1, 101):
        donation = Donation(
            amount=random.uniform(100, 5000),
            status=random.choice([DonationStatus.success, DonationStatus.failed]),
            created_at=datetime.now() - timedelta(days=random.randint(1, 180))
        )
        db.add(donation)
    
    # Create sample complaints
    for i in range(1, 51):
        complaint = Complaint(
            status=random.choice([ComplaintStatus.pending, ComplaintStatus.resolved]),
            created_at=datetime.now() - timedelta(days=random.randint(1, 180))
        )
        db.add(complaint)
    
    db.commit()
    db.close()
    print("Sample data created successfully!")

if __name__ == "__main__":
    create_sample_data()