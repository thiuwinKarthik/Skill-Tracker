#!/usr/bin/env python3
"""
Check if data files exist and diagnose empty responses
"""
import os
from pathlib import Path

# Check data directories
raw_dir = Path("backend/data/raw")
processed_dir = Path("backend/data/processed")

print("=" * 60)
print("DATA FILES DIAGNOSTIC")
print("=" * 60)

# Check raw data
print("\n📁 Raw Data Directory:")
print(f"   Path: {raw_dir.absolute()}")
print(f"   Exists: {raw_dir.exists()}")
if raw_dir.exists():
    raw_files = list(raw_dir.glob("*.json"))
    print(f"   Files found: {len(raw_files)}")
    for f in raw_files[:5]:  # Show first 5
        print(f"   - {f.name} ({f.stat().st_size} bytes)")
    if len(raw_files) > 5:
        print(f"   ... and {len(raw_files) - 5} more")

# Check processed data
print("\n📁 Processed Data Directory:")
print(f"   Path: {processed_dir.absolute()}")
print(f"   Exists: {processed_dir.exists()}")
if processed_dir.exists():
    processed_files = list(processed_dir.glob("processed_skills_*.csv"))
    print(f"   Processed CSV files found: {len(processed_files)}")
    for f in processed_files[:5]:  # Show first 5
        size = f.stat().st_size
        print(f"   - {f.name} ({size} bytes)")
        if size > 0:
            # Try to read first few lines
            try:
                import pandas as pd
                df = pd.read_csv(f)
                print(f"     Rows: {len(df)}, Columns: {df.columns.tolist()}")
            except Exception as e:
                print(f"     Error reading: {e}")
    if len(processed_files) > 5:
        print(f"   ... and {len(processed_files) - 5} more")
    
    # Check historical data
    historical_file = processed_dir / "historical_skills.csv"
    print(f"\n   Historical data file: {historical_file.name}")
    print(f"   Exists: {historical_file.exists()}")
    if historical_file.exists():
        size = historical_file.stat().st_size
        print(f"   Size: {size} bytes")
        if size > 0:
            try:
                import pandas as pd
                df = pd.read_csv(historical_file)
                print(f"   Rows: {len(df)}, Columns: {df.columns.tolist()}")
            except Exception as e:
                print(f"   Error reading: {e}")

print("\n" + "=" * 60)
print("DIAGNOSIS")
print("=" * 60)

if not processed_dir.exists() or len(list(processed_dir.glob("processed_skills_*.csv"))) == 0:
    print("❌ No processed data files found!")
    print("\n💡 Solution:")
    print("   1. Run the pipeline:")
    print("      curl -X POST http://localhost:8000/pipeline/run")
    print("   2. Wait for completion, then check status:")
    print("      curl http://localhost:8000/pipeline/status")
    print("   3. Or generate sample data:")
    print("      python scripts/generate_sample_data.py")
else:
    print("✅ Processed data files found")
    print("\n💡 If endpoints still return empty arrays:")
    print("   1. Check the CSV file has data (rows > 0)")
    print("   2. Verify the 'skill' column exists")
    print("   3. Check backend logs for errors")
