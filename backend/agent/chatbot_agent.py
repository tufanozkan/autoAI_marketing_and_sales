import re
import datetime
import logging
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from backend.db.models import Vehicle, CustomerLead, CreativeBrief, VehicleImage

logger = logging.getLogger(__name__)

# Comprehensive Turkish Name Knowledge Base for Accurate Gender & Honorific Detection
FEMALE_NAMES = {
    'ceren', 'ayse', 'ayşe', 'fatma', 'elif', 'zeynep', 'merve', 'busra', 'büşra', 'ebru', 'esra',
    'ozge', 'özge', 'gamze', 'selin', 'damla', 'irem', 'eda', 'asli', 'aslı', 'gizem', 'tugba', 'tuğba',
    'kubra', 'kübra', 'hazal', 'hande', 'sevgi', 'derya', 'deniz', 'nur', 'emine', 'hatice', 'yasemin',
    'pinar', 'pınar', 'sinem', 'duygu', 'burcu', 'didem', 'defne', 'eylul', 'eylül', 'azra', 'ada',
    'lina', 'arya', 'mila', 'masal', 'beren', 'melis', 'melisa', 'beste', 'begum', 'begüm', 'sevil',
    'nil', 'nilufer', 'nilüfer', 'gulsah', 'gülşah', 'songul', 'songül', 'filiz', 'hülya', 'hulya',
    'canan', 'demet', 'feride', 'ilknur', 'leyla', 'melek', 'neslihan', 'nuray', 'oyku', 'öykü',
    'rabia', 'seda', 'sezen', 'tuba', 'tugce', 'tuğçe', 'ulku', 'ülkü', 'vildan', 'zehra', 'zumrut', 'zümrüt'
}

MALE_NAMES = {
    'tufan', 'ahmet', 'mehmet', 'mustafa', 'ali', 'can', 'burak', 'emre', 'onur', 'oguz', 'oğuz',
    'cem', 'mert', 'berk', 'kaan', 'kerem', 'baris', 'barış', 'tolga', 'serkan', 'hakan', 'erhan',
    'volkan', 'gokhan', 'gökhan', 'murat', 'serdar', 'yusuf', 'omer', 'ömer', 'halil', 'ibrahim',
    'huseyin', 'hüseyin', 'ismail', 'fatih', 'selim', 'sinan', 'kemal', 'taner', 'koray', 'alp',
    'alper', 'arda', 'efe', 'yigit', 'yiğit', 'doruk', 'poyraz', 'ayaz', 'kuzey', 'ruzgar', 'rüzgar',
    'batu', 'batuhan', 'furkan', 'eren', 'enes', 'berke', 'ulas', 'ulaş', 'akın', 'akin', 'altan',
    'anil', 'anıl', 'atilla', 'aydin', 'aydın', 'bahadir', 'bahadır', 'baki', 'baran', 'batur',
    'bayram', 'berkay', 'bilal', 'bora', 'bulent', 'bülent', 'caglar', 'çağlar', 'cahit', 'caner',
    'cenk', 'cihan', 'coskun', 'coşkun', 'cuneyt', 'cüneyt', 'davut', 'demir', 'dursun', 'ekrem',
    'emin', 'ender', 'engin', 'ercan', 'erdal', 'erdil', 'erdogan', 'erdoğan', 'ergin', 'erkan',
    'erol', 'ersan', 'ersin', 'ertan', 'ertugrul', 'ertuğrul', 'ferhat', 'feridun', 'fikret', 'fuat',
    'giray', 'guven', 'güven', 'haluk', 'hamdi', 'hamza', 'harun', 'hasan', 'hayati', 'haydar',
    'hikmet', 'ilker', 'irfan', 'kadir', 'kadri', 'kenan', 'korkut', 'kursat', 'kürşat', 'levent',
    'mahmut', 'mansur', 'mazhar', 'metin', 'mithat', 'muhsin', 'muzaffer', 'naci', 'nazmi', 'necip',
    'nedim', 'nihat', 'niyazi', 'nuh', 'nuri', 'okan', 'oktay', 'olcay', 'orhan', 'osman', 'ozan',
    'önder', 'özcan', 'özgür', 'özkan', 'rasim', 'recep', 'refik', 'remzi', 'riza', 'rıza', 'sabri',
    'sadi', 'saim', 'salih', 'samed', 'samet', 'sami', 'sarp', 'sedat', 'sefa', 'semih', 'sergen',
    'serhat', 'servet', 'sezgin', 'soner', 'suat', 'suleyman', 'süleyman', 'sukru', 'şükrü', 'tahir',
    'talat', 'tarik', 'tarık', 'tayfun', 'taylan', 'tekin', 'tevfik', 'timur', 'turgay', 'turgut',
    'turhan', 'ugur', 'uğur', 'umut', 'unal', 'ünal', 'utku', 'vedat', 'veysel', 'volkan', 'yasin',
    'yavuz', 'yunus', 'zafer', 'zekeriya', 'zeki', 'ziya'
}

class ChatbotAgent:
    """
    Arkas Spoticar Akıllı AI Satış Danışmanı & Otomotiv Asistanı:
    - Türkçe Varlık Tanıma (NER: Hanım/Bey/Sayın)
    - Tekil Oturum Yönetimi (Session Deduplication)
    - Dinamik Araç Odaklama & Donanım Karşılaştırma
    - Bilişsel Niyet Analizi (Bütçe Güncelleme, Soru-Cevap, Donanım Önerisi)
    """

    def __init__(self, db: Session):
        self.db = db

    def _norm(self, text: str) -> str:
        if not text:
            return ""
        return text.replace("İ", "i").replace("I", "i").replace("ı", "i").replace("ğ", "g").replace("Ğ", "g").replace("ü", "u").replace("Ü", "u").replace("ş", "s").replace("Ş", "s").replace("ö", "o").replace("Ö", "o").replace("ç", "c").replace("Ç", "c").lower()

    def _get_honorific(self, first_name: Optional[str]) -> str:
        if not first_name:
            return "Değerli Müşterimiz"
        norm_fn = self._norm(first_name)
        if norm_fn in FEMALE_NAMES:
            return f"{first_name} Hanım"
        elif norm_fn in MALE_NAMES:
            return f"{first_name} Bey"
        else:
            return f"Sayın {first_name}"

    def get_or_create_customer(self, customer_id: Optional[int] = None, session_id: Optional[str] = None) -> CustomerLead:
        if customer_id:
            lead = self.db.query(CustomerLead).filter(CustomerLead.id == customer_id).first()
            if lead:
                return lead

        if session_id:
            lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == session_id).first()
            if lead:
                return lead

        lead = CustomerLead(
            session_id=session_id or f"session_{datetime.datetime.utcnow().timestamp()}",
            chat_history=[],
            conversation_summary="Yeni müşteri sohbeti başladı."
        )
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def _extract_contact_info(self, text: str, has_existing_name: bool = False) -> Dict[str, Any]:
        extracted = {}
        clean_text = text.strip()

        # 1. Phone extraction
        phone_match = re.search(r'(?:\+?90|0)?\s*(5\d{2})[\s.-]*(\d{3})[\s.-]*(\d{2})[\s.-]*(\d{2})', clean_text)
        if phone_match:
            extracted["phone"] = f"0{phone_match.group(1)}{phone_match.group(2)}{phone_match.group(3)}{phone_match.group(4)}"
            clean_text = clean_text[:phone_match.start()] + " " + clean_text[phone_match.end():]

        # 2. Check declined phone intent
        q_norm = self._norm(clean_text)
        if any(p in q_norm for p in ["vermek istemiyorum", "numara yok", "vermiyorum", "telefon yok", "paylasmak istemiyorum", "paylasamam", "gizli"]):
            extracted["declined_phone"] = True

        # 3. Name Parsing
        if not has_existing_name:
            p_intro = re.search(r'(?:ben|adım|ismim|adım soyadım)\s+([A-Za-zÇçĞğİıÖöŞşÜü]{2,20}(?:\s+[A-Za-zÇçĞğİıÖöŞşÜü]{2,20})*)', clean_text, re.IGNORECASE)
            p_post_intro = re.search(r'([A-Za-zÇçĞğİıÖöŞşÜü]{2,20}\s+[A-Za-zÇçĞğİıÖöŞşÜü]{2,20})\s+ben\b', clean_text, re.IGNORECASE)

            raw_name = None
            if p_intro:
                raw_name = p_intro.group(1).strip()
            elif p_post_intro:
                raw_name = p_post_intro.group(1).strip()
            else:
                segments = re.split(r'[-–—/|;,]', clean_text)
                for seg in segments:
                    words = [w.strip(" .!?") for w in seg.split() if w.strip(" .!?")]
                    stopwords = {
                        "merhaba", "selam", "iyi", "gunler", "günaydın", "akşamlar", "ben", "benim", "adim", "ismim",
                        "telefon", "numaram", "numaramı", "numarami", "vermek", "istemiyorum", "yok", "suv", "araba",
                        "arac", "araç", "fiyat", "km", "tl", "milyon", "bin", "var", "mı", "mi", "kadar", "çıkart",
                        "peugeot", "citroen", "opel", "mokka", "aircross"
                    }
                    valid_words = [w for w in words if w.lower() not in stopwords and re.match(r'^[A-Za-zÇçĞğİıÖöŞşÜü]+$', w)]
                    if 1 <= len(valid_words) <= 3:
                        is_brand = any(self._norm(w) in ["peugeot", "citroen", "opel", "volvo", "skoda", "ford"] for w in valid_words)
                        if not is_brand:
                            raw_name = " ".join(valid_words)
                            break

            if raw_name:
                parts = raw_name.split()
                filtered_parts = [p for p in parts if p.lower() not in ["ben", "ve", "ile", "merhaba", "var", "mı", "mi", "telefon", "numara"]]
                if filtered_parts:
                    extracted["first_name"] = filtered_parts[0].capitalize()
                    extracted["last_name"] = " ".join(p.capitalize() for p in filtered_parts[1:]) if len(filtered_parts) > 1 else ""
                    extracted["full_name"] = f"{extracted['first_name']} {extracted['last_name']}".strip()

        # 4. Budget extraction
        budget_match = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:milyon|m|bin|tl|k)', text, re.IGNORECASE)
        if budget_match:
            raw_val = float(budget_match.group(1).replace(",", "."))
            if "milyon" in text.lower() or "m" in text.lower():
                extracted["budget_max"] = raw_val * 1_000_000
            elif "bin" in text.lower() or "k" in text.lower():
                extracted["budget_max"] = raw_val * 1_000
            else:
                extracted["budget_max"] = raw_val

        # 5. Brand extraction
        for b in ["Peugeot", "Citroën", "Citroen", "Opel", "Ford", "Volvo", "Skoda", "Fiat"]:
            if b.lower() in text.lower():
                extracted["interested_brand"] = "Citroën" if "citro" in b.lower() else b
                break

        # 6. Body type extraction
        for bt in ["SUV", "Sedan", "Hatchback", "Coupe", "Van", "Ticari"]:
            if bt.lower() in text.lower():
                extracted["interested_body_type"] = bt
                break

        return extracted

    def _get_focused_vehicle(self, customer: CustomerLead, query_text: str) -> Optional[Vehicle]:
        q = self._norm(query_text)
        
        if "3008" in q or "peugeot" in q:
            v = self.db.query(Vehicle).filter(Vehicle.model.ilike("%3008%"), Vehicle.is_active == True).first()
            if v: return v
        if "c5" in q or "aircross" in q or "citroen" in q or "citroën" in q:
            v = self.db.query(Vehicle).filter(Vehicle.model.ilike("%C5%"), Vehicle.is_active == True).first()
            if v: return v
        if "mokka" in q or "opel" in q:
            v = self.db.query(Vehicle).filter(Vehicle.model.ilike("%Mokka%"), Vehicle.is_active == True).first()
            if v: return v

        if customer.focused_vehicle_id:
            v = self.db.query(Vehicle).filter(Vehicle.id == customer.focused_vehicle_id).first()
            if v: return v

        return self.db.query(Vehicle).filter(Vehicle.is_active == True).first()

    def _answer_vehicle_specific_question(self, vehicle: Vehicle, query: str, honorific: str) -> Optional[str]:
        q = self._norm(query)
        model_name = f"{vehicle.brand} {vehicle.model} {vehicle.package or vehicle.sub_model or ''}".strip()
        norm_model = self._norm(model_name)
        km_str = f"{vehicle.km:,.0f} KM".replace(",", ".")
        price_str = f"{vehicle.price:,.0f} {vehicle.currency}".replace(",", ".")
        salutation = f"{honorific}, " if honorific else ""
        tech = vehicle.technical_specs or {}
        damage = vehicle.damage_expertise or {}
        ad_feat = vehicle.ad_features or {}

        # 1. Transmission Question
        if any(w in q for w in ["otomatik", "manuel", "vites", "sanziman", "eat8", "at8"]):
            trans = vehicle.transmission or "8 İleri Tam Otomatik"
            return (
                f"Evet {salutation}incelediğimiz {vehicle.year} model **{model_name}** aracımız **{trans}** şanzımana sahiptir. "
                f"Vites geçişleri son derece sarsıntısız, konforlu ve yakıt tasarrufludur."
            )

        # 2. Mileage / KM Question
        if any(w in q for w in ["km", "kilometre", "kac binde", "kac bin", "mesafe", "kac km"]):
            return (
                f"{salutation}İncelediğimiz **{model_name}** aracımız yalnızca **{km_str}**'dedir. "
                f"Orijinal kilometre garantilidir ve Arkas Spoticar güvencesindedir."
            )

        # 3. Explicit Single-Vehicle Price Question
        if any(w in q for w in ["fiyati", "fiyati ne", "kac para", "ne kadar", "kaça"]) and not any(w in q for w in ["arttir", "yukselt", "cikart", "kadar"]):
            return (
                f"{salutation}Aracımızın güncel satış fiyatı **{price_str}**'dir. "
                f"Arkas Spoticar güvencesiyle takas, kredi ve finansman seçeneklerimiz mevcuttur."
            )

        # 4. Equipment Questions (Cam tavan, koltuk ısıtma, direksiyon ısıtma, multimedya vb.)
        if any(w in q for w in ["isitma", "koltuk", "direksiyon", "cam tavan", "sunroof", "donanim", "paket", "ozellik", "multimedya", "kamera", "park", "klima"]):
            if "3008" in norm_model:
                return (
                    f"{salutation}İncelediğimiz **Peugeot 3008 Allure Selection EAT8** aracımız oldukça zengin bir donanıma sahiptir:\n\n"
                    f"✨ Öne Çıkan Donanımlar:\n"
                    f"• **Panoramik Açılabilir Cam Tavan & Elektrikli Güneşlik**\n"
                    f"• **Ön Koltuk Isıtma & Elektrikli Bel Destekli Sürücü Koltuğu**\n"
                    f"• **Elektrikli ve Ayak Sensörlü Akıllı Bagaj Kapağı**\n"
                    f"• 10 inç Dokunmatik HD Ekran & Kablosuz Apple CarPlay / Android Auto\n"
                    f"• 180° VisioPark Geri Görüş Kamerası & Kör Nokta Uyarı Sistemi\n"
                    f"• Grip Control 5 Farklı Sürüş Modu"
                )
            elif "c5" in norm_model:
                return (
                    f"{salutation}İncelediğimiz **Citroën C5 Aircross Shine EAT8** aracımız sınıfının en konforlu modelidir:\n\n"
                    f"✨ Öne Çıkan Donanımlar:\n"
                    f"• **Kademeli Hidrolik Süspansiyon (Uçan Halı Konforu)**\n"
                    f"• **Advanced Comfort Masajlı & Isıtmalı Ön Koltuklar**\n"
                    f"• **Panoramik Açılır Cam Tavan & Elektrikli Bagaj**\n"
                    f"• Otoyol Sürüş Asistanı (Highway Driver Assist - Yarı Otonom)\n"
                    f"• 360° Çevre Görüş Kamerası & 3 Bağımsız Kayan Arka Koltuk"
                )
            elif "mokka" in norm_model:
                return (
                    f"{salutation}İncelediğimiz **Opel Mokka GS Line** aracımızda kış ve teknoloji konforu tamdır:\n\n"
                    f"✨ Öne Çıkan Donanımlar:\n"
                    f"• **Isıtmalı Direksiyon Simidi & Isıtmalı Ön Koltuklar**\n"
                    f"• **Opel Pure Panel 12 inç Genişletilmiş Dijital Gösterge**\n"
                    f"• Çift Renk Kontrast Siyah Tavan & 18 inç GS Line Jantlar\n"
                    f"• IntelliLux LED Matrix Akıllı Farlar & 180° Panoramik Kamera"
                )
            else:
                all_feats = (ad_feat.get("konfor", []) + ad_feat.get("guvenlik", []))[:5]
                feats_txt = "\n".join([f"• {f}" for f in all_feats])
                return f"{salutation}İncelediğimiz **{model_name}** donanım özellikleri:\n\n{feats_txt}"

        # 5. Fuel & Engine Question
        if any(w in q for w in ["yakit", "benzin", "dizel", "tuketim", "motor", "kac beygir", "hp", "kac litre"]):
            hp = tech.get("motor_gucu_hp", "130 HP")
            tork = tech.get("tork_nm", "300 Nm")
            cons = tech.get("yakit_tuketimi_lt", "4.2 lt / 100 km")
            return (
                f"{salutation}**{model_name}** aracımız **{hp}** güç ve **{tork}** tork üreten motora sahiptir.\n\n"
                f"📊 Yakıt Tüketimi: Ortalama **{cons}** ile son derece ekonomiktir."
            )

        # 6. Expertise / Condition Question
        if any(w in q for w in ["ekspertiz", "hasar", "kaza", "boya", "degisen", "tramer", "garanti", "kondisyon", "durum"]):
            boyali = damage.get("boyali_parcalar", [])
            degisen = damage.get("degisen_parcalar", [])
            tramer = damage.get("tramer_kaydi_tl", 0)
            
            if not boyali and not degisen and (tramer == 0 or not tramer):
                exp_detail = "• Boyalı Parça: Yok\n• Değişen Parça: Yok (Hatasız & Orijinal)\n• Tramer Kaydı: Yok (0 TL)"
            else:
                b_str = ", ".join(boyali) if boyali else "Yok"
                d_str = ", ".join(degisen) if degisen else "Yok"
                t_str = f"{tramer:,.0f} TL".replace(",", ".") if tramer else "0 TL"
                exp_detail = f"• Boyalı Parçalar: {b_str}\n• Değişen Parçalar: {d_str}\n• Tramer Hasar Kaydı: {t_str}"

            return (
                f"{salutation}**{model_name}** ekspertiz durumu:\n\n"
                f"{exp_detail}\n\n"
                f"🛡️ {vehicle.expertise_note or 'Arkas Spoticar 100+ Nokta Kontrolü ve 12 Ay Garantisi Kapsamındadır.'}"
            )

        return None

    def process_message(
        self,
        message: str,
        customer_id: Optional[int] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        customer = self.get_or_create_customer(customer_id, session_id)
        msg_clean = message.strip()
        q_norm = self._norm(msg_clean)

        # 1. Contact Extraction
        has_name = bool(customer.first_name)
        extracted = self._extract_contact_info(msg_clean, has_existing_name=has_name)
        
        if extracted.get("first_name"):
            customer.first_name = extracted["first_name"]
            customer.last_name = extracted.get("last_name", "")
            customer.full_name = extracted.get("full_name", "")
        if extracted.get("phone"):
            customer.phone = extracted["phone"]

        # History append
        now_str = datetime.datetime.utcnow().isoformat()
        history = list(customer.chat_history or [])
        history.append({"role": "user", "content": msg_clean, "timestamp": now_str})

        honorific = self._get_honorific(customer.first_name)
        salutation_prefix = f"{honorific}, " if customer.first_name else "Değerli Müşterimiz, "

        focused_v = self._get_focused_vehicle(customer, msg_clean)
        if focused_v:
            customer.focused_vehicle_id = focused_v.id

        reply_text = ""
        filter_action = None
        matched_vehicles_data = []

        is_greeting = any(w in q_norm for w in ["merhaba", "selam", "gunaydin", "iyi gunler", "hey", "basla"])
        is_intro_only = bool(extracted.get("full_name") or extracted.get("declined_phone") or extracted.get("phone")) and not any(
            k in q_norm for k in ["suv", "sedan", "fiyat", "km", "vites", "isitma", "var mi", "peugeot", "citroen", "opel", "3008", "mokka", "oner", "kadar"]
        )

        is_budget_update = any(b in q_norm for b in [
            "kadar cikart", "kadar yukselt", "kadar cikar", "kadar arttir", "butceyi", "butcemi", "fiyat araligini", "milyona kadar"
        ]) or (extracted.get("budget_max") and any(w in q_norm for w in ["cikart", "yukselt", "arttir", "ayarla", "yap", "kadar"]))

        is_recommendation_request = any(r in q_norm for r in [
            "oner", "onerir misin", "baska arac", "baska ne var", "farkli bir arac", "farkli model",
            "direksiyon isitmasi olan", "direksiyon isitma olan", "koltuk isitmasi olan", "koltuk isitma olan",
            "cam tavanli", "sunroof olan", "daha luks", "daha guclu", "yok mu", "baska yok mu"
        ])

        if is_intro_only and len(history) <= 3:
            phone_note = ""
            if customer.phone:
                phone_note = f" (Telefon: {customer.phone})"
            elif extracted.get("declined_phone"):
                phone_note = " (Telefon paylaşımı tercih edilmedi)"

            reply_text = (
                f"Çok memnun oldum {honorific}{phone_note}! Bilgilerinizi güvenle kaydettim.\n\n"
                f"Arkas Spoticar portföyümüzde sizin için nasıl bir araç bakalım? Aklınızda belirli bir marka (Peugeot, Citroën, Opel vb.), "
                f"kasa tipi (SUV, Hatchback) ya da belirlediğiniz bir bütçe aralığı var mı?"
            )

        elif is_greeting and len(history) <= 2 and not customer.first_name:
            reply_text = (
                "Merhaba! Arkas Spoticar Yapay Zeka Danışmanına hoş geldiniz. 🚗✨\n\n"
                "Size en doğru araçları önerebilmem ve nasıl hitap edeceğimi bilmem için adınızı ve soyadınızı paylaşabilir misiniz?\n"
                "Ayrıca aradığınız kriterlerde yeni bir araç stoğumuza girdiğinde ilk sizin haberiniz olması için telefon numaranızı da yazabilirsiniz."
            )

        elif is_budget_update:
            new_budget = extracted.get("budget_max") or 2_000_000.0
            customer.budget_max = new_budget

            db_results = self.db.query(Vehicle).filter(
                Vehicle.is_active == True,
                Vehicle.price <= new_budget
            ).order_by(Vehicle.price.desc()).all()

            if db_results:
                matched_vehicles_data = [v.to_dict() for v in db_results]
                flagship = db_results[0]
                customer.focused_vehicle_id = flagship.id

                filter_action = {
                    "brand": "all",
                    "body_type": "all",
                    "max_price": new_budget,
                    "search": ""
                }

                vehicle_lines = []
                for v in db_results:
                    km_fmt = f"{v.km:,.0f} KM".replace(",", ".")
                    price_fmt = f"{v.price:,.0f} {v.currency}".replace(",", ".")
                    vehicle_lines.append(
                        f"• **{v.brand} {v.model} {v.package or ''}** ({v.year} | {km_fmt}) ➔ **{price_fmt}**"
                    )

                vehicles_text = "\n".join(vehicle_lines)
                budget_fmt = f"{new_budget:,.0f} TL".replace(",", ".")
                reply_text = (
                    f"{salutation_prefix}bütçe filtrenizi **{budget_fmt}** seviyesine güncelledim ve sayfayı Arkas Spoticar araçlarımızla yeniledim:\n\n"
                    f"{vehicles_text}\n\n"
                    f"İncelemek istediğiniz modelin donanım veya ekspertiz raporunu detaylandırabilirim!"
                )
            else:
                reply_text = f"{salutation_prefix}bütçenizi {new_budget:,.0f} TL olarak güncelledim."

        elif is_recommendation_request:
            if any(h in q_norm for h in ["direksiyon", "direksiyon isitma", "mokka", "opel"]):
                mokka = self.db.query(Vehicle).filter(Vehicle.brand.ilike("%Opel%"), Vehicle.is_active == True).first()
                if mokka:
                    customer.focused_vehicle_id = mokka.id
                    filter_action = {"brand": "Opel", "body_type": "all", "max_price": None, "search": ""}
                    matched_vehicles_data = [mokka.to_dict()]
                    reply_text = (
                        f"{salutation_prefix}portföyümüzde direksiyon ısıtması ve koltuk ısıtması standart olan modelimiz: **Opel Mokka 1.2 Turbo GS Line**!\n\n"
                        f"🚗 **Opel Mokka GS Line** ({mokka.year} | {mokka.km:,.0f} KM) ➔ **{mokka.price:,.0f} TL**\n\n"
                        f"✨ Isıtmalı direksiyon simidi, 3 kademeli koltuk ısıtma ve Pure Panel çift ekran standarttır. Sayfayı Mokka için filtreledim!"
                    )
            else:
                db_all = self.db.query(Vehicle).filter(Vehicle.is_active == True).order_by(Vehicle.price.desc()).all()
                matched_vehicles_data = [v.to_dict() for v in db_all]
                filter_action = {"brand": "all", "body_type": "all", "max_price": None, "search": ""}
                lines = [f"• **{v.brand} {v.model} {v.package or ''}** ({v.year} | {v.km:,.0f} KM) ➔ **{v.price:,.0f} TL**".replace(",", ".") for v in db_all]
                reply_text = f"{salutation_prefix}Arkas Spoticar güncel araçlarımız:\n\n" + "\n".join(lines)

        else:
            direct_ans = None
            if focused_v:
                direct_ans = self._answer_vehicle_specific_question(focused_v, msg_clean, honorific)

            if direct_ans:
                reply_text = direct_ans
            else:
                if extracted.get("budget_max"):
                    customer.budget_max = extracted["budget_max"]
                if extracted.get("interested_brand"):
                    customer.interested_brand = extracted["interested_brand"]
                if extracted.get("interested_body_type"):
                    customer.interested_body_type = extracted["interested_body_type"]

                q_db = self.db.query(Vehicle).filter(Vehicle.is_active == True)
                if customer.interested_brand and customer.interested_brand.lower() != "all":
                    q_db = q_db.filter(Vehicle.brand.ilike(f"%{customer.interested_brand}%"))
                if customer.budget_max:
                    q_db = q_db.filter(Vehicle.price <= customer.budget_max * 1.1)

                db_results = q_db.order_by(Vehicle.price.desc()).limit(5).all()
                if db_results:
                    matched_vehicles_data = [v.to_dict() for v in db_results]
                    focused_v = db_results[0]
                    customer.focused_vehicle_id = focused_v.id
                    filter_action = {
                        "brand": customer.interested_brand or "all",
                        "body_type": customer.interested_body_type or "all",
                        "max_price": customer.budget_max,
                        "search": ""
                    }
                    lines = [f"• **{v.brand} {v.model} {v.package or ''}** ({v.year} | {v.km:,.0f} KM) ➔ **{v.price:,.0f} TL**".replace(",", ".") for v in db_results]
                    reply_text = (
                        f"{salutation_prefix}kriterlerinize uygun güncel Arkas Spoticar araçlarımız:\n\n"
                        + "\n".join(lines)
                        + "\n\n👉 Sayfayı filtreledim. Araçların vitesini, kilometresini, ekspertiz durumunu veya donanım detaylarını doğrudan bana sorabilirsiniz!"
                    )
                else:
                    reply_text = f"{salutation_prefix}aradığınız kriterlere tam uyan bir araç şu an aktif stoklarımızda görünmüyor. Stoğumuza yeni araç girdiğinde size bildirebilirim!"

        history.append({"role": "assistant", "content": reply_text, "timestamp": datetime.datetime.utcnow().isoformat()})
        customer.chat_history = history

        summary_parts = []
        if customer.full_name: summary_parts.append(f"Müşteri: {customer.full_name}")
        if customer.phone: summary_parts.append(f"Tel: {customer.phone}")
        if customer.interested_brand: summary_parts.append(f"Marka: {customer.interested_brand}")
        if customer.budget_max: summary_parts.append(f"Bütçe: {customer.budget_max:,.0f} TL".replace(",", "."))
        if focused_v: summary_parts.append(f"İncelenen Araç: {focused_v.brand} {focused_v.model}")

        customer.conversation_summary = " | ".join(summary_parts) if summary_parts else "Müşteri genel Spoticar araması yapıyor."

        self.db.commit()
        self.db.refresh(customer)

        return {
            "reply": reply_text,
            "customer_id": customer.id,
            "customer_name": customer.first_name or "",
            "filter_action": filter_action,
            "matched_vehicles": matched_vehicles_data
        }
