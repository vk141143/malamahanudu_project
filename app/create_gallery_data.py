#!/usr/bin/env python3
"""
Sample data generator for gallery module testing
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Gallery, MediaType, Admin
from app.auth import get_password_hash
from datetime import datetime, timedelta
import random
import os
from pathlib import Path

def create_gallery_sample_data():
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
    
    # Create uploads directory
    upload_dir = Path("uploads/gallery")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample data
    image_titles = [
        "Community Event 2024", "Health Camp", "Education Program", "Infrastructure Development",
        "Cultural Festival", "Sports Meet", "Awareness Campaign", "Tree Plantation Drive",
        "Medical Camp", "Skill Development Workshop"
    ]
    
    video_titles = [
        "Annual Conference Highlights", "Community Success Stories", "Training Session",
        "Project Launch Event", "Member Testimonials", "Achievement Ceremony",
        "Workshop Documentation", "Field Visit Coverage", "Program Overview", "Impact Stories"
    ]
    
    descriptions = [
        "A memorable event showcasing community participation and engagement.",
        "Documenting our efforts to serve the community better.",
        "Capturing moments of growth and development in our programs.",
        "Highlighting the positive impact of our initiatives.",
        "Showcasing the dedication and hard work of our team members."
    ]
    
    # Create sample gallery items (without actual files for demo)
    for i in range(1, 21):  # 20 gallery items
        if i <= 12:  # 12 images
            title = random.choice(image_titles)
            media_type = MediaType.image
            media_url = f"uploads/gallery/sample_image_{i}.jpg"
        else:  # 8 videos
            title = random.choice(video_titles)
            media_type = MediaType.video
            media_url = f"uploads/gallery/sample_video_{i}.mp4"
        
        gallery_item = Gallery(
            title=f"{title} {i}",
            description=random.choice(descriptions),
            media_url=media_url,
            media_type=media_type,
            created_at=datetime.now() - timedelta(days=random.randint(1, 365))
        )
        db.add(gallery_item)
    
    db.commit()
    db.close()
    print("Sample gallery data created successfully!")
    print("- 20 gallery items (12 images, 8 videos)")
    print("- Note: Actual media files are not created, only database entries")
    print("- Upload real files through the API to test file handling")

if __name__ == "__main__":
    create_gallery_sample_data()