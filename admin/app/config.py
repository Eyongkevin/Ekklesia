from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BASE_URL: str
    TELEGRAM_BOT_USERNAME: str

    class Config:
        env_file = ".env"

settings = Settings()