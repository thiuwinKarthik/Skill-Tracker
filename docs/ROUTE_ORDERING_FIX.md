# Route Ordering Fix - 405 Method Not Allowed

## Problem

Getting `405 Method Not Allowed` errors when accessing endpoints like `/skills/high-risk` or `/skills/emerging`.

## Root Cause

In FastAPI, **route order matters**. When you have both:
- Specific routes: `/high-risk`, `/emerging`
- Parameterized routes: `/{skill_name}`

The parameterized route will match **first** if it's defined before the specific routes. This causes FastAPI to try to match `/high-risk` as a skill name parameter, leading to routing conflicts.

## Solution

**Specific routes must come BEFORE parameterized routes.**

### Before (Wrong Order):
```python
@router.get("")                    # 1. Base route
@router.get("/{skill_name}")       # 2. Parameterized - matches everything!
@router.get("/high-risk")         # 3. Never reached - 405 error
@router.get("/emerging")          # 4. Never reached - 405 error
```

### After (Correct Order):
```python
@router.get("")                   # 1. Base route
@router.get("/high-risk")         # 2. Specific route - matches first
@router.get("/emerging")          # 3. Specific route - matches first
@router.get("/{skill_name}")      # 4. Parameterized - matches last (catch-all)
```

## Fixed Files

- `backend/app/api/skills.py` - Reordered routes

## Testing

After restarting the backend, test these endpoints:

```bash
# Should work now
curl http://localhost:8000/skills/high-risk
curl http://localhost:8000/skills/emerging
curl http://localhost:8000/skills/React
```

## Important Notes

1. **Restart the backend** after making this change
2. FastAPI matches routes in the order they're defined
3. Always put specific routes before parameterized routes
4. Use the debug script: `python debug_api.py` to test all endpoints

