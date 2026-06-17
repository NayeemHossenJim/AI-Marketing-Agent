import logging
from groq import Groq
from app.core.config import settings

logger = logging.getLogger(__name__)

class MockMarketingTextGenerator:
    def generate(self, prompt: str) -> str:
        return f"Limited time offer: {prompt}. Contact us today and grab the opportunity."

class GroqMarketingTextGenerator:
    def __init__(self):
        self.fallback = MockMarketingTextGenerator()
        self.client = Groq(api_key=settings.groq_api_key) if settings.groq_api_key else None
        self.model = settings.groq_model

    def generate(self, prompt: str) -> str:
        if not self.client:
            return self.fallback.generate(prompt)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Write short, clear, SMS-friendly marketing copy. Keep it under 80 words.",
                    },
                    {
                        "role": "user",
                        "content": f"Create a marketing message for this campaign: {prompt}",
                    },
                ],
                temperature=0.7,
                max_completion_tokens=150,
            )
            text = response.choices[0].message.content
            if not text:
                return self.fallback.generate(prompt)
            return text.strip().strip('"').strip("'")

        except Exception as exc:
            logger.exception("Groq text generation failed")
            return self.fallback.generate(prompt)