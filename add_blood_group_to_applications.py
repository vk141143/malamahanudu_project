from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Check if blood_group column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='member_applications' AND column_name='blood_group'
        """))
        
        if result.fetchone() is None:
            print("Adding blood_group column...")
            conn.execute(text("""
                ALTER TABLE member_applications 
                ADD COLUMN blood_group VARCHAR(10)
            """))
            conn.commit()
            print("blood_group column added successfully!")
        else:
            print("blood_group column already exists")
            
except Exception as e:
    print(f"Error: {str(e)}")
