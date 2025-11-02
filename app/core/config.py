"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Smart Cane GPS Tracker"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    
    # Database
    DATABASE_URL: str = "database.db"
    
    # ESP32
    ESP32_IP: Optional[str] = "10.241.12.160"
    ESP32_DEVICE_ID: str = "SmartCane01"
    
    # Timezone
    SERVER_TIMEZONE: str = "Asia/Ho_Chi_Minh"
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # Sync
    AUTO_SYNC_ENABLED: bool = True
    SYNC_INTERVAL: int = 10  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
