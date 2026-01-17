from app.database import engine
from sqlalchemy import text

# Add qr_code_path column to members table
with engine.connect() as conn:
    conn.execute(text("ALTER TABLE members ADD COLUMN IF NOT EXISTS qr_code_path VARCHAR"))
    conn.commit()
    print("Successfully added qr_code_path column to members table")
