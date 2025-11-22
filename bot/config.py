from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str = "postgresql://user:password@localhost/tonlucky"
    REDIS_URL: str = "redis://localhost:6379"
    TON_CONNECT_API_KEY: Optional[str] = None
    TON_WALLET_ADDRESS: Optional[str] = None
    ADMIN_CHAT_ID: Optional[int] = None
    
    class Config:
        env_file = ".env"


settings = Settings()