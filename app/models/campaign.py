from app.database import Base
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    campaign_name = Column(String(120), nullable=False)
    prompt = Column(Text, nullable=False)
    phone = Column(String(20), nullable=False)
    schedule_time = Column(DateTime, nullable=False, index=True)
    generated_text = Column(Text, nullable=True)
    generated_image_url = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="pending", index=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    sent_at = Column(DateTime, nullable=True)