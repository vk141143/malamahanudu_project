import sqlite3

# Connect to the database
conn = sqlite3.connect('admin_dashboard.db')
cursor = conn.cursor()

# Add photo_path column to members table
try:
    cursor.execute("ALTER TABLE members ADD COLUMN photo_path VARCHAR")
    conn.commit()
    print("Successfully added photo_path column to members table")
except sqlite3.OperationalError as e:
    print(f"Column might already exist: {e}")

conn.close()
