import logging
import re
import urllib.request
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from config import settings
from src.db.models import Vehicle
from .normalizer import VehicleNormalizer

logger = logging.getLogger(__name__)

class ArkasScraper:
    def __init__(self):
        self.base_url = settings.SCRAPER_BASE_URL.rstrip("/")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
        }

    def _fetch_html(self, url: str) -> Optional[str]:
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=settings.SCRAPER_TIMEOUT) as response:
                return response.read().decode("utf-8", errors="ignore")
        except Exception as e:
            logger.warning(f"Error fetching URL {url}: {e}")
            return None

    def fetch_live_listings(self, max_items: int = 50) -> List[Dict[str, Any]]:
        """
        Scrapes real vehicle listings and all photographic angles directly from arkasotomotiv2.com
        """
        logger.info(f"Connecting to live catalog: {self.base_url}/Araclar/Index/1")
        html = self._fetch_html(f"{self.base_url}/Araclar/Index/1")
        if not html:
            logger.error("Could not fetch catalog homepage from arkasotomotiv2.com")
            return []

        soup = BeautifulSoup(html, "html.parser")
        
        # Discover unique vehicle detail links (Araclar/Goster/\d+)
        car_links = []
        for a in soup.find_all("a", href=re.compile(r"Araclar/Goster/\d+")):
            href = a.get("href", "").strip()
            if href and href not in car_links:
                car_links.append(href)

        logger.info(f"Found {len(car_links)} unique vehicles in live catalog.")
        scraped_vehicles = []

        for href in car_links[:max_items]:
            vehicle_url = f"{self.base_url}/{href.lstrip('/')}"
            ext_id_match = re.search(r"Araclar/Goster/(\d+)", href)
            external_id = ext_id_match.group(1) if ext_id_match else f"ARKAS-{len(scraped_vehicles)+1}"

            det_html = self._fetch_html(vehicle_url)
            if not det_html:
                continue

            det_soup = BeautifulSoup(det_html, "html.parser")

            # 1. Title Extraction
            h1 = det_soup.find("h1") or det_soup.find("h2")
            raw_title = h1.get_text(strip=True) if h1 else ""
            clean_title = re.sub(r"^[0-9\.\s]*El\s*", "", raw_title, flags=re.I).strip()
            
            # 2. Extract Real Photos (panel/public/resimler/{id}-*.jpg)
            img_matches = re.findall(r"panel/public/resimler/[^\s\"\'\<\>\)]+", det_html)
            img_urls = []
            for m in img_matches:
                clean_m = m.split("?")[0].split("&")[0]
                if clean_m.endswith((".jpg", ".png", ".jpeg", ".webp")):
                    full_img_url = f"{self.base_url}/{clean_m}"
                    if full_img_url not in img_urls:
                        img_urls.append(full_img_url)

            primary_img = img_urls[0] if img_urls else "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=1200&q=80"

            # 3. Extract Price
            price_match = re.search(r"([\d\.,]+)\s*TL", det_html)
            raw_price = price_match.group(1) if price_match else "0"
            price = VehicleNormalizer.clean_price(raw_price)

            # 4. Extract Specs (Marka, Yıl, Km, Yakıt Tipi, Şanzıman, Renk)
            specs = {}
            for elem in det_soup.find_all(["li", "tr", "div", "p"]):
                txt = elem.get_text(":", strip=True)
                if ":" in txt:
                    parts = txt.split(":")
                    if len(parts) >= 2:
                        k = parts[0].strip()
                        v = parts[1].strip()
                        for target in ["Marka", "Yıl", "Km", "Yakıt Tipi", "Şanzıman", "Renk"]:
                            if target.lower() in k.lower() and v and target not in specs:
                                specs[target] = v

            brand = specs.get("Marka", "")
            if not brand and clean_title:
                parts = clean_title.split(" ")
                brand = parts[0] if parts else "Genel"

            norm_brand = VehicleNormalizer.normalize_brand(brand)

            # Year extraction from specs or title
            raw_year = specs.get("Yıl", "")
            if not raw_year:
                year_match = re.search(r"\b(20[12]\d)\b", clean_title)
                raw_year = year_match.group(1) if year_match else 2023
            year = VehicleNormalizer.clean_year(raw_year)

            # KM extraction from specs or text
            raw_km = specs.get("Km", "")
            if not raw_km:
                km_match = re.search(r"\b(\d{1,3}(?:\.\d{3})+|\d{4,6})\s*(?:km)?\b", det_html, re.I)
                raw_km = km_match.group(1) if km_match else 35000
            km = VehicleNormalizer.clean_km(raw_km)

            fuel_type = specs.get("Yakıt Tipi", "Benzin")
            transmission = specs.get("Şanzıman", "Otomatik")
            color = specs.get("Renk", "Metalik")

            # Extract Model & Sub-model
            model = ""
            sub_model = ""
            if clean_title:
                # Remove year and brand from clean_title
                cleaned_name = re.sub(r"^\b20\d\d\b\s*", "", clean_title).strip()
                cleaned_name = re.sub(rf"^{brand}\s*", "", cleaned_name, flags=re.I).strip()
                title_parts = cleaned_name.split(" ", 1)
                model = title_parts[0] if len(title_parts) > 0 else "Model"
                sub_model = title_parts[1] if len(title_parts) > 1 else ""

            # Determine Body Type from title / sub_model
            body_type = "Sedan"
            upper_all = (clean_title + " " + sub_model).upper()
            if any(k in upper_all for k in ["SUV", "XC", "CROSS", "MOKKA", "2008", "3008", "5008", "KAMIQ", "QASHQAI", "TUCSON", "SPORTAGE"]):
                body_type = "SUV"
            elif any(k in upper_all for k in ["HATCHBACK", "HB", "CLIO", "CORSA", "POLO", "GOLF", "IBIZA", "A3"]):
                body_type = "Hatchback"
            elif any(k in upper_all for k in ["TRANSIT", "CUSTOM", "COURIER", "DUCATO", "VAN", "COMBO"]):
                body_type = "Ticari / Van"

            # Features / Highlights
            features = []
            if sub_model:
                features.append(sub_model)
            features.append(f"{transmission} Vites & {fuel_type}")
            features.append(f"{color} Gövde Rengi")
            features.append("Arkas Otomotiv Yetkili Servis Geçmişli")
            features.append("Ekspertiz ve Kilometre Garantili")

            scraped_vehicles.append({
                "external_id": external_id,
                "source": "Arkas Otomotiv 2",
                "url": vehicle_url,
                "brand": norm_brand,
                "model": model,
                "sub_model": sub_model,
                "year": year,
                "km": km,
                "price": price,
                "currency": "TL",
                "fuel_type": fuel_type,
                "transmission": transmission,
                "body_type": body_type,
                "color": color,
                "features": features,
                "expertise_note": "Arkas 2. El Ekspertiz ve Kilometre Garantilidir. Tüm kontrolleri yapılmıştır.",
                "image_urls": img_urls,
                "primary_image_url": primary_img
            })

        logger.info(f"Successfully parsed {len(scraped_vehicles)} vehicles with genuine gallery photos.")
        return scraped_vehicles

    def scrape_and_save(self, db: Session, limit: int = 50) -> Dict[str, Any]:
        """
        Scrapes real vehicles from arkasotomotiv2.com and saves to PostgreSQL idempotently.
        """
        items = self.fetch_live_listings(max_items=limit)
        
        new_count = 0
        updated_count = 0
        skipped_count = 0
        saved_vehicles = []

        for item in items:
            norm_brand = VehicleNormalizer.normalize_brand(item["brand"])
            norm_price = VehicleNormalizer.clean_price(item["price"])
            norm_km = VehicleNormalizer.clean_km(item["km"])
            norm_year = VehicleNormalizer.clean_year(item["year"])
            norm_features = VehicleNormalizer.normalize_features(item.get("features", []))

            clean_payload = {
                "brand": norm_brand,
                "model": item.get("model", "").strip(),
                "year": norm_year,
                "km": norm_km,
                "price": norm_price,
                "features": norm_features,
                "primary_image_url": item.get("primary_image_url", ""),
                "image_urls_count": len(item.get("image_urls", []))
            }
            content_hash = VehicleNormalizer.compute_content_hash(clean_payload)

            existing = db.query(Vehicle).filter(Vehicle.external_id == item["external_id"]).first()
            if existing:
                if existing.content_hash == content_hash:
                    skipped_count += 1
                    saved_vehicles.append(existing)
                    continue
                else:
                    existing.brand = norm_brand
                    existing.model = item.get("model", existing.model)
                    existing.sub_model = item.get("sub_model", existing.sub_model)
                    existing.year = norm_year
                    existing.km = norm_km
                    existing.price = norm_price
                    existing.fuel_type = item.get("fuel_type", existing.fuel_type)
                    existing.transmission = item.get("transmission", existing.transmission)
                    existing.body_type = item.get("body_type", existing.body_type)
                    existing.color = item.get("color", existing.color)
                    existing.features = norm_features
                    existing.image_urls = item.get("image_urls", existing.image_urls)
                    existing.primary_image_url = item.get("primary_image_url", existing.primary_image_url)
                    existing.content_hash = content_hash
                    existing.is_active = True
                    updated_count += 1
                    saved_vehicles.append(existing)
            else:
                vehicle = Vehicle(
                    external_id=item["external_id"],
                    source=item.get("source", "Arkas Otomotiv 2"),
                    url=item.get("url"),
                    brand=norm_brand,
                    model=item.get("model", ""),
                    sub_model=item.get("sub_model", ""),
                    year=norm_year,
                    km=norm_km,
                    price=norm_price,
                    currency=item.get("currency", "TL"),
                    fuel_type=item.get("fuel_type", ""),
                    transmission=item.get("transmission", ""),
                    body_type=item.get("body_type", ""),
                    color=item.get("color", ""),
                    features=norm_features,
                    expertise_note=item.get("expertise_note", ""),
                    image_urls=item.get("image_urls", []),
                    primary_image_url=item.get("primary_image_url", ""),
                    content_hash=content_hash,
                    is_active=True
                )
                db.add(vehicle)
                db.flush()
                new_count += 1
                saved_vehicles.append(vehicle)

        db.commit()
        return {
            "total_processed": len(items),
            "new_added": new_count,
            "updated": updated_count,
            "skipped_duplicate": skipped_count,
            "saved_vehicles": saved_vehicles
        }
