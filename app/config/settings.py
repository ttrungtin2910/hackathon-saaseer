"""Application configuration settings"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""

    # CosmosDB Configuration
    COSMOS_ENDPOINT: str = os.getenv(
        "COSMOS_ENDPOINT", "https://your-cosmos-account.documents.azure.com:443/"
    )
    COSMOS_KEY: str = os.getenv("COSMOS_KEY", "your-cosmos-primary-key")
    COSMOS_DATABASE_NAME: str = os.getenv("COSMOS_DATABASE_NAME", "ContractManagement")

    # Azure Blob Storage Configuration
    AZURE_SA_URL: str = os.getenv(
        "AZURE_SA_URL", "https://your-storage-account.blob.core.windows.net/"
    )
    AZURE_SA_KEY: str = os.getenv("AZURE_SA_KEY", "your-storage-account-key")
    AZURE_CONTAINER_NAME: str = os.getenv("AZURE_CONTAINER_NAME", "contracts")

    # Azure OpenAI Configuration
    PROVIDER_NAME: str = os.getenv("PROVIDER_NAME", "azure_openai")
    AZURE_OPENAI_API_KEY: str = os.getenv(
        "AZURE_OPENAI_API_KEY", "your-azure-openai-api-key"
    )
    AZURE_OPENAI_ENDPOINT: str = os.getenv(
        "AZURE_OPENAI_ENDPOINT", "https://your-endpoint.openai.azure.com/"
    )
    OPENAI_API_VERSION: str = os.getenv("OPENAI_API_VERSION", "2024-12-01-preview")
    OPENAI_MODEL_NAME: str = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    OPENAI_TIME_OUT: int = int(os.getenv("OPENAI_TIME_OUT", "10"))
    AZ_OPENAI_TEMP: float = float(os.getenv("AZ_OPENAI_TEMP", "0.3"))
    AZ_MAX_TOKEN: int = int(os.getenv("AZ_MAX_TOKEN", "1000"))

    # Legacy OpenAI Configuration (fallback)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")

    # Application Configuration
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "True").lower() == "true"

    # SerpAPI Configuration for web search
    SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY", "your-serpapi-key")


# Global settings instance
settings = Settings()
