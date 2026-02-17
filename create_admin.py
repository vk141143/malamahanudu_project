from app.auth import get_password_hash
from app.database import SessionLocal
from app.models import Admin

db = SessionLocal()

# Delete existing admin
db.query(Admin).filter(Admin.email == "admin@example.com").delete()

# Create new admin with hashed password
hashed_password = get_password_hash("admin123")
admin = Admin(
    email="admin@example.com",
    hashed_password=hashed_password
)

db.add(admin)
db.commit()

print("Admin created successfully!")
print("Email: admin@example.com")
print("Password: admin123")
print(f"Hash: {hashed_password}")
