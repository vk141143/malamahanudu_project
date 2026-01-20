import sqlite3

conn = sqlite3.connect('admin_dashboard.db')
cursor = conn.cursor()

# Drop and recreate the table with correct schema
cursor.execute('DROP TABLE IF EXISTS member_applications')

cursor.execute('''
CREATE TABLE member_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR,
    father_husband_name VARCHAR,
    gender VARCHAR,
    date_of_birth DATE,
    caste VARCHAR,
    aadhaar_number VARCHAR,
    phone_number VARCHAR,
    email_address VARCHAR,
    blood_group VARCHAR,
    state VARCHAR,
    district VARCHAR,
    mandal VARCHAR,
    village VARCHAR,
    full_address TEXT,
    photo_path VARCHAR,
    status VARCHAR DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print("member_applications table recreated successfully with blood_group column")
