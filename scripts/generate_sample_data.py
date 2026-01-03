#!/usr/bin/env python3
"""
Generate sample data for testing when pipeline hasn't run yet
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
import random

# Sample skills data
sample_skills = [
    {"name": "React", "risk": 0.12, "growth": 25.5, "demand": 1250},
    {"name": "Angular", "risk": 0.78, "growth": -15.2, "demand": 850},
    {"name": "Vue.js", "risk": 0.35, "growth": 18.3, "demand": 720},
    {"name": "Python", "risk": 0.08, "growth": 32.1, "demand": 2100},
    {"name": "JavaScript", "risk": 0.15, "growth": 22.4, "demand": 1800},
    {"name": "TypeScript", "risk": 0.10, "growth": 28.7, "demand": 950},
    {"name": "Node.js", "risk": 0.20, "growth": 19.5, "demand": 1100},
    {"name": "Java", "risk": 0.45, "growth": 5.2, "demand": 1400},
    {"name": "Go", "risk": 0.25, "growth": 35.8, "demand": 680},
    {"name": "Rust", "risk": 0.18, "growth": 42.3, "demand": 450},
    {"name": "TensorFlow", "risk": 0.30, "growth": 15.6, "demand": 520},
    {"name": "PyTorch", "risk": 0.22, "growth": 28.9, "demand": 380},
    {"name": "Kubernetes", "risk": 0.12, "growth": 38.2, "demand": 890},
    {"name": "Docker", "risk": 0.15, "growth": 20.1, "demand": 1200},
    {"name": "AWS", "risk": 0.10, "growth": 25.3, "demand": 1500},
]

def generate_sample_data():
    """Generate sample processed data file"""
    processed_dir = Path("backend/data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Create processed skills data
    today = datetime.now().strftime("%Y%m%d")
    filename = f"processed_skills_{today}.csv"
    filepath = processed_dir / filename
    
    data = []
    for skill in sample_skills:
        data.append({
            'skill': skill['name'],
            'current_demand': skill['demand'],
            'forecast_demand': skill['demand'] * (1 + skill['growth'] / 100),
            'risk_score': skill['risk'],
            'risk_category': 'high' if skill['risk'] >= 0.7 else 'low' if skill['risk'] <= 0.3 else 'medium',
            'forecast_trend': 'increasing' if skill['growth'] > 10 else 'decreasing' if skill['growth'] < -10 else 'stable',
            'job_posting_growth': skill['growth'],
            'github_velocity': skill['growth'] * 0.8,
            'community_decay': -skill['growth'] * 0.5,
            'research_trend': skill['growth'] * 0.3,
            'recent_job_postings': skill['demand'] * 0.3,
            'recent_github_stars': skill['demand'] * 0.2,
            'job_volatility': skill['demand'] * 0.1,
            'days_observed': 90,
            'total_observations': 30,
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    print(f"✅ Generated sample data: {filepath}")
    print(f"   Skills: {len(df)}")
    print(f"   Columns: {df.columns.tolist()}")
    
    # Also create historical data
    historical_file = processed_dir / "historical_skills.csv"
    historical_data = []
    for skill in sample_skills:
        for day in range(30):  # 30 days of history
            date = datetime.now().date() - pd.Timedelta(days=30-day)
            historical_data.append({
                'skill': skill['name'],
                'date': date,
                'job_postings': skill['demand'] + random.randint(-50, 50),
                'github_stars': skill['demand'] * 0.5 + random.randint(-20, 20),
                'community_mentions': skill['demand'] * 0.3 + random.randint(-10, 10),
                'research_citations': skill['demand'] * 0.1 + random.randint(-5, 5),
            })
    
    hist_df = pd.DataFrame(historical_data)
    hist_df.to_csv(historical_file, index=False)
    print(f"\n✅ Generated historical data: {historical_file}")
    print(f"   Records: {len(hist_df)}")
    
    return filepath

if __name__ == "__main__":
    print("=" * 60)
    print("GENERATING SAMPLE DATA")
    print("=" * 60)
    generate_sample_data()
    print("\n" + "=" * 60)
    print("✅ Sample data generated!")
    print("=" * 60)
    print("\nNow test the API endpoints:")
    print("  curl http://localhost:8000/skills")
    print("  curl http://localhost:8000/skills/high-risk")
    print("  curl http://localhost:8000/skills/emerging")
