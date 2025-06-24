from functools import lru_cache
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    # Project info
    PROJECT_NAME: str = Field(default="FastAPI Project")
    PROJECT_VERSION: str = Field(default="1.0.0")
    API_V1_STR: str = Field(default="/api/v1")
    
    # Environment
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    ALLOWED_HOSTS: List[str] = Field(default=["*"])
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/fastapi_db"
    )
    TEST_DATABASE_URL: Optional[str] = Field(default=None)
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key-change-this-in-production")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # Email settings (optional)
    SMTP_TLS: bool = Field(default=True)
    SMTP_PORT: Optional[int] = Field(default=587)
    SMTP_HOST: Optional[str] = Field(default=None)
    SMTP_USER: Optional[str] = Field(default=None)
    SMTP_PASSWORD: Optional[str] = Field(default=None)
    EMAILS_FROM_EMAIL: Optional[str] = Field(default=None)
    EMAILS_FROM_NAME: Optional[str] = Field(default=None)
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = Field(default=20)
    MAX_PAGE_SIZE: int = Field(default=100)
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.ENVIRONMENT == "development"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()