from urllib.parse import quote_plus

class ImageUrlGenerator:
    def generate(self, prompt: str) -> str:
        text = quote_plus(prompt[:80])
        return f"https://dummyimage.com/1024x1024/111827/ffffff.png&text={text}"
