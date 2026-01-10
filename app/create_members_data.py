#!/usr/bin/env python3
"""
Sample data generator for members module testing
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Member, MemberStatus, Admin
from app.auth import get_password_hash
from datetime import datetime, timedelta
import random

def create_members_sample_data():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Create admin if not exists
    existing_admin = db.query(Admin).first()
    if not existing_admin:
        admin = Admin(
            email=\"admin@example.com\",
            hashed_password=get_password_hash(\"admin123\")
        )
        db.add(admin)
        print(\"Admin created: admin@example.com / admin123\")\n    \n    # Sample data\n    states = [\"Andhra Pradesh\", \"Telangana\", \"Karnataka\", \"Tamil Nadu\"]\n    districts = {\n        \"Andhra Pradesh\": [\"Visakhapatnam\", \"Vijayawada\", \"Guntur\", \"Tirupati\"],\n        \"Telangana\": [\"Hyderabad\", \"Warangal\", \"Nizamabad\", \"Karimnagar\"],\n        \"Karnataka\": [\"Bangalore\", \"Mysore\", \"Hubli\", \"Mangalore\"],\n        \"Tamil Nadu\": [\"Chennai\", \"Coimbatore\", \"Madurai\", \"Salem\"]\n    }\n    mandals = [\"Mandal1\", \"Mandal2\", \"Mandal3\", \"Mandal4\", \"Mandal5\"]\n    statuses = [MemberStatus.pending, MemberStatus.approved, MemberStatus.rejected]\n    \n    # Create sample members\n    for i in range(1, 101):\n        state = random.choice(states)\n        district = random.choice(districts[state])\n        mandal = random.choice(mandals)\n        \n        member = Member(\n            membership_id=f\"MEM{i:04d}\",\n            name=f\"Member {i}\",\n            phone=f\"9{random.randint(100000000, 999999999)}\",\n            email=f\"member{i}@example.com\",\n            aadhaar=f\"{random.randint(100000000000, 999999999999)}\",\n            state=state,\n            district=district,\n            mandal=mandal,\n            status=random.choice(statuses),\n            created_at=datetime.now() - timedelta(days=random.randint(1, 365))\n        )\n        db.add(member)\n    \n    db.commit()\n    db.close()\n    print(\"Sample members data created successfully!\")\n    print(\"- 100 members with random data\")\n    print(\"- Mixed statuses: pending, approved, rejected\")\n    print(\"- Multiple states and districts\")\n\nif __name__ == \"__main__\":\n    create_members_sample_data()