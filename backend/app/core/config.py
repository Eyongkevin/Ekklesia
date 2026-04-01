from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_BOT_USERNAME: str

    class Config:
        env_file = ".env"

settings = Settings()