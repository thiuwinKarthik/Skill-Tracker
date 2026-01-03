#!/usr/bin/env python3
"""
Complete API testing script
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_all_skills():
    """Test get all skills"""
    print("\n=== Testing Get All Skills ===")
    response = requests.get(f"{BASE_URL}/skills", params={"limit": 5})
    print(f"Status Code: {response.status_code}")
    skills = response.json()
    print(f"Number of skills: {len(skills)}")
    if skills:
        print(f"First skill: {skills[0]['name']}")
    return response.status_code == 200

def test_get_skill_detail():
    """Test get skill detail"""
    print("\n=== Testing Get Skill Detail ===")
    # First get a skill name
    skills_response = requests.get(f"{BASE_URL}/skills", params={"limit": 1})
    if skills_response.status_code == 200:
        skills = skills_response.json()
        if skills:
            skill_name = skills[0]['name']
            response = requests.get(f"{BASE_URL}/skills/{skill_name}")
            print(f"Status Code: {response.status_code}")
            print(f"Skill: {skill_name}")
            print(f"Risk Score: {response.json().get('risk_score', 'N/A')}")
            return response.status_code == 200
    return False

def test_high_risk_skills():
    """Test high-risk skills"""
    print("\n=== Testing High-Risk Skills ===")
    response = requests.get(f"{BASE_URL}/skills/high-risk", params={"limit": 5})
    print(f"Status Code: {response.status_code}")
    skills = response.json()
    print(f"High-risk skills found: {len(skills)}")
    return response.status_code == 200

def test_emerging_skills():
    """Test emerging skills"""
    print("\n=== Testing Emerging Skills ===")
    response = requests.get(f"{BASE_URL}/skills/emerging", params={"limit": 5})
    print(f"Status Code: {response.status_code}")
    skills = response.json()
    print(f"Emerging skills found: {len(skills)}")
    return response.status_code == 200

def test_role_trends():
    """Test role trends"""
    print("\n=== Testing Role Trends ===")
    response = requests.get(f"{BASE_URL}/roles/trends")
    print(f"Status Code: {response.status_code}")
    roles = response.json()
    print(f"Roles found: {len(roles)}")
    return response.status_code == 200

def test_pipeline():
    """Test pipeline endpoints"""
    print("\n=== Testing Pipeline Endpoints ===")
    
    # Get current status
    status_response = requests.get(f"{BASE_URL}/pipeline/status")
    print(f"Current status: {status_response.json().get('status', 'unknown')}")
    
    # Trigger pipeline (if not running)
    if status_response.json().get('status') != 'running':
        trigger_response = requests.post(f"{BASE_URL}/pipeline/run")
        print(f"Trigger status: {trigger_response.status_code}")
        print(f"Response: {json.dumps(trigger_response.json(), indent=2)}")
        return trigger_response.status_code in [200, 409]  # 409 if already running
    else:
        print("Pipeline already running, skipping trigger")
        return True

def main():
    """Run all tests"""
    print("=" * 50)
    print("API Testing Suite")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Get All Skills", test_get_all_skills),
        ("Get Skill Detail", test_get_skill_detail),
        ("High-Risk Skills", test_high_risk_skills),
        ("Emerging Skills", test_emerging_skills),
        ("Role Trends", test_role_trends),
        ("Pipeline", test_pipeline),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"Error in {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, result in results if result)
    print(f"\nTotal: {passed}/{len(results)} tests passed")

if __name__ == "__main__":
    main()
