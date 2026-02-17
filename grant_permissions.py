import psycopg2

# Connect to database
conn = psycopg2.connect(
    host="public-primary-pg-inbangalore-189728-1660502.db.onutho.com",
    port=5432,
    database="defaultdb",
    user="dbadmin",
    password="XYxu6#&8EBw5!3q$"
)

conn.autocommit = True
cursor = conn.cursor()

try:
    print("Granting permissions...")
    cursor.execute("GRANT ALL PRIVILEGES ON SCHEMA public TO dbadmin;")
    cursor.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dbadmin;")
    cursor.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO dbadmin;")
    cursor.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dbadmin;")
    cursor.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO dbadmin;")
    print("Permissions granted successfully!")
except Exception as e:
    print(f"Error: {e}")
    print("\nYou need a superuser account to grant these permissions.")
    print("Contact your database administrator or hosting provider.")
finally:
    cursor.close()
    conn.close()
