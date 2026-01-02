"""
Application configuration using Pydantic settings.
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # Environment
    ENVIRONMENT: str =  "development"
    DEBUG: bool = False
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Data paths
    DATA_RAW_DIR: str = "data/raw"
    DATA_PROCESSED_DIR: str = "data/processed"
    MODELS_DIR: str = "app/models"
    
    # NLP
    SPACY_MODEL: str = "en_core_web_sm"
    
    # ML
    FORECAST_HORIZON_DAYS: int = 90
    RISK_THRESHOLD_HIGH: float = 0.7
    RISK_THRESHOLD_LOW: float = 0.3
    
    # Data sources (API keys should be in .env)
    GITHUB_API_KEY: str = os.getenv("GITHUB_API_KEY", "")
    JOB_BOARD_API_KEY: str = os.getenv("JOB_BOARD_API_KEY", "")
    
    # Pipeline
    PIPELINE_SCHEDULE_HOUR: int = 2  # 2 AM daily
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

