# Future Skill & Tech-Stack Obsolescence Predictor

A production-grade system that continuously ingests real-world technology signals, extracts skills using NLP, forecasts future demand using ML, and computes obsolescence risk scores.

## 🏗️ Architecture

```
Web Sources → Daily Pipeline → NLP Extraction → Feature Engineering → ML Models → FastAPI → React Dashboard
```

## 📁 Project Structure

```
Future_Skill_Obsolescence_Predictor/
├── frontend/        # React (Vite)
├── backend/         # FastAPI + ML
├── experiments/     # Model experiments
├── docs/            # Architecture & API docs
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Docker & Docker Compose (optional)

### Local Development

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --port 8000
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Docker Deployment

```bash
docker-compose up --build
```

## 📊 Features

- **Data Ingestion**: Automated daily pipeline from multiple sources
- **NLP Extraction**: Skill and role extraction using spaCy
- **ML Forecasting**: ARIMA/Prophet models for demand prediction
- **Risk Classification**: Obsolescence risk scoring (0-1)
- **REST APIs**: FastAPI endpoints for data access
- **Interactive Dashboard**: React frontend with visualizations

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

- API keys for data sources
- Database connections
- Model parameters

## 📝 API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Running the Pipeline

```bash
# Manual trigger
curl -X POST http://localhost:8000/pipeline/run

# Or via Python
python -m backend.app.pipeline.daily_pipeline
```

## 📈 Evaluation Metrics

- Trend accuracy
- Forecast error (MAE, RMSE)
- Risk score consistency
- Historical backtesting

## ⚠️ Legal & Ethical

- Respects robots.txt
- Rate-limited scraping
- Uses official APIs when available
- Stores only metadata (no personal data)

## 📄 License

MIT



