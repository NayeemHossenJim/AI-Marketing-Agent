from fastapi import FastAPI
from app.models import campaign
from app.core.config import settings
from app.database import create_tables
from app.core.logger import setup_logger
from contextlib import asynccontextmanager
from app.services.scheduler_service import SchedulerService
from app.api.campaign_routes import router as campaign_router

setup_logger()
scheduler = SchedulerService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    await scheduler.start()
    yield
    await scheduler.stop()

app = FastAPI(title=settings.app_name, lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(campaign_router)