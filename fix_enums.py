"""
Migration script to remove ENUM constraints from PostgreSQL database
Run this once to fix the enum type issues
"""
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Parse the database URL
# Format: postgresql://user:password@host/database
url_parts = DATABASE_URL.replace("postgresql://", "").split("@")
user_pass = url_parts[0].split(":")
host_db = url_parts[1].split("/")

conn = psycopg2.connect(
    host=host_db[0],
    database=host_db[1],
    user=user_pass[0],
    password=user_pass[1]
)

cursor = conn.cursor()

try:
    print("Removing CHECK constraints and converting to VARCHAR...")
    
    # Drop all CHECK constraints
    cursor.execute("""
        ALTER TABLE members DROP CONSTRAINT IF EXISTS members_status_check;
        ALTER TABLE member_applications DROP CONSTRAINT IF EXISTS member_applications_status_check;
        ALTER TABLE member_applications DROP CONSTRAINT IF EXISTS member_applications_gender_check;
        ALTER TABLE donations DROP CONSTRAINT IF EXISTS donations_status_check;
        ALTER TABLE donations DROP CONSTRAINT IF EXISTS donations_payment_method_check;
        ALTER TABLE complaints DROP CONSTRAINT IF EXISTS complaints_status_check;
        ALTER TABLE complaints DROP CONSTRAINT IF EXISTS complaints_type_check;
        ALTER TABLE gallery DROP CONSTRAINT IF EXISTS gallery_media_type_check;
    """)
    
    # Alter columns to remove any enum types
    cursor.execute("""
        ALTER TABLE members ALTER COLUMN status TYPE VARCHAR(20);
        ALTER TABLE member_applications ALTER COLUMN status TYPE VARCHAR(20);
        ALTER TABLE member_applications ALTER COLUMN gender TYPE VARCHAR(10);
        ALTER TABLE donations ALTER COLUMN status TYPE VARCHAR(20);
        ALTER TABLE donations ALTER COLUMN payment_method TYPE VARCHAR(50);
        ALTER TABLE complaints ALTER COLUMN status TYPE VARCHAR(20);
        ALTER TABLE complaints ALTER COLUMN type TYPE VARCHAR(50);
        ALTER TABLE gallery ALTER COLUMN media_type TYPE VARCHAR(10);
    """)
    
    conn.commit()
    print("SUCCESS: All ENUM constraints removed!")
    print("SUCCESS: Database is now ready to accept string values")
    
except Exception as e:
    conn.rollback()
    print(f"Error: {e}")
    
finally:
    cursor.close()
    conn.close()
