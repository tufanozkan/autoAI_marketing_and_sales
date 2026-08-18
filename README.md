# Arkas 2. El Pazarlama AI (Automotive AI Marketing & Sales Platform)

Yapay zeka destekli, 2. el araç verilerini toplayıp marka ve müşteri kimliğine uygun **yüksek dönüşümlü pazarlama metinleri, Safe & Bold reklam kreatifleri, orijinal zengin fotoğraf galerisi ve sayfayı dinamik kontrol eden Bilişsel AI Satış Danışmanı** sunan yeni nesil otomotiv platformu.

---

## 🏗️ Mimari ve Dizin Yapısı

```
arkas_2el_pazarlama_ai/
├── main.py                     # Ana orkestratör (Scraper -> AI Metin Ajanı -> Web Sunucusu)
├── config.py                   # Merkezi konfigürasyon, DB bağlantısı, port ve ortam ayarları
├── requirements.txt            # Python bağımlılıkları (FastAPI, SQLAlchemy, psycopg2, BeautifulSoup4)
├── docker-compose.yml          # PostgreSQL 17 veritabanı konteyner yapılandırması
├── .env                        # Çevre değişkenleri ve DB bağlantı bilgileri
├── .env.example                # Örnek çevre değişkenleri şablonu
├── PROJECT_MEMORY.md           # Sürekli güncellenen mimari hafıza
├── README.md                   # Proje dokümantasyonu ve kullanım kılavuzu
├── docs/                       # Tarih bazlı detaylı mimari ve teknik geliştirme dokümanları
│   ├── 2026-08-17_mvp_mimari_veri_akisi_ve_afis_motoru.md
│   ├── 2026-08-17_canli_katalog_gorsel_cekimi_ve_coklu_aci_afisleri.md
│   ├── 2026-08-18_nextjs_modern_vitrin_ve_studio_donusumu.md
│   ├── 2026-08-18_quiet_luxury_afis_motoru_ve_3_arti_1_aci_guncellemesi.md
│   ├── 2026-08-18_akilli_ai_danisman_ve_musteri_takip_mimarisi.md
│   ├── 2026-08-18_bilissel_ai_satis_danismani_ve_dinamik_arac_onerisi.md
│   ├── 2026-08-18_turkce_varlik_tanima_ve_dogru_hitap_sistemi.md
│   └── 2026-08-18_gorsel_motoru_temizligi_ve_detayli_arac_semasi_hazirligi.md
├── src/
│   ├── db/                     # Veritabanı katmanı
│   │   ├── database.py         # SQLAlchemy engine, connection pool ve session yönetimi
│   │   └── models.py           # Vehicle, CustomerLead, CreativeBrief, MarketingCopy ORM modelleri
│   ├── scraper/                # Veri toplama ve normalizasyon
│   │   ├── arkas_scraper.py    # Detaylı veri toplayıcı
│   │   └── normalizer.py       # Fiyat, KM, teknik özellik ve donanım temizleyici
│   ├── agent/                  # Pazarlama metin & Bilişsel AI Asistan
│   │   ├── brand_rules.py      # Marka arketip kuralları (Volvo, BMW, Mercedes, Peugeot vb.)
│   │   ├── marketing_agent.py  # Persona, Safe (Dengeli) & Bold (İlgi Çekici) metinleri ve kancalar
│   │   └── chatbot_agent.py    # Bilişsel AI Satış Danışmanı (NER, Hitap, Bütçe Esnetme, Çapraz Öneri)
│   └── web/                    # Web sunucusu & REST API
│       └── server.py           # FastAPI REST API (/api/chat, /api/leads, /api/vehicles vb.) ve Next.js mount
└── frontend/                   # Next.js 15 Modern Lüks Vitrin ve Stüdyo (App Router)
    ├── src/app/                # Next.js App Router (globals.css, layout.tsx, page.tsx)
    ├── src/components/         # Navbar, StatsSection, FilterToolbar, VehicleCard, ChatbotWidget, CreativeStudioModal
    └── out/                    # Statik export çıktısı (FastAPI tarafından servis edilir)
```

---

## 🚀 Hızlı Başlangıç

### 1. Ortamı Hazırlayın ve Bağımlılıkları Yükleyin
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Tek Komutla Tüm Sistemi Çalıştırın
```bash
python main.py
```
> Bu komut sırasıyla:
> 1. Web Scraper'ı çalıştırıp araçları detaylı teknik özellikleri ve fotoğraflarıyla PostgreSQL'e kaydeder (`vehicles`).
> 2. AI Marketing Agent ile reklam metinlerini üretir (`creative_briefs`, `marketing_copies`).
> 3. Web Vitrinini ve Bilişsel AI Danışmanı **http://localhost:8000** adresinde başlatır.

---

## 🤖 Bilişsel AI Satış Danışmanı Özellikleri

* **Türkçe Varlık Tanıma (NER) & Doğru Hitap:** Müşteri isimlerini (Ceren Hanım, Tufan Bey) ve negatif telefon niyetlerini kusursuz anlar.
* **Lead Yakalama & Tekil Oturum:** Müşterinin ad, soyad ve tercihlerini tek bir oturum kaydında (`session_id`) tutar.
* **Doğrudan İnsansı Q&A:** Vites, kilometre, ekspertiz ve yakıt sorularına şablon değil samimi ve net yanıtlar verir.
* **Bütçe Esnetme (Budget Expansion):** *"Fiyat aralığını 5m kadar çıkart"* dendiğinde bütçeyi günceller, portföydeki tüm araçları donanım ayrıcalıklarıyla sunar.
* **Çapraz Donanım Önerisi:** Odaktaki araçta olmayan bir donanım istendiğinde tüm portföyü tarayıp bu donanıma sahip modele geçer ve sayfayı anında filtreler.

---

## 🗄️ DBeaver / PostgreSQL Bağlantı Bilgileri

| Parametre | Değer |
| :--- | :--- |
| **Host** | `localhost` veya `127.0.0.1` |
| **Port** | `5432` |
| **Database** | `arkas_marketing_db` |
| **Username** | `postgres` |
| **Password** | `postgres` |

### PostgreSQL Tabloları
* `vehicles` : İlan kimliği, marka, model, paket, yıl, km, fiyat, `technical_specs` (JSON), `ad_features` (JSON), `damage_expertise` (JSON), `image_urls` (JSON) ve SHA256 hash'i.
* `customer_leads` : Müşteri iletişim bilgileri, ilgilenilen marka/kasa, bütçe, tam sohbet dökümü ve AI sohbet özeti.
* `creative_briefs` : Marka arketipi, hedef persona, duygusal satış noktaları ve kancalar.
* `marketing_copies` : Instagram post/hikaye metinleri, başlıklar, CTA ve hashtagler (Safe & Bold).

---

## 📚 Dokümantasyon

Tüm mimari detaylar ve kronolojik kararlar `docs/` klasöründe saklanmaktadır:
* [2026-08-17 MVP Mimari, Veri Akışı ve Afiş Motoru Dokümanı](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-17_mvp_mimari_veri_akisi_ve_afis_motoru.md)
* [2026-08-17 Canlı Katalog Görsel Çekimi ve Çoklu Açı Afişleri](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-17_canli_katalog_gorsel_cekimi_ve_coklu_aci_afisleri.md)
* [2026-08-18 Next.js 15 Modern Vitrin ve Stüdyo Dönüşümü](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_nextjs_modern_vitrin_ve_studio_donusumu.md)
* [2026-08-18 Quiet Luxury Afiş Motoru ve 3+1 Odaklı Kamera Açıları](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_quiet_luxury_afis_motoru_ve_3_arti_1_aci_guncellemesi.md)
* [2026-08-18 Akıllı AI Danışman ve Müşteri Takip Mimarisi](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_akilli_ai_danisman_ve_musteri_takip_mimarisi.md)
* [2026-08-18 Bilişsel AI Satış Danışmanı ve Dinamik Araç Önerisi](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_bilissel_ai_satis_danismani_ve_dinamik_arac_onerisi.md)
* [2026-08-18 Türkçe İsim & Varlık Tanıma (NER) ve Doğru Hitap Mimarisi](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_turkce_varlik_tanima_ve_dogru_hitap_sistemi.md)
* [2026-08-18 Görsel Motoru Temizliği ve Kapsamlı Araç Şeması Hazırlığı](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_gorsel_motoru_temizligi_ve_detayli_arac_semasi_hazirligi.md)