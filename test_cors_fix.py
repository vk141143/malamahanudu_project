import requests
import json

BASE_URL = "https://api.incirclejobs.com"

print("Testing CORS and Endpoint Fixes\n")
print("=" * 50)

# Test 1: Check if server is responding
print("\n1. Testing server health...")
try:
    response = requests.get(f"{BASE_URL}/public/gallery", timeout=10)
    print(f"   Status: {response.status_code}")
    print(f"   CORS Headers Present: {'Access-Control-Allow-Origin' in response.headers}")
    if 'Access-Control-Allow-Origin' in response.headers:
        print(f"   CORS Origin: {response.headers['Access-Control-Allow-Origin']}")
except Exception as e:
    print(f"   Error: {str(e)}")

# Test 2: Test OPTIONS preflight request
print("\n2. Testing CORS preflight (OPTIONS)...")
try:
    response = requests.options(
        f"{BASE_URL}/public/membership/apply",
        headers={
            "Origin": "https://org.incirclejobs.com",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type"
        },
        timeout=10
    )
    print(f"   Status: {response.status_code}")
    print(f"   Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
    print(f"   Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'NOT SET')}")
except Exception as e:
    print(f"   Error: {str(e)}")

# Test 3: Test membership application endpoint structure
print("\n3. Testing membership application endpoint...")
try:
    # This will fail validation but should return proper error with CORS headers
    response = requests.post(
        f"{BASE_URL}/public/membership/apply",
        headers={"Origin": "https://org.incirclejobs.com"},
        data={"full_name": "Test"},
        timeout=10
    )
    print(f"   Status: {response.status_code}")
    print(f"   CORS Headers Present: {'Access-Control-Allow-Origin' in response.headers}")
    if response.status_code >= 400:
        print(f"   Error Response: {response.text[:200]}")
except Exception as e:
    print(f"   Error: {str(e)}")

print("\n" + "=" * 50)
print("Test completed!")
