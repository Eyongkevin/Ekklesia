from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False
    TELEGRAM_BOT_TOKEN: str
    SECRET_KEY: str
    ALGORITHM: str
    SECURE: bool = False
    ACCESS_TOKEN_EXPIRE_HOURS: int

    class Config:
        env_file = ".env"

settings = Settings()