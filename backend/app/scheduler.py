"""
Scheduler for running the daily pipeline automatically.
"""
import schedule
import time
import asyncio
from loguru import logger
from app.pipeline.daily_pipeline import DailyPipeline
from app.config import settings


async def run_scheduled_pipeline():
    """Run the pipeline asynchronously."""
    pipeline = DailyPipeline()
    result = await pipeline.run()
    logger.info(f"Scheduled pipeline completed: {result['status']}")


def scheduled_job():
    """Wrapper for scheduled job."""
    asyncio.run(run_scheduled_pipeline())


def start_scheduler():
    """Start the scheduler."""
    # Schedule daily pipeline
    schedule.every().day.at(f"{settings.PIPELINE_SCHEDULE_HOUR:02d}:00").do(scheduled_job)
    
    logger.info(f"Scheduler started. Pipeline will run daily at {settings.PIPELINE_SCHEDULE_HOUR:02d}:00")
    
    # Run scheduler loop
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    start_scheduler()



