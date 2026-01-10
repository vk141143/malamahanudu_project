#!/usr/bin/env python3
"""
Generate a strong JWT secret key
"""
import secrets

# Generate a secure random key
secret_key = secrets.token_urlsafe(32)

print("=" * 60)
print("GENERATED JWT SECRET KEY")
print("=" * 60)
print(f"\n{secret_key}\n")
print("=" * 60)
print("\nCopy this key to your .env file:")
print(f"SECRET_KEY={secret_key}")
print("=" * 60)