import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    PROJECT_NAME: str = "Fake Job Detector Portal"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Real-Time Global Job Vacancy Portal with Intelligent Fake Job Detection"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/fakejobdb")
    DEV_DATABASE_URL: str = os.getenv("DEV_DATABASE_URL", "sqlite:///./dev.db")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    MODEL_DIR: Path = Path(os.getenv("MODEL_DIR", str(BASE_DIR / "app" / "ml_models" / "artifacts")))

    KAGGLE_USERNAME: str | None = os.getenv("KAGGLE_USERNAME")
    KAGGLE_KEY: str | None = os.getenv("KAGGLE_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
