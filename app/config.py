from pydantic_settings import BaseSettings
from pydantic import field_validator, PostgresDsn
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: PostgresDsn

    # JWT
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # OAuth
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    # Environment
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

    @field_validator("DATABASE_URL")
    def assemble_db_connection(cls, v: PostgresDsn) -> str:
        db_url = str(v)
        if not db_url.endswith("/jwt_api_db"):
            db_url = f"{db_url}/jwt_api_db"
        return db_url

settings = Settings()
