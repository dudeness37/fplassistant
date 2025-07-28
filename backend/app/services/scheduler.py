from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
import asyncio

scheduler = AsyncIOScheduler(timezone="Europe/Madrid")

async def sample_job():
    logger.info("Sample scheduled job ran.")

def start_scheduler():
    scheduler.add_job(sample_job, "interval", seconds=60)  # placeholder
    scheduler.start()
    logger.info("Scheduler started.")
    # Keep scheduler alive in uvicorn event loop
    asyncio.get_event_loop().create_task(asyncio.sleep(0))
