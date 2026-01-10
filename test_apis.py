#!/usr/bin/env python3
"""
API Test Script - Tests all endpoints
Run the server first: uvicorn app.main:app --reload
Then run: python test_apis.py
"""
import requests
import json
from io import BytesIO

BASE_URL = "http://localhost:8000"

def test_admin_login():
    """Test admin login"""
    print("\n=== Testing Admin Login ===")
    response = requests.post(
        f"{BASE_URL}/admin/login",
        json={"email": "admin@example.com", "password": "admin123"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✓ Login successful, token: {token[:20]}...")
        return token
    else:
        print(f"✗ Login failed: {response.text}")
        return None

def test_public_donation():
    """Test public donation API"""
    print("\n=== Testing Public Donation ===")
    response = requests.post(
        f"{BASE_URL}/public/donations",
        json={
            "full_name": "John Doe",
            "email_address": "john@example.com",
            "phone_number": "9876543210",
            "payment_method": "upi",
            "preset_amount": 1000,
            "transaction_id": "TXN123456789",
            "notes": "Test donation"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_public_membership():
    """Test public membership application"""
    print("\n=== Testing Public Membership Application ===")
    
    # Create a dummy image file
    image_data = BytesIO(b"fake image data")
    image_data.name = "photo.jpg"
    
    files = {"photo": ("photo.jpg", image_data, "image/jpeg")}
    data = {
        "full_name": "Jane Smith",
        "father_husband_name": "Robert Smith",
        "gender": "female",
        "date_of_birth": "15-01-1990",
        "caste": "General",
        "aadhaar_number": "123456789012",
        "phone_number": "9876543210",
        "email_address": "jane@example.com",
        "state": "Telangana",
        "district": "Hyderabad",
        "mandal": "Secunderabad",
        "village": "Jubilee Hills",
        "full_address": "123 Main Street"
    }
    
    response = requests.post(
        f"{BASE_URL}/public/membership/apply",
        data=data,
        files=files
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_public_complaint():
    """Test public complaint API"""
    print("\n=== Testing Public Complaint ===")
    
    data = {
        "full_name": "Mike Johnson",
        "phone_number": "9876543210",
        "address": "456 Oak Street",
        "complaint_type": "Healthcare",
        "subject": "Hospital facility issues",
        "detailed_description": "Detailed complaint description here"
    }
    
    response = requests.post(
        f"{BASE_URL}/public/complaints",
        data=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_public_gallery():
    """Test public gallery API"""
    print("\n=== Testing Public Gallery ===")
    response = requests.get(f"{BASE_URL}/public/gallery")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total items: {data['total']}")
    return response.status_code == 200

def test_admin_dashboard(token):
    """Test admin dashboard APIs"""
    print("\n=== Testing Admin Dashboard Summary ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/admin/dashboard/summary", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    return response.status_code == 200

def test_admin_members(token):
    """Test admin members APIs"""
    print("\n=== Testing Admin Members Summary ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/admin/members/summary", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    return response.status_code == 200

def test_admin_donations(token):
    """Test admin donations APIs"""
    print("\n=== Testing Admin Donations Summary ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/admin/donations/summary", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    return response.status_code == 200

def test_admin_complaints(token):
    """Test admin complaints APIs"""
    print("\n=== Testing Admin Complaints Summary ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/admin/complaints/summary", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    return response.status_code == 200

def test_admin_gallery(token):
    """Test admin gallery APIs"""
    print("\n=== Testing Admin Gallery Summary ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/admin/gallery/summary", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    return response.status_code == 200

def main():
    print("=" * 60)
    print("API TESTING SUITE")
    print("=" * 60)
    
    results = {}
    
    # Test admin login first
    token = test_admin_login()
    results["Admin Login"] = token is not None
    
    # Test public APIs (no auth required)
    results["Public Donation"] = test_public_donation()
    results["Public Membership"] = test_public_membership()
    results["Public Complaint"] = test_public_complaint()
    results["Public Gallery"] = test_public_gallery()
    
    # Test admin APIs (auth required)
    if token:
        results["Admin Dashboard"] = test_admin_dashboard(token)
        results["Admin Members"] = test_admin_members(token)
        results["Admin Donations"] = test_admin_donations(token)
        results["Admin Complaints"] = test_admin_complaints(token)
        results["Admin Gallery"] = test_admin_gallery(token)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:30} {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to server")
        print("Please start the server first:")
        print("  uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")