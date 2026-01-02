"""
Roles API endpoints.
"""
from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from loguru import logger

from app.models import Role

router = APIRouter()


@router.get("/trends", response_model=List[Role])
async def get_role_trends():
    """Get role trends and required skills."""
    # This would load from processed role data
    # For now, return mock data
    logger.info("Fetching role trends")
    
    # Mock implementation - replace with actual data loading
    roles = [
        Role(
            name="Software Engineer",
            normalized_name="Software Engineer",
            required_skills=["Python", "JavaScript", "Git"],
            demand_trend="increasing",
            last_updated=datetime.now()
        ),
        Role(
            name="Data Scientist",
            normalized_name="Data Scientist",
            required_skills=["Python", "TensorFlow", "Pandas"],
            demand_trend="increasing",
            last_updated=datetime.now()
        ),
        Role(
            name="DevOps Engineer",
            normalized_name="DevOps Engineer",
            required_skills=["Kubernetes", "Docker", "AWS"],
            demand_trend="stable",
            last_updated=datetime.now()
        )
    ]
    
    return roles

