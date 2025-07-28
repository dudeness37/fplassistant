from pydantic_settings import BaseSettings
from pydantic import AnyUrl
import os

class Settings(BaseSettings):
    DATABASE_URL: AnyUrl | str = "sqlite:///./test.db"
    TELEGRAM_BOT_TOKEN: str | None = None
    TZ: str = "Europe/Madrid"

    class Config:
        # This is mainly for local dev outside Docker; inside Docker we use env vars.
        env_file = os.path.join(os.path.dirname(__file__), "../../..", "infra", ".env")
        env_file_encoding = "utf-8"

settings = Settings()
