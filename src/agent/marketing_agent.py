import random
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from src.db.models import Vehicle, CreativeBrief, MarketingCopy
from .brand_rules import BrandRules

class MarketingAgent:
    """
    Sub-agent responsible for analyzing vehicle listings and generating
    high-converting automotive marketing assets based on brand personality,
    target buyer personas, and emotional hooks.
    """

    def __init__(self, db: Session):
        self.db = db

    def generate_brief_for_vehicle(self, vehicle: Vehicle) -> CreativeBrief:
        brand_cfg = BrandRules.get_brand_config(vehicle.brand)
        segment_cfg = BrandRules.get_segment_rule(vehicle.body_type, vehicle.fuel_type)

        # Merge emotional selling points
        emotional_points = list(brand_cfg.get("emotional_points", []))
        emotional_points.append(segment_cfg.get("focus", ""))

        brief = CreativeBrief(
            vehicle_id=vehicle.id,
            brand_archetype=brand_cfg.get("archetype", "Güvenilir Otomotiv"),
            target_persona=brand_cfg.get("target_persona", "Otomobil Alıcısı"),
            emotional_points=emotional_points,
            tone_of_voice=brand_cfg.get("tone", "Kurumsal & Güvenilir"),
            key_hooks=brand_cfg.get("hooks", [])
        )
        self.db.add(brief)
        self.db.flush()
        return brief

    def generate_copies_for_vehicle(self, vehicle: Vehicle, brief: CreativeBrief) -> List[MarketingCopy]:
        brand_cfg = BrandRules.get_brand_config(vehicle.brand)
        segment_cfg = BrandRules.get_segment_rule(vehicle.body_type, vehicle.fuel_type)
        
        features_str = ", ".join(vehicle.features[:4]) if vehicle.features else "Ekspertiz Garantili, Kusursuz Bakımlı"
        price_fmt = f"{vehicle.price:,.0f} {vehicle.currency}".replace(",", ".")
        km_fmt = f"{vehicle.km:,.0f} km".replace(",", ".")

        # --- VARIANT 1: SAFE (Kurumsal / Güven Odaklı) ---
        safe_headline = f"{vehicle.year} {vehicle.brand} {vehicle.model} • Arkas 2. El Güvencesiyle"
        safe_hook = random.choice(brief.key_hooks) if brief.key_hooks else f"{vehicle.brand} kalitesi ve Arkas güvencesi buluştu."
        safe_body = (
            f"🚘 {vehicle.brand} {vehicle.model} {vehicle.sub_model or ''}\n"
            f"✨ {segment_cfg.get('tag', 'Konfor & Kalite')}\n\n"
            f"Yolculuklarınızda maksimum güvenlik, konfor ve şeffaflık arıyorsanız; titizlikle kontrol edilmiş {vehicle.year} model {vehicle.brand} {vehicle.model} sizleri bekliyor.\n\n"
            f"📌 Öne Çıkan Donanımlar: {features_str}\n"
            f"📍 Kilometre: {km_fmt} | Yıl: {vehicle.year}\n"
            f"🛡️ Durum: {vehicle.expertise_note or 'Arkas Ekspertiz Raporlu, Kusursuz Bakımlı'}\n"
            f"💰 Fiyat: {price_fmt}"
        )
        safe_cta = "Detaylı bilgi ve randevu için bize DM'den veya showroomlarımızdan ulaşabilirsiniz."
        safe_story_frames = [
            {"scene": 1, "text": f"{vehicle.brand} {vehicle.model}\nArkas 2. El Ayrıcalığıyla"},
            {"scene": 2, "text": f"Sadece {km_fmt} • {vehicle.year} Model\n{features_str}"},
            {"scene": 3, "text": f"Hemen İnceleyin: {price_fmt}\nShowroomlarımıza Davetlisiniz 📞"}
        ]
        safe_hashtags = [
            f"#{vehicle.brand.replace('-', '').replace(' ', '')}",
            f"#{vehicle.model.replace(' ', '')}",
            "#Arkas2El",
            "#IkinciElAraba",
            "#GuvenilirIkinciEl",
            "#OtomobilDunyasi"
        ]

        safe_copy = MarketingCopy(
            vehicle_id=vehicle.id,
            variant="safe",
            headline=safe_headline,
            hook=safe_hook,
            body=safe_body,
            cta=safe_cta,
            story_frames=safe_story_frames,
            hashtags=safe_hashtags
        )

        # --- VARIANT 2: BOLD (Duygusal / Dinamik / Yaşam Tarzı) ---
        bold_headline = f"Direksiyondaki Tutkuyu Hissedin: {vehicle.brand} {vehicle.model}"
        bold_hook = f"Sıradan yolculukları unutun. {vehicle.brand} ile her an bir ayrıcalığa dönüşüyor."
        bold_body = (
            f"🔥 Beklentilerin ötesinde bir sürüş deneyimi: {vehicle.brand} {vehicle.model}!\n\n"
            f"{brief.emotional_points[0] if brief.emotional_points else 'Yollarda gözler üzerinizde olacak.'}\n\n"
            f"⚡ {features_str} ile donatılmış bu özel otomobil, yalnızca {km_fmt}'de ve yeni sahibine hazır.\n\n"
            f"💎 {price_fmt} avantajıyla Arkas 2. El'de hemen yerinizi ayırtın!"
        )
        bold_cta = "Bu fırsatı kaçırmamak için hemen profilimizdeki linke tıklayın veya mesaj gönderin!"
        bold_story_frames = [
            {"scene": 1, "text": f"Göz Alıcı Bir Deneyim 🔥\n{vehicle.brand} {vehicle.model}"},
            {"scene": 2, "text": f"{features_str}\n{km_fmt} • Kusursuz Kondisyon"},
            {"scene": 3, "text": f"Fırsatı Yakala: {price_fmt} ⚡\nDM'den Bize Ulaşın!"}
        ]
        bold_hashtags = [
            f"#{vehicle.brand.replace('-', '').replace(' ', '')}Turkiye",
            f"#{vehicle.model.replace(' ', '')}",
            "#Arkas2El",
            "#LuxuryCars",
            "#SurusTutkusu",
            "#Otomotiv"
        ]

        bold_copy = MarketingCopy(
            vehicle_id=vehicle.id,
            variant="bold",
            headline=bold_headline,
            hook=bold_hook,
            body=bold_body,
            cta=bold_cta,
            story_frames=bold_story_frames,
            hashtags=bold_hashtags
        )

        self.db.add(safe_copy)
        self.db.add(bold_copy)
        self.db.flush()
        return [safe_copy, bold_copy]

    def process_vehicle(self, vehicle: Vehicle) -> Dict[str, Any]:
        """Runs full marketing pipeline for a single vehicle."""
        # Clean existing briefs/copies for idempotency
        self.db.query(MarketingCopy).filter(MarketingCopy.vehicle_id == vehicle.id).delete()
        self.db.query(CreativeBrief).filter(CreativeBrief.vehicle_id == vehicle.id).delete()
        self.db.flush()

        brief = self.generate_brief_for_vehicle(vehicle)
        copies = self.generate_copies_for_vehicle(vehicle, brief)
        self.db.commit()

        return {
            "vehicle_id": vehicle.id,
            "brief": brief.to_dict(),
            "copies": [c.to_dict() for c in copies]
        }

    def process_all_pending(self, limit: int = 50) -> int:
        """Processes vehicles that don't have copies yet."""
        vehicles = self.db.query(Vehicle).filter(Vehicle.is_active == True).limit(limit).all()
        count = 0
        for v in vehicles:
            self.process_vehicle(v)
            count += 1
        return count
