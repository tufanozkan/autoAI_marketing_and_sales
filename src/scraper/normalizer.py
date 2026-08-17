import hashlib
import json
import re
from typing import Dict, Any, List

class VehicleNormalizer:
    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        return re.sub(r'\s+', ' ', str(text)).strip()

    @staticmethod
    def clean_price(raw_price: Any) -> float:
        if isinstance(raw_price, (int, float)):
            return float(raw_price)
        if not raw_price:
            return 0.0
        # Remove TL, TRY, dots, commas, spaces
        cleaned = str(raw_price).upper().replace("TL", "").replace("TRY", "").strip()
        cleaned = re.sub(r'[^\d,.]', '', cleaned)
        if "." in cleaned and "," in cleaned:
            # e.g., "1.450.000,00" -> "1450000.00"
            cleaned = cleaned.replace(".", "").replace(",", ".")
        elif "." in cleaned:
            # Could be "1.450.000" or "1450.50"
            parts = cleaned.split(".")
            if len(parts) > 2 or (len(parts) == 2 and len(parts[1]) == 3):
                cleaned = cleaned.replace(".", "")
        elif "," in cleaned:
            cleaned = cleaned.replace(",", ".")
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    @staticmethod
    def clean_km(raw_km: Any) -> int:
        if isinstance(raw_km, int):
            return raw_km
        if not raw_km:
            return 0
        cleaned = re.sub(r'[^\d]', '', str(raw_km))
        try:
            return int(cleaned)
        except ValueError:
            return 0

    @staticmethod
    def clean_year(raw_year: Any) -> int:
        if isinstance(raw_year, int):
            return raw_year
        if not raw_year:
            return 2020
        cleaned = re.sub(r'[^\d]', '', str(raw_year))
        try:
            val = int(cleaned)
            if 1990 <= val <= 2027:
                return val
            return 2020
        except ValueError:
            return 2020

    @staticmethod
    def normalize_brand(brand: str) -> str:
        if not brand:
            return "Genel"
        brand_map = {
            "volvo": "Volvo",
            "bmw": "BMW",
            "mercedes": "Mercedes-Benz",
            "mercedes-benz": "Mercedes-Benz",
            "audi": "Audi",
            "peugeot": "Peugeot",
            "opel": "Opel",
            "renault": "Renault",
            "citroen": "Citroën",
            "citroën": "Citroën",
            "ds": "DS Automobiles",
            "fiat": "Fiat",
            "alfa romeo": "Alfa Romeo",
            "jeep": "Jeep",
            "ford": "Ford",
            "mg": "MG",
            "volkswagen": "Volkswagen",
            "vw": "Volkswagen"
        }
        clean = brand.strip().lower()
        return brand_map.get(clean, brand.strip().title())

    @staticmethod
    def normalize_features(features: Any) -> List[str]:
        if isinstance(features, list):
            return [VehicleNormalizer.clean_text(f) for f in features if f]
        if isinstance(features, str):
            parts = re.split(r'[,;\n•|]', features)
            return [VehicleNormalizer.clean_text(p) for p in parts if p.strip()]
        return []

    @staticmethod
    def compute_content_hash(data: Dict[str, Any]) -> str:
        """Computes SHA256 hash of core vehicle attributes to detect changes."""
        key_data = {
            "brand": str(data.get("brand", "")).strip().lower(),
            "model": str(data.get("model", "")).strip().lower(),
            "year": int(data.get("year", 0)),
            "km": int(data.get("km", 0)),
            "price": float(data.get("price", 0.0)),
            "features": sorted(data.get("features", [])),
            "primary_image_url": str(data.get("primary_image_url", ""))
        }
        serialized = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
