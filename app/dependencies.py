from fastapi import Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.services.sms_sender import ConsoleSmsSender
from app.services.campaign_service import CampaignService
from app.services.image_generator import ImageUrlGenerator
from app.services.text_generator import GroqMarketingTextGenerator
from app.repositories.campaign_repository import CampaignRepository

def get_campaign_service(db: Session = Depends(get_db)) -> CampaignService:
    repository = CampaignRepository(db)
    return CampaignService(
        repository,
        GroqMarketingTextGenerator(),
        ImageUrlGenerator(),
        ConsoleSmsSender(),
    )