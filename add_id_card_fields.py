"""
Migration script to add ID card fields to members and member_applications tables
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def run_migration():
    with engine.connect() as conn:
        try:
            # Add columns to members table
            conn.execute(text("ALTER TABLE members ADD COLUMN IF NOT EXISTS designation VARCHAR(100)"))
            conn.execute(text("ALTER TABLE members ADD COLUMN IF NOT EXISTS father_husband_name VARCHAR(255)"))
            conn.execute(text("ALTER TABLE members ADD COLUMN IF NOT EXISTS full_address TEXT"))
            conn.execute(text("ALTER TABLE members ADD COLUMN IF NOT EXISTS village VARCHAR(255)"))
            
            # Add designation column to member_applications table
            conn.execute(text("ALTER TABLE member_applications ADD COLUMN IF NOT EXISTS designation VARCHAR(100)"))
            
            conn.commit()
            print("[SUCCESS] Migration completed successfully!")
            print("[SUCCESS] Added designation, father_husband_name, full_address, village to members table")
            print("[SUCCESS] Added designation to member_applications table")
        except Exception as e:
            print(f"[ERROR] Migration failed: {str(e)}")
            conn.rollback()

if __name__ == "__main__":
    run_migration()
