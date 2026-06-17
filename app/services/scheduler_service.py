import logging
import asyncio
from datetime import datetime
from app.core.config import settings
from app.database import SessionLocal
from app.services.sms_sender import ConsoleSmsSender
from app.services.campaign_service import CampaignService
from app.services.image_generator import ImageUrlGenerator
from app.services.text_generator import GroqMarketingTextGenerator
from app.repositories.campaign_repository import CampaignRepository

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self):
        self.interval_seconds = settings.scheduler_interval_seconds
        self.task: asyncio.Task | None = None
        self.running = False

    async def start(self) -> None:
        if self.task:
            return
        self.running = True
        self.task = asyncio.create_task(self.run())
        logger.info("Scheduler started")

    async def stop(self) -> None:
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        logger.info("Scheduler stopped")

    async def run(self) -> None:
        while self.running:
            try:
                await asyncio.to_thread(self.check_campaigns)
            except Exception:
                logger.exception("Scheduler check failed")
            await asyncio.sleep(self.interval_seconds)

    def check_campaigns(self) -> None:
        db = SessionLocal()
        try:
            repository = CampaignRepository(db)
            service = CampaignService(
                repository,
                GroqMarketingTextGenerator(),
                ImageUrlGenerator(),
                ConsoleSmsSender(),
            )
            campaigns = repository.get_due_campaigns(datetime.now())
            for campaign in campaigns:
                service.send_campaign(campaign)
        finally:
            db.close()