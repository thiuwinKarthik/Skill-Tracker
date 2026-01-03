# Skill-Tracker — Project Overview

This document explains the overall workflow, modules, and tech stack of the Skill-Tracker project.

## Summary

Skill-Tracker is a full-stack application that ingests raw signals (job postings, GitHub activity, research citations), processes and stores processed skill-level data, trains forecasting and risk models, exposes REST APIs for a frontend dashboard, and provides scripts for local testing and data generation.

## Tech Stack

- Backend: Python, FastAPI, Uvicorn
- Data & ML: pandas, numpy, scikit-learn, statsmodels, Prophet, TensorFlow
- NLP: spaCy
- Web scraping / HTTP: requests, aiohttp, beautifulsoup4
- Task/scheduling: schedule
- Logging: loguru
- Frontend: React, Vite, Recharts, Axios
- Dev tooling: ESLint, Vite, git

## Repository Layout (key folders/files)

- `backend/` — FastAPI backend and ML code
  - `app/main.py` — FastAPI app entrypoint (routes mounted here)
  - `app/api/` — REST endpoint implementations (`health.py`, `pipeline.py`, `skills.py`, `roles.py`)
  - `app/ml/` — Model code: `feature_engineering.py`, `forecaster.py`, `risk_classifier.py`
  - `app/nlp/extractor.py` — text processing helpers
  - `app/pipeline/` — `daily_pipeline.py` & data source connectors
  - `data/processed/` — processed CSVs consumed by the API
  - `requirements.txt` — Python dependencies

- `frontend/` — React single-page app
  - `src/pages/` — page components (`Dashboard.jsx`, `Skills.jsx`, `SkillDetail.jsx`, etc.)
  - `src/components/` — UI components (`Card.jsx`, `SkillCard.jsx`, `Loading.jsx`, `Error.jsx`)
  - `src/services/api.js` — Axios wrapper for backend endpoints
  - `package.json` — frontend dependencies and scripts

- `scripts/` — utility scripts: `generate_sample_data.py`, `check_data.py`, `debug_api.py`, `test_api.py`
- `docs/` — design notes, endpoint guides and fixes

## High-level Workflow

1. Data ingestion: connectors in `app/pipeline/data_sources.py` collect raw data (job postings, GitHub, research sources).
2. Feature engineering: `app/ml/feature_engineering.py` transforms raw signals into skill-level features (demand, velocity, volatility).
3. Modeling:
   - Forecasting: `app/ml/forecaster.py` produces demand forecasts per skill (Prophet / statsmodels / TF models).
   - Risk classification: `app/ml/risk_classifier.py` computes a `risk_score` for each skill using engineered features and trained classifiers.
4. Pipeline: `app/pipeline/daily_pipeline.py` orchestrates ingestion, FE, model inference, and writes processed CSVs under `backend/data/processed/`.
5. Backend API: `app/api/*.py` exposes endpoints consumed by the frontend:
   - `/health` — health status
   - `/skills` — list skills (supports `limit`, filtering)
   - `/skills/high-risk` — top high-risk skills
   - `/skills/emerging` — top emerging skills
   - `/roles/trends` — role-level trends
   - `/pipeline/run` & `/pipeline/status` — trigger and check pipeline
6. Frontend: React app (`frontend/`) calls API via `src/services/api.js` to render the dashboard, charts, and skill cards.

## Module Responsibilities

- `app/main.py`: create FastAPI app, include routers, configure middleware, and start the server with Uvicorn.
- `app/api/health.py`: simple liveness/readiness and version info endpoint.
- `app/api/skills.py`: endpoints to list skills, get skill details, and compute top N high-risk/emerging skills.
- `app/api/pipeline.py`: endpoints to trigger the pipeline (background task) and return run status.
- `app/ml/feature_engineering.py`: functions to aggregate and compute numeric features used by ML models.
- `app/ml/forecaster.py`: forecast demand using historical time-series per skill. May use Prophet / statsmodels.
- `app/ml/risk_classifier.py`: load trained classifier, compute/predict `risk_score` from features.
- `app/nlp/extractor.py`: helper functions for extracting key phrases, mentions, and signals from text sources.
- `app/pipeline/daily_pipeline.py`: top-level pipeline that pulls sources, runs FE, models, and writes `processed_skills_*.csv` and `historical_skills.csv`.
- `frontend/src/services/api.js`: contains `getSkills()`, `getHighRiskSkills()`, `getEmergingSkills()`, `triggerPipeline()`, and `healthCheck()` used across the React pages.

## How to run locally (quickstart)

1. Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

2. Frontend

```powershell
cd frontend
npm install
npm run dev
```

3. Generate sample data (if pipeline not available)

```powershell
python scripts/generate_sample_data.py
```

4. Test API endpoints

```powershell
python scripts/debug_api.py
python scripts/test_api.py
```

## Notes & Recommendations

- Remove the committed `backend/venv` from the repo (done via `.gitignore`).
- Add `pre-commit` hooks for `black` (Python), `eslint --fix` (JS) to keep code style consistent.
- Add unit tests for critical ML functions and API endpoints. Presently testing is manual via `scripts/test_api.py`.
- Consider containerizing with Docker for reproducible runs.

If you want, I can create a condensed `README.md` with these instructions and add `CONTRIBUTING.md` and `DEVELOPER_SETUP.md`. Tell me which files to generate next.
