from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    database_url: str = "sqlite:///:memory:" if os.getenv("VERCEL") == "1" else "sqlite:///data/app.db"

    class Config:
        env_file = ".env"


settings = Settings()
