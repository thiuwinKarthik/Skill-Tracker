"""
Pipeline control endpoints.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from datetime import datetime
from loguru import logger
import asyncio

from app.models import PipelineStatus
from app.pipeline.daily_pipeline import DailyPipeline

router = APIRouter()

# Global state to track pipeline execution
pipeline_status = {
    "status": "idle",
    "started_at": None,
    "completed_at": None,
    "records_processed": 0,
    "errors": []
}


async def run_pipeline_background():
    """Run pipeline in background."""
    global pipeline_status
    
    pipeline_status["status"] = "running"
    pipeline_status["started_at"] = datetime.now()
    pipeline_status["errors"] = []
    
    try:
        pipeline = DailyPipeline()
        result = await pipeline.run()
        
        pipeline_status["status"] = result["status"]
        # Handle completed_at - it might be None or a string
        completed_at_str = result.get("completed_at")
        if completed_at_str:
            try:
                pipeline_status["completed_at"] = datetime.fromisoformat(completed_at_str)
            except (ValueError, TypeError):
                # If it's already a datetime object or invalid format
                pipeline_status["completed_at"] = datetime.now()
        else:
            pipeline_status["completed_at"] = None
        pipeline_status["records_processed"] = result.get("records_processed", 0)
        pipeline_status["errors"] = result.get("errors", [])
        
        logger.info(f"Pipeline completed: {result['status']}")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        pipeline_status["status"] = "failed"
        pipeline_status["completed_at"] = datetime.now()
        pipeline_status["errors"] = [str(e)]


@router.post("/run", response_model=PipelineStatus)
async def trigger_pipeline(background_tasks: BackgroundTasks):
    """Manually trigger the daily pipeline."""
    global pipeline_status
    
    if pipeline_status["status"] == "running":
        raise HTTPException(
            status_code=409,
            detail="Pipeline is already running"
        )
    
    # Run pipeline in background
    background_tasks.add_task(run_pipeline_background)
    
    return PipelineStatus(
        status="running",
        started_at=datetime.now(),
        completed_at=None,
        records_processed=0,
        errors=[]
    )


@router.get("/status", response_model=PipelineStatus)
async def get_pipeline_status():
    """Get current pipeline execution status."""
    global pipeline_status
    
    return PipelineStatus(
        status=pipeline_status["status"],
        started_at=pipeline_status["started_at"],
        completed_at=pipeline_status["completed_at"],
        records_processed=pipeline_status["records_processed"],
        errors=pipeline_status["errors"]
    )

