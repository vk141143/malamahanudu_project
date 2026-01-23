import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: DATABASE_URL not found in environment variables")
    exit(1)

# Create engine
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Add blood_group column to members table
        conn.execute(text('ALTER TABLE members ADD COLUMN IF NOT EXISTS blood_group VARCHAR'))
        conn.commit()
        print("Successfully added blood_group column to members table")
except Exception as e:
    print(f"Error: {e}")
