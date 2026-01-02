"""
Data models for the application.
"""
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime


class Skill(BaseModel):
    """Skill data model."""
    name: str
    normalized_name: str
    current_demand: float
    forecast_demand: float
    risk_score: float
    risk_category: str
    trend: str  # "increasing", "decreasing", "stable"
    last_updated: datetime


class SkillDetail(Skill):
    """Extended skill model with additional details."""
    job_posting_growth: float
    github_velocity: float
    community_mentions: float
    research_citations: float
    related_skills: List[str]
    historical_data: List[Dict[str, float]]
    description: Optional[str] = None
    category: Optional[str] = None
    popularity: Optional[str] = None
    trend_info: Optional[str] = None


class Role(BaseModel):
    """Role data model."""
    name: str
    normalized_name: str
    required_skills: List[str]
    demand_trend: str
    last_updated: datetime


class PipelineStatus(BaseModel):
    """Pipeline execution status."""
    status: str  # "running", "completed", "failed"
    started_at: datetime
    completed_at: Optional[datetime]
    records_processed: int
    errors: List[str]


class HealthCheck(BaseModel):
    """Health check response."""
    status: str
    timestamp: datetime
    version: str

