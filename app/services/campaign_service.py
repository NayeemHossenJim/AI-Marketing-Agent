from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate
from app.services.sms_sender import ConsoleSmsSender
from app.services.image_generator import ImageUrlGenerator
from app.services.text_generator import GroqMarketingTextGenerator
from app.repositories.campaign_repository import CampaignRepository

class CampaignService:
    def __init__(
        self,
        repository: CampaignRepository,
        text_generator: GroqMarketingTextGenerator,
        image_generator: ImageUrlGenerator,
        sms_sender: ConsoleSmsSender,
    ):
        self.repository = repository
        self.text_generator = text_generator
        self.image_generator = image_generator
        self.sms_sender = sms_sender

    def create_campaign(self, payload: CampaignCreate) -> Campaign:
        return self.repository.create(payload)

    def list_campaigns(self) -> list[Campaign]:
        return self.repository.list_all()

    def get_campaign(self, campaign_id: int) -> Campaign:
        campaign = self.repository.get(campaign_id)
        if not campaign:
            raise LookupError("Campaign not found")
        return campaign

    def send_campaign(self, campaign: Campaign) -> Campaign:
        try:
            text = self.text_generator.generate(campaign.prompt)
            image_url = self.image_generator.generate(campaign.prompt)
            self.sms_sender.send(campaign.phone, campaign.campaign_name, text, image_url)
            return self.repository.mark_sent(campaign, text, image_url)
        except Exception as exc:
            return self.repository.mark_failed(campaign, str(exc))

    def send_now(self, campaign_id: int) -> Campaign:
        campaign = self.get_campaign(campaign_id)
        if campaign.status == "sent":
            return campaign
        return self.send_campaign(campaign)