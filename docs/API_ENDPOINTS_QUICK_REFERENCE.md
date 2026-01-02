# API Endpoints Quick Reference

## Base URL
```
http://localhost:8000
```

## All Endpoints

**⚠️ IMPORTANT: Use the correct HTTP method (GET or POST) for each endpoint!**

### 1. Health Check
```
GET /health
```
**Method: GET** ✅
**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456",
  "version": "1.0.0"
}
```

---

### 2. Get All Skills
```
GET /skills?limit=10&min_risk=0.5&max_risk=0.8
```
**Method: GET** ✅
**Query Params:**
- `limit` (int, 1-1000): Limit results
- `min_risk` (float, 0.0-1.0): Minimum risk score
- `max_risk` (float, 0.0-1.0): Maximum risk score

**Response:**
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
  }
]
```

---

### 3. Get Skill Detail
```
GET /skills/{skill_name}
```
**Method: GET** ✅
**Path Param:**
- `skill_name` (string): Name of the skill

**Response:**
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
  "related_skills": ["JavaScript", "TypeScript"],
  "historical_data": []
}
```

---

### 4. Get High-Risk Skills
```
GET /skills/high-risk?limit=10
```
**Method: GET** ✅
**Query Params:**
- `limit` (int, 1-100, default: 10): Limit results

**Response:**
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
  }
]
```

---

### 5. Get Emerging Skills
```
GET /skills/emerging?limit=10
```
**Method: GET** ✅
**Query Params:**
- `limit` (int, 1-100, default: 10): Limit results

**Response:**
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
  }
]
```

---

### 6. Get Role Trends
```
GET /roles/trends
```
**Method: GET** ✅
**Response:**
```json
[
  {
    "name": "Software Engineer",
    "normalized_name": "Software Engineer",
    "required_skills": ["Python", "JavaScript", "Git"],
    "demand_trend": "increasing",
    "last_updated": "2024-01-15T10:30:00.123456"
  }
]
```

---

### 7. Trigger Pipeline
```
POST /pipeline/run
```
**Method: POST** ✅ (NOT GET!)
**Response:**
```json
{
  "status": "running",
  "started_at": "2024-01-15T10:30:00.123456",
  "completed_at": null,
  "records_processed": 0,
  "errors": []
}
```

---

### 8. Get Pipeline Status
```
GET /pipeline/status
```
**Method: GET** ✅ (NOT POST!)
**Response:**
```json
{
  "status": "completed",
  "started_at": "2024-01-15T10:30:00.123456",
  "completed_at": "2024-01-15T10:35:15.789012",
  "records_processed": 1250,
  "errors": []
}
```

**Status Values:**
- `idle` - Not running
- `running` - Currently executing
- `completed` - Finished successfully
- `failed` - Encountered errors

---

## Quick Test Commands

```bash
# Health check
curl http://localhost:8000/health

# Get all skills
curl "http://localhost:8000/skills?limit=10"

# Get skill detail
curl http://localhost:8000/skills/React

# High-risk skills
curl "http://localhost:8000/skills/high-risk?limit=10"

# Emerging skills
curl "http://localhost:8000/skills/emerging?limit=10"

# Role trends
curl http://localhost:8000/roles/trends

# Pipeline status
curl http://localhost:8000/pipeline/status

# Trigger pipeline
curl -X POST http://localhost:8000/pipeline/run
```

---

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

