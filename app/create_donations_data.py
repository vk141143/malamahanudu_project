#!/usr/bin/env python3
"""
Sample data generator for donations module testing
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Donation, DonationStatus, PaymentMethod, Admin
from app.auth import get_password_hash
from datetime import datetime, timedelta
import random

def create_donations_sample_data():
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
    
    # Sample data
    donor_names = [
        "John Doe", "Jane Smith", "Mike Johnson", "Sarah Wilson", "David Brown",
        "Lisa Davis", "Tom Miller", "Anna Garcia", "Chris Martinez", "Emma Taylor"
    ]
    
    payment_methods = [PaymentMethod.upi, PaymentMethod.card, PaymentMethod.netbanking, PaymentMethod.cash]
    statuses = [DonationStatus.pending, DonationStatus.verified, DonationStatus.acknowledged, DonationStatus.failed]
    
    # Create sample donations
    for i in range(1, 151):  # 150 donations
        donor_name = random.choice(donor_names)
        email_name = donor_name.lower().replace(" ", "")
        
        donation = Donation(
            donor_name=donor_name,
            donor_email=f"{email_name}{i}@example.com",
            amount=round(random.uniform(100, 10000), 2),
            payment_method=random.choice(payment_methods),
            transaction_id=f"TXN{random.randint(100000000, 999999999)}",
            status=random.choice(statuses),
            created_at=datetime.now() - timedelta(days=random.randint(1, 365))
        )
        db.add(donation)
    
    db.commit()
    db.close()
    print("Sample donations data created successfully!")
    print("- 150 donations with random data")
    print("- Mixed statuses: pending, verified, acknowledged, failed")
    print("- Various payment methods and amounts")

if __name__ == "__main__":
    create_donations_sample_data()