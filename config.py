import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
POSTERS_DIR = STATIC_DIR / "generated_posters"
FRONTEND_OUT_DIR = BASE_DIR / "frontend" / "out"

# Ensure static and output directories exist
STATIC_DIR.mkdir(parents=True, exist_ok=True)
POSTERS_DIR.mkdir(parents=True, exist_ok=True)

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
    SCRAPER_BASE_URL: str = os.getenv("SCRAPER_BASE_URL", "https://www.arkas2el.com")
    SCRAPER_TIMEOUT: int = 15
    MAX_SCRAPE_ITEMS: int = int(os.getenv("MAX_SCRAPE_ITEMS", "50"))
    
    # Web Server Settings
    WEB_HOST: str = os.getenv("WEB_HOST", "0.0.0.0")
    WEB_PORT: int = int(os.getenv("WEB_PORT", "8000"))
    
    # Poster Generation Settings
    POSTER_WIDTH: int = 1080
    POSTER_HEIGHT: int = 1350  # 4:5 Instagram Portrait Format
    BANNER_WIDTH: int = 1200
    BANNER_HEIGHT: int = 630   # Web / Landscape Format
    
    # Brand Theme Colors
    PRIMARY_COLOR: str = "#E30613"   # Arkas Red
    NAVY_COLOR: str = "#002B49"      # Arkas Navy
    DARK_BG: str = "#0F172A"         # Luxury Slate Dark
    GOLD_ACCENT: str = "#D4AF37"     # Premium Gold
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
