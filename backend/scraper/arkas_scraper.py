import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from .sahibinden_scraper import SahibindenScraper

logger = logging.getLogger(__name__)

class ShowroomScraper:
    """
    Showroom Scraper Facade:
    Runs SahibindenScraper to collect verified vehicle listings from listing portals.
    """
    def __init__(self):
        self.sahibinden_scraper = SahibindenScraper()

    def scrape_and_save(self, db: Session, limit: int = 50) -> Dict[str, int]:
        return self.sahibinden_scraper.scrape_and_save(db, limit=limit)

# Backward-compatibility alias
ArkasScraper = ShowroomScraper
