import sqlite3

# Connect to database
conn = sqlite3.connect('admin_dashboard.db')
cursor = conn.cursor()

# Add blood_group column to member_applications table
try:
    cursor.execute('ALTER TABLE member_applications ADD COLUMN blood_group VARCHAR')
    conn.commit()
    print("Successfully added blood_group column to member_applications table")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Column blood_group already exists")
    else:
        print(f"Error: {e}")

conn.close()
