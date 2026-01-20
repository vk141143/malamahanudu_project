from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Check current constraints
        result = conn.execute(text("""
            SELECT column_name, is_nullable, data_type
            FROM information_schema.columns 
            WHERE table_name='member_applications' 
            AND column_name IN ('village', 'full_address')
        """))
        
        print("Current column settings:")
        for row in result:
            print(f"  {row[0]}: nullable={row[1]}, type={row[2]}")
        
        # Make village and full_address nullable
        print("\nMaking columns nullable...")
        conn.execute(text("""
            ALTER TABLE member_applications 
            ALTER COLUMN village DROP NOT NULL
        """))
        conn.execute(text("""
            ALTER TABLE member_applications 
            ALTER COLUMN full_address DROP NOT NULL
        """))
        conn.commit()
        print("Columns updated successfully!")
            
except Exception as e:
    print(f"Error: {str(e)}")
