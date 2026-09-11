import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the backend directory (independent of the working directory)
BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR / ".env")

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./vittvaani.db")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    RESET_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("RESET_TOKEN_EXPIRE_MINUTES", "30"))

    # AI/LLM
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "claude-sonnet-4-20250514")

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # Frontend
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    # Google OAuth (leave empty to disable the flow; button then reports not configured)
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_AUTH_URL: str = os.getenv("GOOGLE_AUTH_URL", "https://accounts.google.com/o/oauth2/v2/auth")
    GOOGLE_TOKEN_URL: str = os.getenv("GOOGLE_TOKEN_URL", "https://oauth2.googleapis.com/token")
    GOOGLE_USERINFO_URL: str = os.getenv("GOOGLE_USERINFO_URL", "https://www.googleapis.com/oauth2/v3/userinfo")

    @property
    def google_oauth_enabled(self) -> bool:
        return bool(self.GOOGLE_CLIENT_ID and self.GOOGLE_CLIENT_SECRET)

    @property
    def google_redirect_uri(self) -> str:
        return f"{self.BACKEND_URL}/api/auth/google/callback"

    # App
    APP_NAME: str = "ArthSetu API"
    VERSION: str = "1.0.0"

settings = Settings()