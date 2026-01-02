"""
FastAPI main application entry point.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import uvicorn

from app.api import skills, roles, pipeline, health
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    # Startup
    logger.info("Starting Future Skill Obsolescence Predictor API")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    yield
    # Shutdown
    logger.info("Shutting down API")


# Initialize FastAPI app
app = FastAPI(
    title="Future Skill Obsolescence Predictor API",
    description="API for skill demand forecasting and obsolescence risk prediction",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(skills.router, prefix="/skills", tags=["Skills"])
app.include_router(roles.router, prefix="/roles", tags=["Roles"])
app.include_router(pipeline.router, prefix="/pipeline", tags=["Pipeline"])


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

