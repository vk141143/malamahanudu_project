#!/usr/bin/env python3
"""
Generate bcrypt password hash for admin accounts
Usage: python hash_password.py
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

if __name__ == "__main__":
    password = input("Enter password to hash: ")
    hashed = hash_password(password)
    print(f"Hashed password: {hashed}")
    print(f"SQL: INSERT INTO admins (email, hashed_password) VALUES ('your_email@example.com', '{hashed}');")