from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./data/app.db"
    seatgeek_client_id: str | None = None
    
    class Config:
        env_file = ".env"

settings = Settings()
