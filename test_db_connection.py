from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

try:
    # Test connection
    with engine.connect() as conn:
        print("Database connection successful!")
        
        # Check tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\nAvailable tables: {tables}")
        
        # Check member_applications table structure
        if 'member_applications' in tables:
            print("\nmember_applications table exists")
            columns = inspector.get_columns('member_applications')
            print("\nColumns in member_applications:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
        else:
            print("\nmember_applications table does NOT exist!")
            
except Exception as e:
    print(f"Database connection failed: {str(e)}")
