from datetime import datetime
from sqlalchemy.orm import Session
from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate

class CampaignRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: CampaignCreate) -> Campaign:
        campaign = Campaign(**payload.model_dump(), status="pending")
        self.db.add(campaign)
        self.db.commit()
        self.db.refresh(campaign)
        return campaign

    def list_all(self) -> list[Campaign]:
        return self.db.query(Campaign).order_by(Campaign.schedule_time.desc()).all()

    def get(self, campaign_id: int) -> Campaign | None:
        return self.db.query(Campaign).filter(Campaign.id == campaign_id).first()

    def get_due_campaigns(self, now: datetime) -> list[Campaign]:
        return (
            self.db.query(Campaign)
            .filter(Campaign.status == "pending", Campaign.schedule_time <= now)
            .order_by(Campaign.schedule_time.asc())
            .all()
        )

    def mark_sent(self, campaign: Campaign, text: str, image_url: str) -> Campaign:
        campaign.status = "sent"
        campaign.generated_text = text
        campaign.generated_image_url = image_url
        campaign.sent_at = datetime.now()
        campaign.error_message = None
        self.db.commit()
        self.db.refresh(campaign)
        return campaign

    def mark_failed(self, campaign: Campaign, error: str) -> Campaign:
        campaign.status = "failed"
        campaign.error_message = error
        self.db.commit()
        self.db.refresh(campaign)
        return campaign