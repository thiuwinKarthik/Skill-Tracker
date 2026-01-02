# Bug Fixes

## Date Format Parsing Error

### Issue
Pipeline was failing with error: "time data \"2026-01-02\" doesn't match format \"%Y-%m-%d %H:%M:%S\""

### Root Cause
When loading historical data from CSV, pandas was trying to parse date strings with a specific format that didn't match the actual date format in the file (date-only vs datetime).

### Fix Applied

**Changed `_load_historical_data()` in `backend/app/pipeline/daily_pipeline.py`:**
- Removed explicit format specification
- Now uses `pd.to_datetime()` with `errors='coerce'` to automatically detect date formats
- This handles both date-only strings (YYYY-MM-DD) and datetime strings

**Before:**
```python
df = pd.read_csv(historical_file, parse_dates=['date'])
df['date'] = pd.to_datetime(df['date'])
```

**After:**
```python
df = pd.read_csv(historical_file)
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])
```

**Changed `_save_historical_data()`:**
- Added proper datetime type checking before formatting
- Ensures dates are saved in consistent YYYY-MM-DD format

---

## DateTime/Timestamp Comparison Error

### Issue
Pipeline was failing with error: "cannot compare timestamp with date time"

### Root Cause
The code was mixing Python's `datetime.date` objects with pandas `Timestamp` objects, causing type mismatch errors when:
1. Loading historical data (pandas converts dates to Timestamp)
2. Adding new data (using Python date objects)
3. Comparing dates in feature engineering

### Fix Applied

#### 1. `backend/app/pipeline/daily_pipeline.py`

**Changed:**
- `_load_historical_data()`: Now ensures date column is always `pd.Timestamp` type
- `_update_historical_data()`: Uses `pd.Timestamp.now().normalize()` instead of `datetime.now().date()`
- Added explicit type conversion with `pd.to_datetime()` for consistency

**Before:**
```python
today = datetime.now().date()  # Python date object
```

**After:**
```python
today = pd.Timestamp.now().normalize()  # pandas Timestamp
new_df['date'] = pd.to_datetime(new_df['date'])  # Ensure type consistency
```

#### 2. `backend/app/ml/feature_engineering.py`

**Changed:**
- `_calculate_skill_features()`: Ensures date column is Timestamp before operations
- Fixed date comparison to use `pd.Timestamp` consistently
- Added proper handling for date differences

**Before:**
```python
recent_cutoff = datetime.now().date() - timedelta(days=30)
recent_data = skill_data[skill_data['date'] >= pd.Timestamp(recent_cutoff)]
```

**After:**
```python
skill_data['date'] = pd.to_datetime(skill_data['date'])
recent_cutoff = pd.Timestamp.now().normalize() - timedelta(days=30)
recent_data = skill_data[skill_data['date'] >= recent_cutoff]
```

#### 3. `backend/app/api/pipeline.py`

**Changed:**
- Added better error handling for datetime conversion in pipeline status

### Testing

After applying the fix, test the pipeline:

```bash
# Trigger pipeline
curl -X POST http://localhost:8000/pipeline/run

# Check status
curl http://localhost:8000/pipeline/status
```

The pipeline should now complete successfully without datetime comparison errors.

