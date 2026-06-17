from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Marketing Automation"
    database_url: str = "sqlite:///./campaigns.db"
    groq_api_key: str | None = None
    groq_model: str = "llama-3.3-70b-versatile"
    scheduler_interval_seconds: int = 5

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()