import logging
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from backend.db.models import Vehicle
from .search_engine import VehicleSearchEngine
from .nlu import norm

logger = logging.getLogger(__name__)

class ChatbotTools:
    @staticmethod
    def answer_general_faq(query_text: str, salutation: str) -> Optional[str]:
        q = norm(query_text)
        sal = f"{salutation}, " if salutation else "Değerli Müşterimiz, "

        # 1. Trade-in (Takas)
        if any(w in q for w in ["takas", "eski arac", "aracimi vermek", "takasa", "degerleme", "değerleme"]):
            return (
                f"{sal}Showroomumuzda mevcut aracınız için şeffaf, hızlı ve güvenilir **takas desteği** sunuyoruz.\n\n"
                f"🔄 Dilerseniz aracınızın **marka, model, yıl, kilometre ve hasar durumunu** buradan paylaşırsanız anında ön değerlendirme yapabilir veya sizi merkez showroomumuzda ücretsiz ekspertiz için ağırlayabiliriz!"
            )

        # 2. Credit / Financing (Kredi & Taksit)
        if any(w in q for w in ["kredi", "finansman", "taksit", "pesinat", "peşinat", "faiz", "oran", "vade", "banka"]):
            return (
                f"{sal}Anlaşmalı finans kuruluşlarımız ve bankalarımızla ikinci el araçlarımızda cazip faizli **taşıt kredisi ve esnek finansman çözümleri** sağlıyoruz.\n\n"
                f"💳 Araç bedelinin model yılına göre %70'ine kadar kredi kullandırabilmekteyiz. İlgilendiğiniz model için peşinat ve aylık taksit planı çıkarmamı ister misiniz?"
            )

        # 3. Location / Hours
        if any(w in q for w in ["nerede", "neredesiniz", "adres", "lokasyon", "konum", "showroom", "galeri", "saat kacta", "saat kaçta", "calisma saatleri", "çalışma saatleri", "acik mi", "açık mı"]):
            return (
                f"{sal}Merkez Showroomumuz haftanın 7 günü hizmet vermektedir.\n\n"
                f"📍 **Adres:** Otomotiv Plaza No: 100 Showroom Alanı\n"
                f"🕒 **Çalışma Saatleri:** Pazartesi - Cumartesi: 08:30 - 18:30 | Pazar: 11:00 - 17:00\n\n"
                f"Araçlarımızı yakından incelemek ve kahvemiz eşliğinde test sürüşü yapmak için dilediğiniz zaman bekleriz!"
            )

        # 4. Warranty & Inspection
        if any(w in q for w in ["garanti", "garanti suresi", "garanti süresi", "kac ay garanti", "kaç ay garanti", "guvence", "güvence", "100 nokta", "kac nokta", "kaç nokta", "ekspertiz"]):
            return (
                f"{sal}Bünyemizdeki tüm araçlarımız **100+ Nokta Kapsamlı Teknik Kontrolden** geçmektedir.\n\n"
                f"🛡️ Araçlarımız **12 Aya Kadar Sınırsız Kilometre Garantisi**, 7/24 Yol Yardımı ve Şeffaf Ekspertiz Raporu güvencesiyle teslim edilmektedir."
            )

        return None

    @staticmethod
    def generate_vehicle_executive_presentation(vehicle: Vehicle, salutation: str, db: Session) -> str:
        model_name = f"{vehicle.brand} {vehicle.model} {vehicle.package or vehicle.sub_model or ''}".strip()
        km_str = f"{vehicle.km:,.0f} KM".replace(",", ".")
        price_str = f"{vehicle.price:,.0f} {vehicle.currency}".replace(",", ".")
        sal = f"{salutation}, " if salutation else "Değerli Müşterimiz, "

        tech = vehicle.technical_specs or {}
        damage = vehicle.damage_expertise or {}
        ad_feat = vehicle.ad_features or {}

        # Core specs
        fuel = vehicle.fuel_type or ("Dizel" if "bluehdi" in norm(vehicle.package or "") else "Benzin")
        trans = vehicle.transmission or tech.get("sanziman", "Tam Otomatik")
        hp = tech.get("motor_gucu_hp") or vehicle.engine_power or "130 HP"
        cons = tech.get("yakit_tuketimi_lt", "4.5 lt / 100 km")
        bagaj = tech.get("bagaj_hacmi_lt", "500+ Litre")

        # Highlights from equipment
        highlights = []
        for cat in ["konfor", "guvenlik", "multimedya", "dis_donanim", "ic_donanim"]:
            items = ad_feat.get(cat, [])
            if items:
                highlights.append(items[0])
                if len(items) > 1 and len(highlights) < 5:
                    highlights.append(items[1])

        feat_lines = "\n".join([f"  • {f}" for f in highlights[:5]]) if highlights else "  • Zengin konfor, güvenlik ve multimedya donanım paketi"

        # Expertise details
        boyali = damage.get("boyali_parcalar", [])
        degisen = damage.get("degisen_parcalar", [])
        tramer = damage.get("tramer_kaydi_tl", 0)
        if not boyali and not degisen and (tramer == 0 or not tramer):
            exp_text = "Hatasız, Boyasız ve Değişensiz (Tramer Hasar Kaydı: 0 TL)"
        else:
            b_cnt = f"{len(boyali)} parça boyalı" if boyali else "Boyasız"
            d_cnt = f"{len(degisen)} parça değişen" if degisen else "Değişensiz"
            t_val = f"Tramer: {tramer:,.0f} TL".replace(",", ".") if tramer else "Tramer: 0 TL"
            exp_text = f"{b_cnt}, {d_cnt}, {t_val}"

        note = vehicle.expertise_note or "100+ Nokta Kontrolünden geçmiş olup 12 Ay Mekanik & Elektronik Garantilidir."

        return (
            f"{sal}**{model_name}** ({vehicle.year}) modelimiz hakkında kapsamlı ve detaylı bilgiler:\n\n"
            f"📋 **Temel Özellikler & Performans:**\n"
            f"• 💰 **Satış Fiyatı:** {price_str}\n"
            f"• 📍 **Kilometre:** {km_str} (Orijinal Kilometre Garantili)\n"
            f"• ⚙️ **Vites & Şanzıman:** {trans}\n"
            f"• ⛽ **Motor & Yakıt:** {fuel} ({hp}) | Ortalama Tüketim: {cons}\n"
            f"• 🧳 **Bagaj Hacmi:** {bagaj}\n\n"
            f"✨ **Öne Çıkan Donanımlar & Konfor:**\n"
            f"{feat_lines}\n\n"
            f"🛡️ **Ekspertiz & Garanti Durumu:**\n"
            f"• **Durum:** {exp_text}\n"
            f"• **Güvence:** {note}\n\n"
            f"Bu aracımız için showroomumuzda **test sürüşü randevusu** oluşturmamı veya takas/kredi teklifi hazırlamamı ister misiniz? 🚗✨"
        )

    @staticmethod
    def answer_vehicle_aspects(vehicle: Vehicle, aspects: List[str], salutation: str, db: Session) -> str:
        concrete_aspects = [a for a in (aspects or []) if a != "overview"]
        if not concrete_aspects:
            return ChatbotTools.generate_vehicle_executive_presentation(vehicle, salutation, db)

        aspects = concrete_aspects
        model_name = f"{vehicle.brand} {vehicle.model} {vehicle.package or vehicle.sub_model or ''}".strip()
        km_str = f"{vehicle.km:,.0f} KM".replace(",", ".")
        price_str = f"{vehicle.price:,.0f} {vehicle.currency}".replace(",", ".")
        sal = f"{salutation}, " if salutation else "Değerli Müşterimiz, "

        tech = vehicle.technical_specs or {}
        damage = vehicle.damage_expertise or {}
        ad_feat = vehicle.ad_features or {}

        # Flatten ad features
        flat_feats = []
        for cat_items in ad_feat.values():
            if isinstance(cat_items, list):
                flat_feats.extend(cat_items)
            elif isinstance(cat_items, str):
                flat_feats.append(cat_items)

        # Check multi-aspect
        if len(aspects) >= 2:
            bullets = []
            if "price" in aspects:
                bullets.append(f"• 💰 **Fiyat:** {price_str}")
            if "mileage" in aspects:
                bullets.append(f"• 📍 **Kilometre:** {km_str} (Orijinal Garantili)")
            if "transmission" in aspects:
                trans = vehicle.transmission or tech.get("sanziman", "Tam Otomatik")
                bullets.append(f"• ⚙️ **Şanzıman:** {trans}")
            if "fuel" in aspects or "engine" in aspects:
                fuel = vehicle.fuel_type or ("Dizel" if "bluehdi" in norm(vehicle.package or "") else "Benzin")
                hp = tech.get("motor_gucu_hp") or vehicle.engine_power or "130 HP"
                cons = tech.get("yakit_tuketimi_lt", "4.9 lt / 100 km")
                bullets.append(f"• ⛽ **Yakıt & Motor:** {fuel} | {hp} Güç | Ortalama Tüketim: {cons}")
            if "trunk" in aspects:
                bagaj = tech.get("bagaj_hacmi_lt", "500+ Litre")
                bullets.append(f"• 🧳 **Bagaj Hacmi:** {bagaj}")
            if "sunroof" in aspects:
                has_sunroof = VehicleSearchEngine._vehicle_has_feature(vehicle, "sunroof")
                bullets.append(f"• ☀️ **Cam Tavan:** {'Panoramik Açılabilir Cam Tavan Mevcut' if has_sunroof else 'Bu araçta cam tavan bulunmuyor'}")
            if "expertise" in aspects:
                boyali = damage.get("boyali_parcalar", [])
                degisen = damage.get("degisen_parcalar", [])
                tramer = damage.get("tramer_kaydi_tl", 0)
                if not boyali and not degisen and (tramer == 0 or not tramer):
                    bullets.append("• 🛡️ **Ekspertiz:** Hatasız, Boyasız, Tramer Kaydı Yok (0 TL)")
                else:
                    bullets.append(f"• 🛡️ **Ekspertiz:** Boyalı: {len(boyali)} parça, Değişen: {len(degisen)} parça")

            return (
                f"{sal}**{model_name}** ({vehicle.year}) aracımız hakkında merak ettiğiniz detaylar:\n\n"
                + "\n".join(bullets)
                + "\n\nAracımızı showroomumuzda test sürüşüyle deneyimlemek ister misiniz?"
            )

        # Single aspect details
        if "transmission" in aspects:
            trans = vehicle.transmission or tech.get("sanziman", "Tam Otomatik")
            return (
                f"{sal}{vehicle.year} model **{model_name}** aracımız **{trans}** şanzımana sahiptir. "
                f"Vites geçişleri son derece pürüzsüz ve konforludur."
            )

        if "mileage" in aspects:
            return (
                f"{sal}**{model_name}** aracımız yalnızca **{km_str}**'dedir. "
                f"Orijinal kilometre garantilidir ve ekspertiz güvencesindedir."
            )

        if "price" in aspects:
            return (
                f"{sal}**{model_name}** aracımızın güncel satış fiyatı **{price_str}**'dir. "
                f"Showroom güvencesiyle takas, kredi ve avantajlı finansman seçeneklerimiz mevcuttur."
            )

        if "trunk" in aspects:
            bagaj = tech.get("bagaj_hacmi_lt", "500+ Litre")
            return (
                f"{sal}**{model_name}** aracımızın bagaj kapasitesi **{bagaj}**'dir. "
                f"Geniş yükleme alanı ve katlanabilir koltuklarıyla son derece fonksiyoneldir."
            )

        if "sunroof" in aspects:
            has_sunroof = VehicleSearchEngine._vehicle_has_feature(vehicle, "sunroof")
            if has_sunroof:
                return (
                    f"{sal}evet! **{model_name}** aracımızda **Panoramik Açılabilir Cam Tavan & Elektrikli Güneşlik** mevcuttur. "
                    f"Ferah ve aydınlık bir sürüş deneyimi sunar."
                )
            else:
                alt = VehicleSearchEngine.find_cross_alternative_with_feature(db, vehicle.id, "sunroof")
                alt_txt = f" Ancak portföyümüzdeki **{alt.brand} {alt.model} {alt.package or ''}** modelimizde Panoramik Açılabilir Cam Tavan mevcuttur." if alt else ""
                return (
                    f"{sal}**{model_name}** modelimizde cam tavan bulunmamaktadır.{alt_txt} "
                    f"Dilerseniz cam tavanlı alternatiflerimizi detaylandırabilirim!"
                )

        if "heating" in aspects:
            has_heat = VehicleSearchEngine._vehicle_has_feature(vehicle, "seat_heating")
            if has_heat:
                return f"{sal}evet! **{model_name}** aracımızda konfor artıran **Koltuk Isıtma** donanımı mevcuttur."
            else:
                alt = VehicleSearchEngine.find_cross_alternative_with_feature(db, vehicle.id, "seat_heating")
                alt_txt = f" Ancak stoklarımızdaki **{alt.brand} {alt.model}** modelimizde Advanced Comfort Masajlı & Isıtmalı Koltuklar mevcuttur." if alt else ""
                return f"{sal}**{model_name}** modelimizde koltuk ısıtma özelliği bulunmamaktadır.{alt_txt}"

        if "fuel" in aspects or "engine" in aspects:
            fuel = vehicle.fuel_type or ("Dizel" if "bluehdi" in norm(vehicle.package or "") else "Benzin")
            hp = tech.get("motor_gucu_hp") or vehicle.engine_power or "130 HP"
            tork = tech.get("tork_nm", "300 Nm")
            cons = tech.get("yakit_tuketimi_lt", "4.9 lt / 100 km")
            acc = tech.get("hizlanma_0_100")
            acc_str = f"\n🏎️ 0-100 km/s Hızlanma: **{acc}**" if acc else ""
            return (
                f"{sal}**{model_name}** ({fuel}) teknik performans detayları:\n\n"
                f"⚡ Motor Gücü & Tork: **{hp}** güç | **{tork}** tork\n"
                f"⛽ Ortalama Yakıt Tüketimi: **{cons}** ile son derece ekonomiktir.{acc_str}"
            )

        if "expertise" in aspects:
            boyali = damage.get("boyali_parcalar", [])
            degisen = damage.get("degisen_parcalar", [])
            tramer = damage.get("tramer_kaydi_tl", 0)

            if not boyali and not degisen and (tramer == 0 or not tramer):
                exp_detail = "• Boyalı Parça: **Yok (Tamamen Orijinal)**\n• Değişen Parça: **Yok (Hatasız)**\n• Tramer Hasar Kaydı: **Yok (0 TL)**"
            else:
                b_str = ", ".join(boyali) if boyali else "Yok"
                d_str = ", ".join(degisen) if degisen else "Yok"
                t_str = f"{tramer:,.0f} TL".replace(",", ".") if tramer else "0 TL"
                exp_detail = f"• Boyalı Parçalar: **{b_str}**\n• Değişen Parçalar: **{d_str}**\n• Tramer Hasar Kaydı: **{t_str}**"

            note = vehicle.expertise_note or "100+ Nokta Kontrolü ve 12 Ay Garantisi Kapsamındadır."
            return (
                f"{sal}**{model_name}** ekspertiz durumu:\n\n"
                f"{exp_detail}\n\n"
                f"🛡️ {note}"
            )

        if "equipment" in aspects:
            categories = [
                ("✨ Konfor & Teknoloji", ad_feat.get("konfor", [])),
                ("🛡️ Güvenlik & Sürüş Asistanları", ad_feat.get("guvenlik", [])),
                ("📱 Multimedya & Bağlantı", ad_feat.get("multimedya", [])),
                ("🚘 Dış & İç Tasarım", (ad_feat.get("dis_donanim", [])[:3] + ad_feat.get("ic_donanim", [])[:2]))
            ]
            lines = []
            for cat_title, items in categories:
                if items:
                    lines.append(f"**{cat_title}:**")
                    for it in items[:4]:
                        lines.append(f"• {it}")
                    lines.append("")

            if lines:
                return f"{sal}**{model_name}** aracımızın öne çıkan donanımları:\n\n" + "\n".join(lines).strip()
            else:
                return f"{sal}**{model_name}** aracımız zengin donanım paketi, dijital kokpiti ve güvenlik asistanlarıyla donatılmıştır."

        return f"{sal}**{model_name}** ({vehicle.year}) aracımız {km_str} mesafede olup güncel liste fiyatı {price_str}'dir."
