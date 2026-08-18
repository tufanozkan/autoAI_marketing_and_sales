import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
FRONTEND_OUT_DIR = BASE_DIR / "frontend" / "out"

# Ensure static directory exists
STATIC_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseSettings):
    APP_NAME: str = "Arkas 2. El Pazarlama AI"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    
    # Database Settings (PostgreSQL - DBeaver Connection)
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "arkas_marketing_db")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"postgresql://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'postgres')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'arkas_marketing_db')}"
    )
    
    # Scraper Settings
    SCRAPER_BASE_URL: str = os.getenv("SCRAPER_BASE_URL", "https://arkasspoticar.sahibinden.com")
    SPOTI_CAR_URL: str = os.getenv("SPOTI_CAR_URL", "https://www.spoticar.com.tr/ikinci-el-araclar?filters[3][pointofsale]=CT1444T001")
    SCRAPER_TIMEOUT: int = int(os.getenv("SCRAPER_TIMEOUT", "10"))
    MAX_SCRAPE_ITEMS: int = int(os.getenv("MAX_SCRAPE_ITEMS", "50"))
    
    # Web Server Settings
    WEB_HOST: str = os.getenv("WEB_HOST", "0.0.0.0")
    WEB_PORT: int = int(os.getenv("WEB_PORT", "8000"))
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
