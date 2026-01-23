import sqlite3

# Connect to database
conn = sqlite3.connect('admin_dashboard.db')
cursor = conn.cursor()

try:
    # Add blood_group column to members table
    cursor.execute('ALTER TABLE members ADD COLUMN blood_group VARCHAR')
    conn.commit()
    print("Successfully added blood_group column to members table")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e).lower():
        print("blood_group column already exists in members table")
    else:
        print(f"Error: {e}")
finally:
    conn.close()
