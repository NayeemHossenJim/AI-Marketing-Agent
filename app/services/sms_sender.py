import logging

logger = logging.getLogger(__name__)

class ConsoleSmsSender:
    def send(self, phone: str, campaign_name: str, text: str, image_url: str) -> None:
        message = (
            f"Sending marketing message to {phone}\n"
            f"Campaign: {campaign_name}\n"
            f"Generated Text:\n{text}\n"
            f"Generated Image:\n{image_url}"
        )
        print(message)
        logger.info("Campaign sent to %s", phone)
