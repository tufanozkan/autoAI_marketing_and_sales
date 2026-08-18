import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from backend.db.models import Vehicle, CreativeBrief
from .brand_rules import BrandRules

logger = logging.getLogger(__name__)

class MarketingAgent:
    """
    Arkas Spoticar Otomotiv Pazarlama & Metin Üretim Ajanı:
    - 1. Dengeli (Balanced / Safe): Şeffaf, net, teknik ve ekspertiz detaylarını içeren objektif ton.
    - 2. Profesyonel (Professional): Kurumsal, saygın, filo ve premium alıcılara hitap eden ton.
    - 3. İlgi Çekici (Engaging / Bold): Sosyal medya ve B2C müşteriler için enerjik, emojili pazarlama tonu.
    - Çıktılar doğrudan 'creative_briefs' tablosuna yazılır.
    """

    def __init__(self, db: Session):
        self.db = db

    def generate_and_save_brief_for_vehicle(self, vehicle: Vehicle) -> CreativeBrief:
        brand_cfg = BrandRules.get_brand_config(vehicle.brand)
        segment_cfg = BrandRules.get_segment_rule(vehicle.body_type, vehicle.fuel_type)

        emotional_points = list(brand_cfg.get("emotional_points", []))
        if segment_cfg.get("focus"):
            emotional_points.append(segment_cfg.get("focus"))

        price_fmt = f"{vehicle.price:,.0f} {vehicle.currency}".replace(",", ".")
        km_fmt = f"{vehicle.km:,.0f} KM".replace(",", ".")
        pkg_name = f"{vehicle.brand} {vehicle.model} {vehicle.package or vehicle.sub_model or ''}".strip()

        tech = vehicle.technical_specs or {}
        ad_feat = vehicle.ad_features or {}
        damage = vehicle.damage_expertise or {}

        # Format damage text
        boyali = damage.get("boyali_parcalar", [])
        degisen = damage.get("degisen_parcalar", [])
        tramer = damage.get("tramer_kaydi_tl", 0)

        if not boyali and not degisen and (tramer == 0 or not tramer):
            exp_status_str = "Hatasız, Boyasız ve Değişensiz (Tramer kaydı yoktur)"
        else:
            parts = []
            if boyali: parts.append(f"Boyalı Parçalar: {', '.join(boyali)}")
            if degisen: parts.append(f"Değişen Parçalar: {', '.join(degisen)}")
            if tramer: parts.append(f"Tramer Kaydı: {tramer:,.0f} TL".replace(",", "."))
            exp_status_str = " | ".join(parts)

        # 1. DENGELİ (BALANCED)
        balanced_copy = (
            f"İncelemekte olduğunuz {vehicle.year} model {pkg_name}, {km_fmt} orijinal kilometresindedir. "
            f"{tech.get('motor_gucu_hp', '130 HP')} güç üreten motoru ve {vehicle.transmission or 'Otomatik'} şanzımanı ile "
            f"100 km'de ortalama {tech.get('yakit_tuketimi_lt', '4.9 lt')} yakıt tüketimi sunmaktadır.\n\n"
            f"Ekspertiz ve Kondisyon Durumu:\n"
            f"• {exp_status_str}\n"
            f"• {vehicle.expertise_note or 'Arkas Spoticar 100+ Nokta Kontrolünden geçmiş olup 12 Ay Garantilidir.'}\n\n"
            f"Öne Çıkan Donanımlar: {', '.join((ad_feat.get('konfor', []) + ad_feat.get('guvenlik', []))[:4])}.\n"
            f"Aracımız {price_fmt} liste fiyatı ve Arkas güvencesiyle satışa sunulmuştur."
        )

        # 2. PROFESYONEL (PROFESSIONAL)
        professional_copy = (
            f"Arkas Otomotiv kurumsal portföyünde yer alan {vehicle.year} {pkg_name}, segmentinin en verimli modelleri arasında yer almaktadır. "
            f"{tech.get('tork_nm', '230 Nm')} tork değeri ve {tech.get('bagaj_hacmi_lt', '350 lt')} bagaj hacmi ile hem kurumsal filo operasyonları hem de bireysel üst düzey kullanım için ideal bir tercihtir.\n\n"
            f"Kurumsal Güvence Standartları:\n"
            f"• Spoticar 100+ Nokta Kapsamlı Mekanik ve Elektronik Ekspertiz Onayı\n"
            f"• 12 Ay Spoticar Premium Mekanik Garanti Kapsamı\n"
            f"• Şeffaf Ekspertiz: {exp_status_str}\n\n"
            f"Kurumsal fatura, takas desteği ve avantajlı taşıt kredisi imkanlarıyla Arkas showroomlarında incelenebilir."
        )

        # 3. İLGİ ÇEKİCİ (ENGAGING)
        engaging_copy = (
            f"✨ Hayalinizdeki otomobil Arkas Spoticar ayrıcalığıyla karşınızda! {vehicle.year} model {pkg_name}! 🚗💨\n\n"
            f"🔥 Neden Bu Araç?\n"
            f"• {tech.get('motor_gucu_hp', '130 HP')} gücünde seri performans & 100 km'de yalnızca {tech.get('yakit_tuketimi_lt', '4.9 lt')} tüketim! ⚡\n"
            f"• {', '.join(ad_feat.get('konfor', [])[:3])} gibi üst düzey konfor donanımları! 🛋️\n"
            f"• {', '.join(ad_feat.get('multimedya', [])[:2])} ile kesintisiz dijital bağlantı! 📱\n"
            f"• Durum: {exp_status_str} 🛡️\n\n"
            f"💎 Sadece {km_fmt}'de, pırıl pırıl kondisyonda ve 12 ay garantili!\n"
            f"💰 Fiyat: {price_fmt}\n\n"
            f"Fırsatı kaçırma! Hemen mesaj at veya showroomumuza uğra! 📲"
        )

        story_frames = [
            {"scene": 1, "text": f"{pkg_name}\n{km_fmt} • {vehicle.year} Model 🔥"},
            {"scene": 2, "text": f"Ekspertiz: {exp_status_str}\n100+ Nokta Garantisi 🛡️"},
            {"scene": 3, "text": f"Satış Fiyatı: {price_fmt}\nShowroomumuza Bekleriz 📞"}
        ]

        hashtags = [
            f"#{vehicle.brand.replace('-', '').replace(' ', '')}",
            f"#{vehicle.model.replace(' ', '')}",
            "#ArkasSpoticar",
            "#IkinciEl",
            "#GarantiliAraba",
            "#OtomobilDunyasi"
        ]

        existing = self.db.query(CreativeBrief).filter(CreativeBrief.vehicle_id == vehicle.id).first()
        if existing:
            existing.brand_archetype = brand_cfg.get("archetype", "Güvenilir Otomotiv")
            existing.target_persona = brand_cfg.get("target_persona", "Otomobil Alıcısı")
            existing.emotional_points = emotional_points
            existing.tone_of_voice = brand_cfg.get("tone", "Kurumsal & Şeffaf")
            existing.key_hooks = brand_cfg.get("hooks", [])
            existing.balanced_copy = balanced_copy
            existing.professional_copy = professional_copy
            existing.engaging_copy = engaging_copy
            existing.story_frames = story_frames
            existing.hashtags = hashtags
            brief = existing
        else:
            brief = CreativeBrief(
                vehicle_id=vehicle.id,
                brand_archetype=brand_cfg.get("archetype", "Güvenilir Otomotiv"),
                target_persona=brand_cfg.get("target_persona", "Otomobil Alıcısı"),
                emotional_points=emotional_points,
                tone_of_voice=brand_cfg.get("tone", "Kurumsal & Şeffaf"),
                key_hooks=brand_cfg.get("hooks", []),
                balanced_copy=balanced_copy,
                professional_copy=professional_copy,
                engaging_copy=engaging_copy,
                story_frames=story_frames,
                hashtags=hashtags
            )
            self.db.add(brief)

        self.db.commit()
        self.db.refresh(brief)
        return brief

    def process_all_pending(self, limit: int = 50) -> int:
        vehicles = self.db.query(Vehicle).filter(Vehicle.is_active == True).limit(limit).all()
        count = 0
        for v in vehicles:
            self.generate_and_save_brief_for_vehicle(v)
            count += 1
        return count
