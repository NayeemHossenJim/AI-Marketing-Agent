from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator

class CampaignCreate(BaseModel):
    campaign_name: str = Field(min_length=2, max_length=120)
    prompt: str = Field(min_length=3)
    phone: str = Field(min_length=6, max_length=20)
    schedule_time: datetime

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        phone = value.strip()
        allowed = phone.startswith("+") and phone[1:].isdigit() or phone.isdigit()
        if not allowed:
            raise ValueError("Phone number must contain digits and optional leading +")
        return phone

class CampaignResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    campaign_name: str
    prompt: str
    phone: str
    schedule_time: datetime
    generated_text: str | None
    generated_image_url: str | None
    status: str
    error_message: str | None
    created_at: datetime
    sent_at: datetime | None