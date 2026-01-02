#!/usr/bin/env python3
"""
Debug script to test all API endpoints and identify 405 errors
"""
import requests
import json
from urllib.parse import quote

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, description, data=None):
    """Test an endpoint and report results"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"{method} {endpoint}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=10)
        else:
            print(f"❌ Unknown method: {method}")
            return
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 405:
            print(f"❌ METHOD NOT ALLOWED!")
            print(f"Allowed methods might be: {response.headers.get('Allow', 'Unknown')}")
        elif response.status_code >= 400:
            print(f"❌ Error: {response.text}")
        else:
            print(f"✅ Success!")
            try:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            except:
                print(f"Response: {response.text[:200]}")
                
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error - Is the server running on {BASE_URL}?")
    except requests.exceptions.Timeout:
        print(f"❌ Timeout - Request took too long")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("="*60)
    print("API ENDPOINT DEBUGGER")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print("\nMake sure the backend server is running!")
    print("Start it with: cd backend && uvicorn app.main:app --reload")
    
    # Test all endpoints
    endpoints = [
        ("GET", "/health", "Health Check"),
        ("GET", "/health/", "Health Check (with trailing slash)"),
        ("GET", "/skills", "Get All Skills"),
        ("GET", "/skills?limit=2", "Get Skills with limit"),
        ("GET", "/skills/high-risk", "Get High-Risk Skills"),
        ("GET", "/skills/emerging", "Get Emerging Skills"),
        ("GET", "/roles/trends", "Get Role Trends"),
        ("GET", "/pipeline/status", "Get Pipeline Status"),
        ("GET", "/pipeline/status/", "Get Pipeline Status (with trailing slash)"),
        ("POST", "/pipeline/run", "Trigger Pipeline"),
        ("POST", "/pipeline/run/", "Trigger Pipeline (with trailing slash)"),
        # Test wrong methods
        ("GET", "/pipeline/run", "❌ WRONG: GET on /pipeline/run (should be POST)"),
        ("POST", "/pipeline/status", "❌ WRONG: POST on /pipeline/status (should be GET)"),
        ("POST", "/health", "❌ WRONG: POST on /health (should be GET)"),
    ]
    
    for method, endpoint, description in endpoints:
        test_endpoint(method, endpoint, description)
    
    print("\n" + "="*60)
    print("DEBUGGING COMPLETE")
    print("="*60)
    print("\nIf you see 405 errors:")
    print("1. Check the 'Allowed methods' in the error response")
    print("2. Make sure you're using the correct HTTP method")
    print("3. Check if there's a trailing slash issue")
    print("4. Restart the backend server if you made code changes")

if __name__ == "__main__":
    main()

