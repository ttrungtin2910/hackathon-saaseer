"""
Configuration settings for SaaSeer Contract Management API
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # Application settings
    app_name: str = Field(default="SaaSeer Contract Management API", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=True, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # Server settings
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # Azure Cosmos DB settings
    cosmos_endpoint: str = Field(..., env="COSMOS_ENDPOINT")
    cosmos_key: str = Field(..., env="COSMOS_KEY")
    cosmos_database_name: str = Field(default="ContractManagement", env="COSMOS_DATABASE_NAME")
    cosmos_container_name: str = Field(default="contracts", env="COSMOS_CONTAINER_NAME")
    
    # CORS settings
    cors_origins: list = Field(default=["*"], env="CORS_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    cors_allow_methods: list = Field(default=["*"], env="CORS_ALLOW_METHODS")
    cors_allow_headers: list = Field(default=["*"], env="CORS_ALLOW_HEADERS")
    
    # Logging settings
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # OpenAI settings
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-5", env="OPENAI_MODEL")
    
    # Expiration settings
    expiry_warning_days: int = Field(default=60, env="EXPIRY_WARNING_DAYS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Dependency function to get settings instance
    """
    return settings
