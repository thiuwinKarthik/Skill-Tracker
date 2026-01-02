# API Testing Guide

Complete guide to all API endpoints with request/response examples and testing commands.

## Base URL

```
http://localhost:8000
```

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Endpoints

### 1. Health Check

**GET** `/health`

Check API health status.

#### Response Example

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456",
  "version": "1.0.0"
}
```

#### Test with cURL

```bash
curl -X GET http://localhost:8000/health
```

#### Test with Python

```python
import requests

response = requests.get("http://localhost:8000/health")
print(response.json())
```

---

### 2. Get All Skills

**GET** `/skills`

Retrieve all skills with optional filtering.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Limit results (1-1000) |
| `min_risk` | float | No | Minimum risk score (0.0-1.0) |
| `max_risk` | float | No | Maximum risk score (0.0-1.0) |

#### Response Example

```json
[
  {
    "name": "React",
    "normalized_name": "React",
    "current_demand": 1250.0,
    "forecast_demand": 1350.0,
    "risk_score": 0.12,
    "risk_category": "low",
    "trend": "increasing",
    "last_updated": "2024-01-15T10:30:00.123456"
  },
  {
    "name": "Angular",
    "normalized_name": "Angular",
    "current_demand": 850.0,
    "forecast_demand": 720.0,
    "risk_score": 0.78,
    "risk_category": "high",
    "trend": "decreasing",
    "last_updated": "2024-01-15T10:30:00.123456"
  }
]
```

#### Test Examples

```bash
# Get all skills
curl -X GET http://localhost:8000/skills

# Get first 10 skills
curl -X GET "http://localhost:8000/skills?limit=10"

# Get high-risk skills only
curl -X GET "http://localhost:8000/skills?min_risk=0.7"

# Get low-risk skills only
curl -X GET "http://localhost:8000/skills?max_risk=0.3"

# Combined filters
curl -X GET "http://localhost:8000/skills?min_risk=0.5&max_risk=0.8&limit=20"
```

#### Python Example

```python
import requests

# Get all skills
response = requests.get("http://localhost:8000/skills")
skills = response.json()
print(f"Total skills: {len(skills)}")

# Get high-risk skills
response = requests.get("http://localhost:8000/skills", params={"min_risk": 0.7})
high_risk = response.json()
print(f"High-risk skills: {len(high_risk)}")
```

---

### 3. Get Skill Detail

**GET** `/skills/{skill_name}`

Get detailed information about a specific skill.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `skill_name` | string | Yes | Name of the skill (URL encoded) |

#### Response Example

```json
{
  "name": "React",
  "normalized_name": "React",
  "current_demand": 1250.0,
  "forecast_demand": 1350.0,
  "risk_score": 0.12,
  "risk_category": "low",
  "trend": "increasing",
  "last_updated": "2024-01-15T10:30:00.123456",
  "job_posting_growth": 25.5,
  "github_velocity": 15.3,
  "community_mentions": 1250.0,
  "research_citations": 45.0,
  "related_skills": ["JavaScript", "TypeScript", "Node.js"],
  "historical_data": []
}
```

#### Test Examples

```bash
# Get React details
curl -X GET http://localhost:8000/skills/React

# Get Python details (URL encoded)
curl -X GET "http://localhost:8000/skills/Python"

# Get skill with special characters
curl -X GET "http://localhost:8000/skills/C%2B%2B"
```

#### Python Example

```python
import requests
from urllib.parse import quote

skill_name = "React"
response = requests.get(f"http://localhost:8000/skills/{quote(skill_name)}")
skill = response.json()
print(f"Skill: {skill['name']}")
print(f"Risk Score: {skill['risk_score']}")
print(f"Trend: {skill['trend']}")
```

---

### 4. Get High-Risk Skills

**GET** `/skills/high-risk`

Get skills with high obsolescence risk (≥70%).

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Limit results (1-100, default: 10) |

#### Response Example

```json
[
  {
    "name": "Angular",
    "normalized_name": "Angular",
    "current_demand": 850.0,
    "forecast_demand": 720.0,
    "risk_score": 0.78,
    "risk_category": "high",
    "trend": "decreasing",
    "last_updated": "2024-01-15T10:30:00.123456"
  },
  {
    "name": "jQuery",
    "normalized_name": "jQuery",
    "current_demand": 320.0,
    "forecast_demand": 250.0,
    "risk_score": 0.85,
    "risk_category": "high",
    "trend": "decreasing",
    "last_updated": "2024-01-15T10:30:00.123456"
  }
]
```

#### Test Examples

```bash
# Get top 10 high-risk skills
curl -X GET http://localhost:8000/skills/high-risk

# Get top 50 high-risk skills
curl -X GET "http://localhost:8000/skills/high-risk?limit=50"
```

#### Python Example

```python
import requests

response = requests.get("http://localhost:8000/skills/high-risk", params={"limit": 20})
high_risk_skills = response.json()

for skill in high_risk_skills:
    print(f"{skill['name']}: {skill['risk_score']*100:.1f}% risk")
```

---

### 5. Get Emerging Skills

**GET** `/skills/emerging`

Get emerging skills with low risk and high growth.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Limit results (1-100, default: 10) |

#### Response Example

```json
[
  {
    "name": "React",
    "normalized_name": "React",
    "current_demand": 1250.0,
    "forecast_demand": 1350.0,
    "risk_score": 0.12,
    "risk_category": "low",
    "trend": "increasing",
    "last_updated": "2024-01-15T10:30:00.123456"
  },
  {
    "name": "TypeScript",
    "normalized_name": "TypeScript",
    "current_demand": 980.0,
    "forecast_demand": 1100.0,
    "risk_score": 0.15,
    "risk_category": "low",
    "trend": "increasing",
    "last_updated": "2024-01-15T10:30:00.123456"
  }
]
```

#### Test Examples

```bash
# Get top 10 emerging skills
curl -X GET http://localhost:8000/skills/emerging

# Get top 30 emerging skills
curl -X GET "http://localhost:8000/skills/emerging?limit=30"
```

#### Python Example

```python
import requests

response = requests.get("http://localhost:8000/skills/emerging", params={"limit": 25})
emerging_skills = response.json()

for skill in emerging_skills:
    print(f"{skill['name']}: {skill['job_posting_growth']:.1f}% growth")
```

---

### 6. Get Role Trends

**GET** `/roles/trends`

Get technology roles and their required skills.

#### Response Example

```json
[
  {
    "name": "Software Engineer",
    "normalized_name": "Software Engineer",
    "required_skills": ["Python", "JavaScript", "Git"],
    "demand_trend": "increasing",
    "last_updated": "2024-01-15T10:30:00.123456"
  },
  {
    "name": "Data Scientist",
    "normalized_name": "Data Scientist",
    "required_skills": ["Python", "TensorFlow", "Pandas"],
    "demand_trend": "increasing",
    "last_updated": "2024-01-15T10:30:00.123456"
  },
  {
    "name": "DevOps Engineer",
    "normalized_name": "DevOps Engineer",
    "required_skills": ["Kubernetes", "Docker", "AWS"],
    "demand_trend": "stable",
    "last_updated": "2024-01-15T10:30:00.123456"
  }
]
```

#### Test Examples

```bash
# Get all role trends
curl -X GET http://localhost:8000/roles/trends
```

#### Python Example

```python
import requests

response = requests.get("http://localhost:8000/roles/trends")
roles = response.json()

for role in roles:
    print(f"{role['name']}: {len(role['required_skills'])} skills")
    print(f"  Skills: {', '.join(role['required_skills'])}")
    print(f"  Trend: {role['demand_trend']}\n")
```

---

### 7. Trigger Pipeline

**POST** `/pipeline/run`

Manually trigger the daily data pipeline.

#### Response Example

```json
{
  "status": "running",
  "started_at": "2024-01-15T10:30:00.123456",
  "completed_at": null,
  "records_processed": 0,
  "errors": []
}
```

#### Test Examples

```bash
# Trigger pipeline
curl -X POST http://localhost:8000/pipeline/run
```

#### Python Example

```python
import requests
import time

# Trigger pipeline
response = requests.post("http://localhost:8000/pipeline/run")
result = response.json()
print(f"Pipeline status: {result['status']}")

# Wait and check status
time.sleep(5)
status_response = requests.get("http://localhost:8000/pipeline/status")
status = status_response.json()
print(f"Current status: {status['status']}")
```

---

### 8. Get Pipeline Status

**GET** `/pipeline/status`

Get current pipeline execution status.

#### Response Example

```json
{
  "status": "completed",
  "started_at": "2024-01-15T10:30:00.123456",
  "completed_at": "2024-01-15T10:35:15.789012",
  "records_processed": 1250,
  "errors": []
}
```

#### Possible Status Values

- `idle` - Pipeline not running
- `running` - Pipeline currently executing
- `completed` - Pipeline finished successfully
- `failed` - Pipeline encountered errors

#### Test Examples

```bash
# Get pipeline status
curl -X GET http://localhost:8000/pipeline/status
```

#### Python Example

```python
import requests

response = requests.get("http://localhost:8000/pipeline/status")
status = response.json()

print(f"Status: {status['status']}")
if status['completed_at']:
    print(f"Completed: {status['completed_at']}")
    print(f"Records processed: {status['records_processed']}")
if status['errors']:
    print(f"Errors: {status['errors']}")
```

---

## Complete Testing Script

### Python Test Script

Save as `test_api.py`:

```python
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
```

### Bash Test Script

Save as `test_api.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "=========================================="
echo "API Testing Suite"
echo "=========================================="

# Test Health
echo -e "\n[1] Testing Health Endpoint"
curl -s -X GET "$BASE_URL/health" | jq '.'

# Test Get All Skills
echo -e "\n[2] Testing Get All Skills"
curl -s -X GET "$BASE_URL/skills?limit=5" | jq 'length'

# Test High-Risk Skills
echo -e "\n[3] Testing High-Risk Skills"
curl -s -X GET "$BASE_URL/skills/high-risk?limit=5" | jq 'length'

# Test Emerging Skills
echo -e "\n[4] Testing Emerging Skills"
curl -s -X GET "$BASE_URL/skills/emerging?limit=5" | jq 'length'

# Test Role Trends
echo -e "\n[5] Testing Role Trends"
curl -s -X GET "$BASE_URL/roles/trends" | jq 'length'

# Test Pipeline Status
echo -e "\n[6] Testing Pipeline Status"
curl -s -X GET "$BASE_URL/pipeline/status" | jq '.'

# Test Trigger Pipeline (commented out to avoid running)
# echo -e "\n[7] Testing Trigger Pipeline"
# curl -s -X POST "$BASE_URL/pipeline/run" | jq '.'

echo -e "\n=========================================="
echo "Testing Complete"
echo "=========================================="
```

---

## Error Responses

All endpoints may return the following error responses:

### 404 Not Found

```json
{
  "detail": "Skill 'NonExistentSkill' not found"
}
```

### 409 Conflict

```json
{
  "detail": "Pipeline is already running"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Error processing skill data"
}
```

---

## Quick Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/skills` | Get all skills |
| GET | `/skills/{skill_name}` | Get skill detail |
| GET | `/skills/high-risk` | Get high-risk skills |
| GET | `/skills/emerging` | Get emerging skills |
| GET | `/roles/trends` | Get role trends |
| POST | `/pipeline/run` | Trigger pipeline |
| GET | `/pipeline/status` | Get pipeline status |

---

## Notes

1. **First Run**: If no data exists, run the pipeline first:
   ```bash
   curl -X POST http://localhost:8000/pipeline/run
   ```

2. **Data Availability**: Some endpoints may return empty arrays if the pipeline hasn't run yet.

3. **Rate Limiting**: The API doesn't implement rate limiting in the current version, but data sources have built-in rate limiting.

4. **CORS**: The API is configured to accept requests from `http://localhost:5173` (frontend).

