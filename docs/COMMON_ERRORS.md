# Common Errors and Solutions

## "Method Not Allowed" Error

### Problem
You're getting a `{"detail": "Method Not Allowed"}` error when calling an API endpoint.

### Solution
Make sure you're using the correct HTTP method for each endpoint:

### Correct HTTP Methods

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | **GET** | Health check |
| `/skills` | **GET** | Get all skills |
| `/skills/{skill_name}` | **GET** | Get skill detail |
| `/skills/high-risk` | **GET** | Get high-risk skills |
| `/skills/emerging` | **GET** | Get emerging skills |
| `/roles/trends` | **GET** | Get role trends |
| `/pipeline/run` | **POST** | Trigger pipeline |
| `/pipeline/status` | **GET** | Get pipeline status |

### Common Mistakes

❌ **Wrong:**
```bash
# Trying to POST to status endpoint
curl -X POST http://localhost:8000/pipeline/status
```

✅ **Correct:**
```bash
# Use GET for status
curl -X GET http://localhost:8000/pipeline/status
# or simply
curl http://localhost:8000/pipeline/status
```

❌ **Wrong:**
```bash
# Trying to GET to run endpoint
curl http://localhost:8000/pipeline/run
```

✅ **Correct:**
```bash
# Use POST for run
curl -X POST http://localhost:8000/pipeline/run
```

### Quick Test Commands

```bash
# Health check (GET)
curl http://localhost:8000/health

# Get skills (GET)
curl http://localhost:8000/skills?limit=5

# Trigger pipeline (POST)
curl -X POST http://localhost:8000/pipeline/run

# Check pipeline status (GET)
curl http://localhost:8000/pipeline/status
```

---

## Pipeline Status: "running" but No Completion

### Problem
Pipeline shows status "running" but never completes or shows errors.

### Solution

1. **Wait a bit** - The pipeline may still be processing
2. **Check the status again:**
   ```bash
   curl http://localhost:8000/pipeline/status
   ```

3. **Check backend logs** - Look for error messages in the terminal where you started the backend

4. **If stuck in "running" state**, you may need to restart the backend server

---

## Empty Results from Skills Endpoints

### Problem
Getting empty arrays `[]` from skills endpoints.

### Solution

1. **Run the pipeline first:**
   ```bash
   curl -X POST http://localhost:8000/pipeline/run
   ```

2. **Wait for completion** (check status)

3. **Then query skills:**
   ```bash
   curl http://localhost:8000/skills
   ```

---

## Date Format Errors

### Problem
Getting date parsing errors in the pipeline.

### Solution
This should be fixed in the latest code. If you still see date errors:

1. **Delete old CSV files** (they may have incompatible formats):
   ```bash
   # On Windows PowerShell
   Remove-Item backend\data\processed\*.csv
   ```

2. **Run pipeline again:**
   ```bash
   curl -X POST http://localhost:8000/pipeline/run
   ```

---

## CORS Errors in Frontend

### Problem
Frontend can't connect to backend API.

### Solution

1. **Check backend is running** on `http://localhost:8000`

2. **Check CORS settings** in `backend/app/config.py`:
   ```python
   CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
   ```

3. **Verify frontend API URL** in `frontend/src/services/api.js`:
   ```javascript
   const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
   ```

---

## Module Import Errors

### Problem
Getting `ModuleNotFoundError` or import errors.

### Solution

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Install spaCy model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Check Python path** - Make sure you're running from the correct directory

---

## Port Already in Use

### Problem
Error: "Address already in use" when starting the backend.

### Solution

1. **Find and kill the process:**
   ```bash
   # On Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```

2. **Or use a different port:**
   ```bash
   uvicorn app.main:app --port 8001
   ```

---

## Need More Help?

1. **Check the logs** - Backend logs will show detailed error messages
2. **Use Swagger UI** - Visit `http://localhost:8000/docs` for interactive API testing
3. **Check the API Testing Guide** - See `docs/API_TESTING_GUIDE.md`



