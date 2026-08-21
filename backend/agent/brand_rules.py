from typing import Dict, Any, List

class BrandRules:
    BRAND_CONFIG: Dict[str, Dict[str, Any]] = {
        "Volvo": {
            "archetype": "Koruyucu & Güvenilir (The Caregiver / Sage)",
            "tone": "Sakin, prestijli, güven veren, aile ve güvenlik odaklı",
            "keywords": ["Güvenlik", "İskandinav Lüksü", "Aile Koruması", "Huzurlu Yolculuk", "Showroom Güvencesi"],
            "target_persona": "Ailesinin güvenliğini her şeyin üstünde tutan, konfor ve uzun ömürlü kalite arayan profesyoneller",
            "emotional_points": [
                "Her kilometrede sevdikleriniz için tavizsiz güvenlik kalkanı",
                "İskandinav tasarımının sunduğu dingin ve lüks yaşam alanı",
                "Sertifikalı 2. El garantisiyle sıfır risk, kusursuz huzur"
            ],
            "accent_color": "#003057",  # Volvo Blue
            "badge_icon": "🛡️",
            "hooks": [
                "Ailenizin güvenliği için tasarlandı: Volvo konforu showroomumuzda.",
                "Yollardaki en güvenli sığınağınız. Kusursuz kondisyonda Volvo.",
                "İskandinav zarafeti ve üst düzey güvenlik şimdi yeni sahibini bekliyor."
            ]
        },
        "BMW": {
            "archetype": "Hükümdar & Kaşif (The Ruler / Hero)",
            "tone": "Dinamik, tutkulu, iddialı, sürüş hazzı ve performans odaklı",
            "keywords": ["Sürüş Zevki", "M Sport Dinamizm", "Saf Güç", "Prestij", "Yüksek Performans"],
            "target_persona": "Direksiyon başında kontrolü ve adrenalini seven, başarısını ve dinamizmini yansıtmak isteyen yöneticiler",
            "emotional_points": [
                "Her virajda kalbinizi hızlandıran saf sürüş keyfi",
                "İkonik M tasarım ve yollarda bakışları üzerine çeken duruş",
                "Yetkili servis geçmişi ve 100+ nokta kontrolüyle tam güven"
            ],
            "accent_color": "#0066B1",  # BMW Blue
            "badge_icon": "⚡",
            "hooks": [
                "Direksiyona geçin ve saf sürüş zevkini yeniden tanımlayın.",
                "Bakışları üzerinize çekecek güç ve zarafet: BMW performansı.",
                "Sadece bir otomobil değil; her sürüşte ayrıcalıklı bir tutku."
            ]
        },
        "Mercedes-Benz": {
            "archetype": "Hükümdar & Lüks Lideri (The Ruler / Sovereign)",
            "tone": "Kusursuz, zarif, üst segment lüks ve liderlik dili",
            "keywords": ["Yıldızın Işığı", "Üstün Konfor", "Liderlik", "Yönetici Sınıfı", "Kusursuz Prestij"],
            "target_persona": "Statü, mutlak konfor ve mükemmel işçilik arayan iş insanları ve üst düzey liderler",
            "emotional_points": [
                "Başarınızı taçlandıran eşsiz Mercedes-Benz prestiji",
                "Gürültüden uzak, birinci sınıf konforla dolu iç kabin",
                "Yıldızın ışığında güvenle geleceğe sürüş"
            ],
            "accent_color": "#00A19C",  # Mercedes Teal/Silver
            "badge_icon": "⭐",
            "hooks": [
                "Başarınızı yollara yansıtın: Eşsiz Mercedes-Benz konforu.",
                "Yıldızın prestiji ve showroom ayrıcalığı ile yollarınızda.",
                "Her detayında birinci sınıf işçilik ve kusursuz asalet."
            ]
        },
        "Audi": {
            "archetype": "Yenilikçi & Akılcı (The Visionary / Creator)",
            "tone": "Teknolojik, fütüristik, zeki ve modern lüks",
            "keywords": ["Teknoloji ile Bir Adım Önde", "Quattro Çekiş", "Fütüristik Kokpit", "Modern Estetik"],
            "target_persona": "Teknolojiye meraklı, yenilikçi ve estetik zekaya önem veren vizyoner profesyoneller",
            "emotional_points": [
                "Teknolojinin sunduğu akıllı ve güvenli sürüş deneyimi",
                "Quattro gücüyle her yol koşulunda tavizsiz hakimiyet",
                "Modern çağın gereksinimlerine tam yanıt veren fütüristik kabin"
            ],
            "accent_color": "#BB0A30",  # Audi Red
            "badge_icon": "🔬",
            "hooks": [
                "Teknolojiyle bir adım önde: Audi akıllı sürüş deneyimi.",
                "Yarınların sürüş teknolojisi bugün showroomumuzda sizi bekliyor.",
                "Zeka, estetik ve üstün mühendisliğin kusursuz buluşması."
            ]
        },
        "Peugeot": {
            "archetype": "Stil Sahibi & Dinamik (The Magician / Trendsetter)",
            "tone": "Modern, çekici, tasarım odaklı, şehirli ve özgüvenli",
            "keywords": ["i-Cockpit Deneyimi", "Göz Alıcı Tasarım", "Aslan Pençesi Işıklar", "Şehir Estetiği"],
            "target_persona": "Tasarımıyla fark yaratmak isteyen, teknolojik donanımlara ve şık detaylara değer veren modern şehirliler",
            "emotional_points": [
                "Her yolculuğu keyfe dönüştüren fütüristik i-Cockpit kabin",
                "Cesur ve ödüllü tasarımıyla sokaklarda hemen fark edilen stil",
                "Düşük yakıt tüketimi ve yüksek konforun ideal dengesi"
            ],
            "accent_color": "#004B87",  # Peugeot Blue
            "badge_icon": "🦁",
            "hooks": [
                "Sıradanlığı geride bırakın: Peugeot'nun göz alıcı tasarımı.",
                "Her sürüşte büyüleyen i-Cockpit dünyasına adım atın.",
                "Cesur stil, yüksek konfor ve sertifikalı ekspertiz güvencesi bir arada."
            ]
        },
        "Opel": {
            "archetype": "Akılcı & Ulaşılabilir Alman (The Everyman / Realist)",
            "tone": "Pratik, sağlam, modern, yüksek fiyat/performans ve güvenilir",
            "keywords": ["Alman Mühendisliği", "Pure Panel", "Akılcı Seçim", "Geniş Yaşam Alanı", "Düşük Tüketim"],
            "target_persona": "Bütçesini akıllıca yöneten, sağlamlıktan ve modern teknolojiden ödün vermeyen aileler",
            "emotional_points": [
                "Alman sağlamlığıyla uzun yıllar sorunsuz yol arkadaşlığı",
                "Günlük hayatı kolaylaştıran ergonomik ve teknolojik donanımlar",
                "Ekonomik sürüş ve yüksek 2. el değeri"
            ],
            "accent_color": "#FFCC00",  # Opel Yellow
            "badge_icon": "⚡",
            "hooks": [
                "Alman mühendisliği, akılcı teknoloji ve tam güvenilirlik.",
                "Aileniz için en doğru ve en sağlam seçim showroomumuzda.",
                "Pratik zeka ve modern konforun buluştuğu nokta."
            ]
        },
        "Volkswagen": {
            "archetype": "Güvenilir & Zamansız (The Ruler / Caregiver)",
            "tone": "Kaliteli, oturaklı, dengeli ve zamansız Alman ekolü",
            "keywords": ["Zamansız Tasarım", "Yüksek 2. El Değeri", "Alman Konforu", "DSG Hassasiyeti"],
            "target_persona": "İstikrar, yüksek ikinci el değeri ve risksiz kalite arayan tüm sürücüler",
            "emotional_points": [
                "Yıllar geçse de değerini ve konforunu koruyan zamansız kalite",
                "Hassas sürüş dinamikleri ve sessiz kabin konforu",
                "Kapsamlı ekspertiz güvencesiyle garantili huzur"
            ],
            "accent_color": "#001E50",  # VW Navy
            "badge_icon": "💎",
            "hooks": [
                "Değerini her zaman koruyan zamansız Alman kalitesi.",
                "Yollarda güven ve prestijin simgesi: Volkswagen.",
                "Kusursuz işçilik ve sorunsuz sürüş keyfi showroomumuzda."
            ]
        },
        "Renault": {
            "archetype": "Samimi & Akıllı Şehirli (The Everyman / Companion)",
            "tone": "Sıcak, dost canlısı, ekonomik ve dinamik",
            "keywords": ["Akıllı Şehir Otomobili", "Ekonomik Sürüş", "Dinamik Çizgiler", "Pratik Konfor"],
            "target_persona": "Şehir içi trafiğinde çeviklik, düşük yakıt maliyeti ve stil arayan gençler ve aileler",
            "emotional_points": [
                "Şehir hayatını kolaylaştıran çevik ve akıllı sürüş",
                "Cebinizi güldüren düşük tüketim ve bol yedek parça güvencesi",
                "Renkli ve enerjik tasarımıyla hayata uyum sağlayan enerji"
            ],
            "accent_color": "#FFCC00",  # Renault Yellow
            "badge_icon": "🌟",
            "hooks": [
                "Şehrin ritmini yakalayın: Enerjik ve ekonomik.",
                "Akılcı bütçe, modern donanım ve 12 ay showroom garantisi.",
                "Hayata renk katan pratik sürüş deneyimi."
            ]
        },
        "Skoda": {
            "archetype": "Simply Clever & Akılcı Aile (The Sage / Everyman)",
            "tone": "Zeki, geniş yaşam alanı odaklı, fonksiyonel, güvenilir ve konforlu",
            "keywords": ["Simply Clever", "Geniş İç Hacim", "Akılcı Çözümler", "Aile Konforu", "Yüksek Güvenlik"],
            "target_persona": "Geniş bagaj ve iç hacme değer veren, hayatı kolaylaştıran pratik çözümler arayan aileler",
            "emotional_points": [
                "Her yolculukta tüm aileniz için maksimum ferahlık ve konfor",
                "Simply Clever akılcı detaylarla hayatı kolaylaştıran tasarım",
                "Detaylı 100+ nokta ekspertiziyle tam şeffaflık ve sıfır risk"
            ],
            "accent_color": "#4BA82E",  # Skoda Green
            "badge_icon": "🍀",
            "hooks": [
                "Akılcı çözümler ve geniş konfor: Skoda ayrıcalığı.",
                "Ailenizin tüm ihtiyaçlarına tek araçla mükemmel yanıt.",
                "Zeka dolu donanımlar ve sertifikalı ekspertiz güvencesi bir arada."
            ]
        },
        "Ford": {
            "archetype": "Güçlü & Dayanıklı Yol Arkadaşı (The Hero / Realist)",
            "tone": "Sağlam, dinamik yol tutuşlu, dayanıklı ve güvenilir",
            "keywords": ["Üstün Yol Tutuş", "EcoBoost Performans", "Dayanıklılık", "Sağlam Mühendislik"],
            "target_persona": "Güçlü yol tutuş, sağlam gövde ve iş/aile hayatında yüksek dayanıklılık arayan sürücüler",
            "emotional_points": [
                "Efsanevi Ford yol tutuşuyla her virajda mutlak hakimiyet",
                "Zorlu şartlara meydan okuyan sağlam ve dayanıklı yapı",
                "Düşük işletme maliyeti ve yüksek ikinci el güvencesi"
            ],
            "accent_color": "#002C6C",  # Ford Blue
            "badge_icon": "🚙",
            "hooks": [
                "Yollarda sağlamlık ve güven: Efsanevi Ford performansı.",
                "Her yolculukta üstün yol tutuş ve tavizsiz dayanıklılık.",
                "Güçlü yol arkadaşınız sertifikalı showroom güvencesiyle sizi bekliyor."
            ]
        }
    }

    SEGMENT_RULES: Dict[str, Dict[str, str]] = {
        "SUV": {
            "focus": "Geniş aile yaşamı, macera, yüksek oturma pozisyonu ve güvenli yol tutuş",
            "tag": "Geniş Yaşam Alanı & Macera Ruhu"
        },
        "Sedan": {
            "focus": "Prestij, kurumsal asalet, sessiz kabin konforu ve dengeli sürüş",
            "tag": "Kurumsal Zarafet & Maksimum Konfor"
        },
        "Hatchback": {
            "focus": "Şehir içi pratik park, çevik manevra, ekonomik tüketim ve gençlik",
            "tag": "Şehir Çevikliği & Akılcı Pratiklik"
        },
        "Elektrik": {
            "focus": "Sıfır emisyon, sessiz anlık tork, geleceğin teknolojisi ve çevre dostu lüks",
            "tag": "%100 Elektrik & Geleceğin Sürüşü"
        }
    }

    @classmethod
    def get_brand_config(cls, brand: str) -> Dict[str, Any]:
        brand_norm = brand.strip().title()
        if "Mercedes" in brand_norm:
            brand_norm = "Mercedes-Benz"
        elif "Bmw" in brand_norm:
            brand_norm = "BMW"
        elif "Vw" in brand_norm or "Volkswagen" in brand_norm:
            brand_norm = "Volkswagen"
            
        return cls.BRAND_CONFIG.get(brand_norm, {
            "archetype": "Güvenilir & Kaliteli Otomotiv",
            "tone": "Profesyonel, güven veren, net ve fayda odaklı",
            "keywords": ["Showroom Güvencesi", "Ekspertiz Garantisi", "Konfor", "Yol Arkadaşı"],
            "target_persona": "Aracında güvenlik, bütçe dengesi ve satış sonrası huzur arayan otomobil sahipleri",
            "emotional_points": [
                "Sertifikalı 2. El güvencesiyle sıfır riskli satın alma deneyimi",
                "Titizlikle kontrol edilmiş ekspertiz ve teknik kondisyon",
                "Yolculuklarınızı keyfe dönüştüren konforlu detaylar"
            ],
            "accent_color": "#E30613",
            "badge_icon": "🚗",
            "hooks": [
                "Hayalinizdeki otomobil sertifikalı showroom güvencesiyle sizi bekliyor.",
                "Kusursuz kondisyonda, ekspertiz garantili güvenli sürüş.",
                "Aradığınız konfor ve kalite en uygun avantajlarla burada."
            ]
        })

    @classmethod
    def get_segment_rule(cls, body_type: str, fuel_type: str = "") -> Dict[str, str]:
        if fuel_type and "elektrik" in str(fuel_type).lower():
            return cls.SEGMENT_RULES["Elektrik"]
        norm = str(body_type).upper() if body_type else "SEDAN"
        if "SUV" in norm:
            return cls.SEGMENT_RULES["SUV"]
        elif "HATCHBACK" in norm or "HB" in norm:
            return cls.SEGMENT_RULES["Hatchback"]
        elif "SEDAN" in norm:
            return cls.SEGMENT_RULES["Sedan"]
        return cls.SEGMENT_RULES["Sedan"]
