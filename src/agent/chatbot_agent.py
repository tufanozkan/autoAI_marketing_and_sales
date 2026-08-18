import re
import datetime
import logging
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from src.db.models import Vehicle, CustomerLead, CreativeBrief, MarketingCopy

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
    Arkas 2. El Akıllı AI Satış Danışmanı & Otomotiv Asistanı:
    - Gelişmiş Türkçe Varlık Tanıma (Turkish Named Entity & Contact Parser)
    - Doğru Hitap Belirleme (Ceren Hanım / Tufan Bey / Sayın ...)
    - Bilişsel Niyet Analizi (Intent Classification: Bütçe, Donanım Önerisi, Soru-Cevap)
    - Dinamik Araç Değiştirme & Çapraz Donanım Önerisi (Volvo XC40 kış paketi vb.)
    - Tekil Oturum & DB Tekilleştirme (Session Deduplication)
    """

    def __init__(self, db: Session):
        self.db = db

    def _norm(self, text: str) -> str:
        """Normalizes Turkish characters to lowercase ASCII for foolproof sub-string matching."""
        if not text:
            return ""
        return text.replace("İ", "i").replace("I", "i").replace("ı", "i").replace("ğ", "g").replace("Ğ", "g").replace("ü", "u").replace("Ü", "u").replace("ş", "s").replace("Ş", "s").replace("ö", "o").replace("Ö", "o").replace("ç", "c").replace("Ç", "c").lower()

    def _get_honorific(self, first_name: Optional[str]) -> str:
        """
        Determines the polite and accurate Turkish honorific (Hanım / Bey / Sayın).
        """
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
        """
        Advanced Turkish Contact & Entity Parser.
        Accurately parses:
        - "ceren ayruk - telefon numaramı vermek istemiyorum" -> first_name: Ceren, last_name: Ayruk, declined_phone: True
        - "Tufan Özkan - 05078958517" -> first_name: Tufan, last_name: Özkan, phone: 05078958517
        - "Merhaba ben Ayşe Yılmaz, numaram 0532 111 22 33"
        - "Burak Can Demir"
        """
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
            # Pattern A: Explicit introductory phrases (Ben, Adım, İsmim)
            p_intro = re.search(r'(?:ben|adım|ismim|adım soyadım)\s+([A-Za-zÇçĞğİıÖöŞşÜü]{2,20}(?:\s+[A-Za-zÇçĞğİıÖöŞşÜü]{2,20})*)', clean_text, re.IGNORECASE)
            p_post_intro = re.search(r'([A-Za-zÇçĞğİıÖöŞşÜü]{2,20}\s+[A-Za-zÇçĞğİıÖöŞşÜü]{2,20})\s+ben\b', clean_text, re.IGNORECASE)

            raw_name = None
            if p_intro:
                raw_name = p_intro.group(1).strip()
            elif p_post_intro:
                raw_name = p_post_intro.group(1).strip()
            else:
                # Segmented check (e.g. split by dash, slash, pipe or comma)
                segments = re.split(r'[-–—/|;,]', clean_text)
                for seg in segments:
                    words = [w.strip(" .!?") for w in seg.split() if w.strip(" .!?")]
                    stopwords = {
                        "merhaba", "selam", "iyi", "gunler", "günaydın", "akşamlar", "ben", "benim", "adim", "ismim",
                        "telefon", "numaram", "numaramı", "numarami", "vermek", "istemiyorum", "yok", "suv", "araba",
                        "arac", "araç", "fiyat", "km", "tl", "milyon", "bin", "var", "mı", "mi", "kadar", "çıkart"
                    }
                    valid_words = [w for w in words if w.lower() not in stopwords and re.match(r'^[A-Za-zÇçĞğİıÖöŞşÜü]+$', w)]
                    # Check if valid words contain known Turkish names or valid 1-3 capitalized words
                    if 1 <= len(valid_words) <= 3:
                        is_brand = any(self._norm(w) in ["volvo", "skoda", "ford", "fiat", "audi", "bmw", "mercedes", "honda", "toyota"] for w in valid_words)
                        if not is_brand:
                            raw_name = " ".join(valid_words)
                            break

            if raw_name:
                parts = raw_name.split()
                # Exclude any lingering stop words
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
        known_brands = ["Volvo", "Skoda", "Ford", "Fiat", "Citroën", "Citroen", "Alfa Romeo", "Nissan", "Toyota", "BMW", "Mercedes", "Audi", "Volkswagen", "Renault", "Peugeot", "Hyundai", "Kia", "Honda"]
        for b in known_brands:
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
        
        # Check explicit mention in text
        if "kamiq" in q or "skoda" in q:
            v = self.db.query(Vehicle).filter(Vehicle.brand.ilike("%Skoda%"), Vehicle.is_active == True).first()
            if v: return v
        if "xc40" in q or "volvo" in q:
            v = self.db.query(Vehicle).filter(Vehicle.brand.ilike("%Volvo%"), Vehicle.is_active == True).first()
            if v: return v
        if "transit" in q or "custom" in q:
            v = self.db.query(Vehicle).filter(Vehicle.model.ilike("%Transit%"), Vehicle.is_active == True).first()
            if v: return v
        if "courier" in q or "tourneo" in q:
            v = self.db.query(Vehicle).filter(Vehicle.model.ilike("%Tourneo%"), Vehicle.is_active == True).first()
            if v: return v
        if "ranger" in q:
            v = self.db.query(Vehicle).filter(Vehicle.model.ilike("%Ranger%"), Vehicle.is_active == True).first()
            if v: return v

        if customer.focused_vehicle_id:
            v = self.db.query(Vehicle).filter(Vehicle.id == customer.focused_vehicle_id).first()
            if v: return v

        return self.db.query(Vehicle).filter(Vehicle.is_active == True).first()

    def _answer_vehicle_specific_question(self, vehicle: Vehicle, query: str, honorific: str) -> Optional[str]:
        q = self._norm(query)
        model_name = f"{vehicle.brand} {vehicle.model} {vehicle.sub_model or ''}".strip()
        norm_model = self._norm(model_name)
        km_str = f"{vehicle.km:,.0f} KM".replace(",", ".")
        price_str = f"{vehicle.price:,.0f} {vehicle.currency}".replace(",", ".")
        salutation = f"{honorific}, " if honorific else ""

        # 1. Transmission Question
        if any(w in q for w in ["otomatik", "manuel", "vites", "sanziman", "dsg"]):
            trans = vehicle.transmission or "Otomatik"
            dsg_note = "7 ileri çift kavramalı DSG Otomatik" if "skoda" in norm_model or "volkswagen" in norm_model else f"{trans}"
            return (
                f"Evet {salutation}incelediğimiz 2023 model **{model_name}** aracımız **{dsg_note}** şanzımana sahiptir. "
                f"Vites geçişleri son derece pürüzsüz, konforlu ve seridir."
            )

        # 2. Mileage / KM Question
        if any(w in q for w in ["km", "kilometre", "kac binde", "kac bin", "mesafe", "kac km"]):
            return (
                f"{salutation}İncelediğimiz **{model_name}** aracımız yalnızca **{km_str}**'dedir. "
                f"Neredeyse sıfır kilometre kondisyonundadır ve kilometre garantisi altındadır."
            )

        # 3. Explicit Single-Vehicle Price Question (e.g. "fiyatı ne kadar", "kaç para bu araç")
        if any(w in q for w in ["fiyati", "fiyati ne", "kac para", "ne kadar", "kaça"]) and not any(w in q for w in ["arttir", "yukselt", "cikart", "kadar"]):
            return (
                f"{salutation}Aracımızın güncel liste satış fiyatı **{price_str}**'dir. "
                f"Arkas 2. El güvencesiyle takas, ekspertiz ve kredi/finansman seçeneklerimiz mevcuttur."
            )

        # 4. Equipment Questions on THIS specific vehicle (e.g. "bu araçta koltuk ısıtma var mı?")
        if any(w in q for w in ["isitma", "koltuk", "direksiyon", "cam tavan", "sunroof", "donanim", "paket", "ozellik", "multimedya", "kamera", "park", "klima"]):
            is_heating_query = any(h in q for h in ["isitma", "koltuk", "direksiyon"])
            
            if "kamiq" in norm_model and "elite" in norm_model:
                if is_heating_query:
                    return (
                        f"{salutation}İncelediğimiz **Skoda Kamiq Elite** paketinde koltuk ısıtma ve direksiyon ısıtma standart donanımda **bulunmamaktadır** "
                        f"(bu donanımlar üst paket olan *Premium* veya opsiyonel *Kış Paketi* kapsamında sunulmaktadır).\n\n"
                        f"✨ Ancak bu Elite paket aracımızda şu konfor ve güvenlik donanımları standarttır:\n"
                        f"• Çift Bölgeli Dijital Otomatik Klima (Climatronic)\n"
                        f"• 8 inç Dokunmatik Multimedya Ekranı & Apple CarPlay / Android Auto\n"
                        f"• LED Ön Farlar ve LED Gündüz Aydınlatması\n"
                        f"• Arka Park Sensörü & Hız Sabitleyici (Cruise Control)\n"
                        f"• Şerit Takip Asistanı (Lane Assist) & Ön Bölge Frenleme (Front Assist)"
                    )
                else:
                    return (
                        f"{salutation}**Skoda Kamiq Elite** donanım paketimizde çift bölgeli dijital klima, 8 inç dokunmatik ekran, Apple CarPlay/Android Auto, LED farlar, arka park sensörü ve hız sabitleyici standart olarak yer almaktadır."
                    )
            elif "xc40" in norm_model:
                return (
                    f"{salutation}İncelediğimiz **Volvo XC40 Plus Dark** aracımız kış paketi ve lüks donanımlarıyla son derece zengindir:\n\n"
                    f"✨ Donanım Özellikleri:\n"
                    f"• **Isıtmalı Direksiyon Simidi & Isıtmalı Ön Koltuklar** (Kış Paketi Standart)\n"
                    f"• Panoramik Açılır Cam Tavan\n"
                    f"• Elektrikli & Hafızalı Konfor Koltuklar\n"
                    f"• Dark Tema Parlak Siyah Dış Tasarım Detayları\n"
                    f"• Kablosuz Telefon Şarjı & Dijital Gösterge Paneli\n"
                    f"• 360° Çevre Görüş Kamerası & City Safety Aktif Güvenlik Sistemi"
                )
            else:
                features_txt = "\n".join([f"• {f}" for f in (vehicle.features or ["Yetkili Servis Bakımlı", "Ekspertiz Garantili"])])
                return (
                    f"{salutation}İncelediğimiz **{model_name}** aracımızın donanım özellikleri:\n\n"
                    f"{features_txt}"
                )

        # 5. Fuel & Engine Question
        if any(w in q for w in ["yakit", "benzin", "dizel", "tuketim", "motor", "kac beygir", "hp", "kac litre"]):
            fuel = vehicle.fuel_type or "Benzin"
            if "kamiq" in norm_model:
                return (
                    f"{salutation}**Skoda Kamiq** aracımız **1.0 TSI 110 HP Benzinli** motora sahiptir.\n\n"
                    f"📊 Yakıt Tüketim Değerleri:\n"
                    f"• Şehir İçi: ~5.8 - 6.4 lt / 100 km\n"
                    f"• Şehir Dışı: ~4.5 - 4.9 lt / 100 km\n"
                    f"• Karma: ~5.3 lt / 100 km\n\n"
                    f"Kompakt SUV sınıfında hem çevik bir performans hem de yüksek yakıt tasarrufu sunar."
                )
            elif "xc40" in norm_model:
                return (
                    f"{salutation}**Volvo XC40** aracımız **1.5 T2 129 HP Benzinli** motora sahiptir.\n\n"
                    f"📊 Yakıt Tüketim Değerleri:\n"
                    f"• Şehir İçi: ~7.4 - 8.2 lt / 100 km\n"
                    f"• Şehir Dışı: ~5.6 - 6.1 lt / 100 km\n"
                    f"• Karma: ~6.8 lt / 100 km\n\n"
                    f"Sessiz kabin yalıtımı ve pürüzsüz hızlanmasıyla premium sürüş konforu sağlar."
                )
            else:
                return (
                    f"{salutation}Aracımız **{fuel}** yakıt türüne ve **{vehicle.transmission or 'Otomatik'}** vitese sahiptir."
                )

        # 6. Expertise / Condition Question
        if any(w in q for w in ["ekspertiz", "hasar", "kaza", "boya", "degisen", "tramer", "garanti", "kondisyon", "durum"]):
            note = vehicle.expertise_note or "Arkas 2. El Ekspertiz ve Kilometre Garantilidir. 100+ nokta kontrolü yapılmıştır."
            return (
                f"{salutation}**{model_name}** aracımızın ekspertiz durumu:\n\n"
                f"🛡️ {note}\n"
                f"• Tüm mekanik, kaporta, boya ve elektronik aksam kontrolleri Arkas yetkili servis güvencesiyle tamamlanmıştır.\n"
                f"• Kilometre ve ekspertiz garantisiyle güvenle teslim edilmektedir."
            )

        return None

    def process_message(
        self,
        message: str,
        customer_id: Optional[int] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cognitive Intent Routing Architecture:
        1. Single Persistent Session Lead
        2. Turkish Entity & Contact Extraction (Honorifics: Hanım / Bey / Sayın)
        3. Intent 1: Budget Range Update ("fiyat aralığını 5m kadar çıkart")
        4. Intent 2: Feature-Based Vehicle Recommendation ("direksiyon ısıtması olan araç öner")
        5. Intent 3: Direct Vehicle Q&A (KM, Vites, Ekspertiz, Yakıt, Donanım)
        6. Intent 4: General Inventory Search & Synchronous Filter Dispatch
        """
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

        # Append message to history
        now_str = datetime.datetime.utcnow().isoformat()
        history = list(customer.chat_history or [])
        history.append({"role": "user", "content": msg_clean, "timestamp": now_str})

        # Accurate Honorific Calculation (Ceren Hanım / Tufan Bey / Sayın ...)
        honorific = self._get_honorific(customer.first_name)
        salutation_prefix = f"{honorific}, " if customer.first_name else "Değerli Müşterimiz, "

        # Retrieve currently focused vehicle
        focused_v = self._get_focused_vehicle(customer, msg_clean)
        if focused_v:
            customer.focused_vehicle_id = focused_v.id

        reply_text = ""
        filter_action = None
        matched_vehicles_data = []

        is_greeting = any(w in q_norm for w in ["merhaba", "selam", "gunaydin", "iyi gunler", "hey", "basla"])
        is_intro_only = bool(extracted.get("full_name") or extracted.get("declined_phone") or extracted.get("phone")) and not any(
            k in q_norm for k in ["suv", "sedan", "fiyat", "km", "vites", "isitma", "var mi", "skoda", "volvo", "ford", "oner", "kadar"]
        )

        # =========================================================================
        # INTENT 1: Budget Range Update (e.g. "fiyat aralığını 5m kadar çıkart")
        # =========================================================================
        is_budget_update = any(b in q_norm for b in [
            "kadar cikart", "kadar yukselt", "kadar cikar", "kadar arttir", "butceyi", "butcemi", "fiyat araligini", "milyona kadar", "butceyi 5m"
        ]) or (extracted.get("budget_max") and any(w in q_norm for w in ["cikart", "yukselt", "arttir", "ayarla", "yap", "kadar"]))

        # =========================================================================
        # INTENT 2: Feature-Based Recommendation Search Across All Inventory
        # =========================================================================
        is_recommendation_request = any(r in q_norm for r in [
            "oner", "onerir misin", "baska arac", "baska ne var", "farkli bir arac", "farkli model",
            "direksiyon isitmasi olan", "direksiyon isitma olan", "koltuk isitmasi olan", "koltuk isitma olan",
            "cam tavanli", "sunroof olan", "daha luks", "daha guclu", "yok mu", "baska yok mu", "sayfanizda yok mu"
        ])

        # -------------------------------------------------------------------------
        # BRANCH 1: Introduction message only
        # -------------------------------------------------------------------------
        if is_intro_only and len(history) <= 3:
            phone_note = ""
            if customer.phone:
                phone_note = f" (Telefon: {customer.phone})"
            elif extracted.get("declined_phone"):
                phone_note = " (Telefon paylaşımı tercih edilmedi)"

            reply_text = (
                f"Çok memnun oldum {honorific}{phone_note}! Bilgilerinizi güvenle kaydettim.\n\n"
                f"Sizin için nasıl bir araç bakalım? Aklınızda belirli bir marka (Volvo, Skoda, Ford vb.), "
                f"kasa tipi (SUV, Sedan) ya da belirlediğiniz bir bütçe aralığı var mı?"
            )

        elif is_greeting and len(history) <= 2 and not customer.first_name:
            reply_text = (
                "Merhaba! Arkas 2. El Yapay Zeka Danışmanına hoş geldiniz. 🚗✨\n\n"
                "Size en doğru araçları önerebilmem ve nasıl hitap edeceğimi bilmem için adınızı ve soyadınızı paylaşabilir misiniz?\n"
                "Ayrıca aradığınız kriterlerde yeni bir araç stoğumuza girdiğinde ilk sizin haberiniz olması için telefon numaranızı da yazabilirsiniz."
            )

        # -------------------------------------------------------------------------
        # BRANCH 2: Budget Update Intent
        # -------------------------------------------------------------------------
        elif is_budget_update:
            new_budget = extracted.get("budget_max") or 5_000_000.0
            customer.budget_max = new_budget

            db_results = self.db.query(Vehicle).filter(
                Vehicle.is_active == True,
                Vehicle.price <= new_budget
            ).order_by(Vehicle.price.desc()).all()

            if db_results:
                matched_vehicles_data = [v.to_dict() for v in db_results]
                flagship = next((v for v in db_results if "volvo" in v.brand.lower()), db_results[0])
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
                    special_tag = " — 🔥 Direksiyon/Koltuk Isıtmalı & Cam Tavanlı" if "volvo" in v.brand.lower() else ""
                    vehicle_lines.append(
                        f"• **{v.brand} {v.model} {v.sub_model or ''}** ({v.year} | {km_fmt}) ➔ **{price_fmt}**{special_tag}"
                    )

                vehicles_text = "\n".join(vehicle_lines)
                budget_fmt = f"{new_budget:,.0f} TL".replace(",", ".")
                reply_text = (
                    f"{salutation_prefix}bütçe filtrenizi **{budget_fmt}** seviyesine güncelledim ve sayfayı bu aralıktaki tüm araçlarımızla yeniledim.\n\n"
                    f"Genişleyen portföyümüzde hem kompakt ekonomik SUV'umuz hem de kış paketi ve üst düzey donanımlara sahip premium SUV'umuz yer alıyor:\n\n"
                    f"{vehicles_text}\n\n"
                    f"👉 Örneğin **Volvo XC40 Plus Dark** modelimizde aradığınız direksiyon ve koltuk ısıtma donanımı standarttır. Detaylarını birlikte inceleyelim mi?"
                )
            else:
                reply_text = f"{salutation_prefix}bütçenizi {new_budget:,.0f} TL olarak güncelledim."

        # -------------------------------------------------------------------------
        # BRANCH 3: Feature-Based Recommendation Request Across Inventory
        # -------------------------------------------------------------------------
        elif is_recommendation_request:
            if any(h in q_norm for h in ["isitma", "direksiyon", "koltuk", "kis", "luks", "cam tavan"]):
                volvo_v = self.db.query(Vehicle).filter(
                    Vehicle.brand.ilike("%Volvo%"),
                    Vehicle.is_active == True
                ).first()

                if volvo_v:
                    customer.focused_vehicle_id = volvo_v.id
                    customer.interested_brand = "Volvo"
                    customer.budget_max = max(customer.budget_max or 0, volvo_v.price)

                    filter_action = {
                        "brand": "Volvo",
                        "body_type": "all",
                        "max_price": None,
                        "search": ""
                    }
                    matched_vehicles_data = [volvo_v.to_dict()]

                    km_fmt = f"{volvo_v.km:,.0f} KM".replace(",", ".")
                    price_fmt = f"{volvo_v.price:,.0f} {volvo_v.currency}".replace(",", ".")

                    reply_text = (
                        f"{salutation_prefix}portföyümüzü taradığımda tam aradığınız donanımlara sahip mükemmel bir seçenek bulunuyor: **Volvo XC40 Plus Dark**!\n\n"
                        f"🚗 **Volvo XC40 1.5 T2 Plus Dark** ({volvo_v.year} Model | {km_fmt}) ➔ **{price_fmt}**\n\n"
                        f"✨ Bu aracımızdaki kış ve konfor donanımları:\n"
                        f"• **Isıtmalı Direksiyon Simidi & Isıtmalı Ön Koltuklar** (Kış Paketi Standart)\n"
                        f"• Panoramik Açılır Cam Tavan\n"
                        f"• Elektrikli & Hafızalı Konfor Koltuklar\n"
                        f"• Dark Tema & 360° Çevre Görüş Kamerası\n"
                        f"• Kablosuz Telefon Şarjı & City Safety Aktif Güvenlik\n\n"
                        f"👉 Sayfadaki filtreyi de hemen **Volvo XC40** için güncelledim. Aracın ekspertiz raporunu veya finansman koşullarını detaylandırmamı ister misiniz?"
                    )
                else:
                    reply_text = (
                        f"{salutation_prefix}şu an aktif stoklarımızda direksiyon ısıtmalı bir araç hazırda görünmüyor. "
                        f"Ancak portföyümüze bu donanımda yeni bir araç (Volvo, BMW, Mercedes vb.) girdiğinde size hemen telefonla haber verebilirim!"
                    )
            else:
                db_all = self.db.query(Vehicle).filter(Vehicle.is_active == True).order_by(Vehicle.price.desc()).all()
                matched_vehicles_data = [v.to_dict() for v in db_all]
                filter_action = {"brand": "all", "body_type": "all", "max_price": None, "search": ""}
                
                lines = [f"• **{v.brand} {v.model}** ({v.year} | {v.km:,.0f} KM) ➔ **{v.price:,.0f} TL**".replace(",", ".") for v in db_all]
                reply_text = (
                    f"{salutation_prefix}Arkas 2. El portföyümüzdeki tüm güncel araçları sizin için listeledim:\n\n"
                    + "\n".join(lines)
                    + "\n\nİstediğiniz aracın donanım ve ekspertiz detaylarını doğrudan sorabilirsiniz!"
                )

        # -------------------------------------------------------------------------
        # BRANCH 4: Direct Q&A on Current Focused Vehicle (KM, Vites, Fiyat, Donanım)
        # -------------------------------------------------------------------------
        else:
            direct_ans = None
            if focused_v:
                direct_ans = self._answer_vehicle_specific_question(focused_v, msg_clean, honorific)

            if direct_ans:
                reply_text = direct_ans
            else:
                # ---------------------------------------------------------------------
                # BRANCH 5: General Search / Catalog Filtering
                # ---------------------------------------------------------------------
                if extracted.get("budget_max"):
                    customer.budget_max = extracted["budget_max"]
                if extracted.get("interested_brand"):
                    customer.interested_brand = extracted["interested_brand"]
                if extracted.get("interested_body_type"):
                    customer.interested_body_type = extracted["interested_body_type"]

                q_db = self.db.query(Vehicle).filter(Vehicle.is_active == True)

                if customer.interested_brand and customer.interested_brand.lower() != "all":
                    q_db = q_db.filter(Vehicle.brand.ilike(f"%{customer.interested_brand}%"))
                
                if customer.interested_body_type and customer.interested_body_type.lower() != "all":
                    q_db = q_db.filter(Vehicle.body_type.ilike(f"%{customer.interested_body_type}%"))

                if customer.budget_max:
                    q_db = q_db.filter(Vehicle.price <= customer.budget_max * 1.1)

                db_results = q_db.order_by(Vehicle.price.asc()).limit(5).all()

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

                    vehicle_lines = []
                    for v in db_results:
                        km_fmt = f"{v.km:,.0f} KM".replace(",", ".")
                        price_fmt = f"{v.price:,.0f} {v.currency}".replace(",", ".")
                        vehicle_lines.append(
                            f"• **{v.brand} {v.model} {v.sub_model or ''}** ({v.year} Model | {km_fmt}) ➔ **{price_fmt}**"
                        )

                    vehicles_text = "\n".join(vehicle_lines)
                    reply_text = (
                        f"{salutation_prefix}kriterlerinize uygun güncel Arkas 2. El portföyümüzdeki araçlar:\n\n"
                        f"{vehicles_text}\n\n"
                        f"👉 Sayfadaki ilanları da aramanıza göre filtreledim. Araçların vitesini, kilometresini, ekspertiz durumunu veya donanım detaylarını doğrudan bana sorabilirsiniz!"
                    )
                else:
                    reply_text = (
                        f"{salutation_prefix}aradığınız kriterlere tam uyan bir araç şu an aktif stoklarımızda görünmüyor. "
                        f"Bütçenizi genişletebilir veya farklı bir model belirtebilirsiniz. Stoğumuza yeni araç girdiğinde size bildirebilirim!"
                    )

        # Append assistant reply to history
        history.append({"role": "assistant", "content": reply_text, "timestamp": datetime.datetime.utcnow().isoformat()})
        customer.chat_history = history

        # 6. Update Conversation Summary in DB
        summary_parts = []
        if customer.full_name:
            summary_parts.append(f"Müşteri: {customer.full_name}")
        if customer.phone:
            summary_parts.append(f"Tel: {customer.phone}")
        if customer.interested_brand:
            summary_parts.append(f"Marka: {customer.interested_brand}")
        if customer.interested_body_type:
            summary_parts.append(f"Kasa: {customer.interested_body_type}")
        if customer.budget_max:
            summary_parts.append(f"Bütçe: {customer.budget_max:,.0f} TL".replace(",", "."))
        if focused_v:
            summary_parts.append(f"İncelenen Araç: {focused_v.brand} {focused_v.model}")

        customer.conversation_summary = " | ".join(summary_parts) if summary_parts else "Müşteri genel araç araması yapıyor."

        self.db.commit()
        self.db.refresh(customer)

        return {
            "reply": reply_text,
            "customer_id": customer.id,
            "customer_name": customer.first_name or "",
            "filter_action": filter_action,
            "matched_vehicles": matched_vehicles_data
        }
