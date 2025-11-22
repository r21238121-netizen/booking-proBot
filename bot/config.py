from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Bot Configuration
    BOT_TOKEN: str
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379"
    TON_CONNECT_API_KEY: Optional[str] = None
    TON_WALLET_ADDRESS: Optional[str] = None
    ADMIN_CHAT_ID: Optional[int] = None
    WEBHOOK_URL: Optional[str] = None
    
    # Security
    SECRET_KEY: str
    JWT_SECRET: str
    
    # Limits
    MAX_WITHDRAWAL_PER_DAY: float = 5.0
    WITHDRAWAL_FEE_PERCENT: float = 3.0
    MIN_DEPOSIT_AMOUNT: float = 0.01
    MAX_BET_AMOUNT: int = 1000
    MIN_BET_AMOUNT: int = 10
    
    # Game Settings
    DICE_MIN_BET: int = 10
    DICE_MAX_BET: int = 1000
    DICE_MULTIPLIER: int = 5
    
    # Referral Settings
    REFERRAL_COMMISSION: float = 10.0  # 10% commission
    
    # TON Network
    TON_NETWORK: str = "testnet"  # or mainnet
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return os.getenv("ENVIRONMENT") == "production"


settings = Settings()