"""
Health check endpoint.
"""
from fastapi import APIRouter
from datetime import datetime
from app.models import HealthCheck

router = APIRouter()


@router.get("", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )

