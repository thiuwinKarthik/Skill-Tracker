#!/bin/bash

BASE_URL="http://localhost:8000"

echo "=========================================="
echo "API Testing Suite"
echo "=========================================="

# Test Health
echo -e "\n[1] Testing Health Endpoint"
curl -s -X GET "$BASE_URL/health" | python -m json.tool

# Test Get All Skills
echo -e "\n[2] Testing Get All Skills (limit=5)"
curl -s -X GET "$BASE_URL/skills?limit=5" | python -m json.tool | head -20

# Test High-Risk Skills
echo -e "\n[3] Testing High-Risk Skills (limit=5)"
curl -s -X GET "$BASE_URL/skills/high-risk?limit=5" | python -m json.tool | head -20

# Test Emerging Skills
echo -e "\n[4] Testing Emerging Skills (limit=5)"
curl -s -X GET "$BASE_URL/skills/emerging?limit=5" | python -m json.tool | head -20

# Test Role Trends
echo -e "\n[5] Testing Role Trends"
curl -s -X GET "$BASE_URL/roles/trends" | python -m json.tool

# Test Pipeline Status
echo -e "\n[6] Testing Pipeline Status"
curl -s -X GET "$BASE_URL/pipeline/status" | python -m json.tool

# Test Trigger Pipeline (commented out to avoid running)
# echo -e "\n[7] Testing Trigger Pipeline"
# curl -s -X POST "$BASE_URL/pipeline/run" | python -m json.tool

echo -e "\n=========================================="
echo "Testing Complete"
echo "=========================================="
echo -e "\nNote: For full JSON output, use jq or python -m json.tool"
echo "Example: curl -s $BASE_URL/health | python -m json.tool"

