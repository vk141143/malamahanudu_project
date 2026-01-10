#!/usr/bin/env python3
"""
Sample data generator for complaints module testing
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Complaint, ComplaintStatus, ComplaintType, Admin
from app.auth import get_password_hash
from datetime import datetime, timedelta
import random

def create_complaints_sample_data():
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
    complainant_names = [
        "Rajesh Kumar", "Priya Sharma", "Amit Singh", "Sunita Devi", "Vikram Reddy",
        "Kavitha Nair", "Suresh Gupta", "Meera Patel", "Ravi Chandra", "Lakshmi Rao"
    ]
    
    complaint_types = [ComplaintType.healthcare, ComplaintType.education, ComplaintType.employment, 
                      ComplaintType.infrastructure, ComplaintType.social_welfare, ComplaintType.other]
    
    statuses = [ComplaintStatus.pending, ComplaintStatus.in_progress, ComplaintStatus.resolved, ComplaintStatus.closed]
    
    subjects = [
        "Hospital facility issues", "School infrastructure problems", "Job application delay",
        "Road maintenance required", "Pension not received", "Water supply issues",
        "Electricity connection problem", "Document verification delay", "Medical reimbursement",
        "Education scholarship query"
    ]
    
    # Create sample complaints
    for i in range(1, 101):  # 100 complaints
        complainant_name = random.choice(complainant_names)
        email_name = complainant_name.lower().replace(" ", "")
        
        complaint = Complaint(
            complainant_name=complainant_name,
            email=f"{email_name}{i}@example.com",
            phone=f"9{random.randint(100000000, 999999999)}",
            type=random.choice(complaint_types),
            subject=random.choice(subjects),
            description=f"Detailed description of the complaint regarding {random.choice(subjects).lower()}. This is a sample complaint for testing purposes.",
            reference_id=f"CMP{i:04d}",
            status=random.choice(statuses),
            admin_notes="Sample admin notes" if random.choice([True, False]) else None,
            created_at=datetime.now() - timedelta(days=random.randint(1, 365))
        )
        db.add(complaint)
    
    db.commit()
    db.close()
    print("Sample complaints data created successfully!")
    print("- 100 complaints with random data")
    print("- Mixed statuses: pending, in_progress, resolved, closed")
    print("- Various complaint types and subjects")

if __name__ == "__main__":
    create_complaints_sample_data()