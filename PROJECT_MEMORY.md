# PROJECT_MEMORY.md - Arkas 2. El Pazarlama AI

## 1. Proje Özeti ve Vizyon
* **Proje Adı:** Automotive AI Marketing Platform (Arkas 2. El Pazarlama AI)
* **Amaç:** 2. el araç verilerini toplayarak salt teknik özellik listelemek yerine; marka kimliği, hedef kitle ve duygusal satış noktalarına (emotional selling points) dayalı yüksek dönüşümlü reklam metinleri, kancalar ve hikayeler üreten, zengin orijinal fotoğraflarla sergileyen ve sayfayı dinamik kontrol eden Bilişsel AI Satış Danışmanı sunan yeni nesil platform.
* **Ana Felsefe:** "Bir araç kataloğu gibi değil, otomotiv pazarlama ajansı ve uzman satış danışmanı gibi düşün."

## 2. Teknoloji Yığını (Tech Stack)
* **Çekirdek Dil:** Python 3.11+ (FastAPI, SQLAlchemy 2.0, BeautifulSoup4, Requests, Pydantic v2)
* **Veritabanı:** PostgreSQL 17 (Host: `localhost`, Port: `5432`, DB: `arkas_marketing_db`, User: `postgres`, Password: `postgres`)
* **AI Metin Motoru:** `MarketingAgent` (Safe / Dengeli & Bold / İlgi Çekici reklam metinleri, kancalar, hikaye akışları)
* **AI Danışman & Bilişsel Niyet Motoru:** `ChatbotAgent` (Cognitive Intent Classifier, Turkish NER & Honorifics, Dynamic Cross-Vehicle Recommendation, Budget Expansion, Context-Aware Active Memory, PostgreSQL RAG + Canlı Ağ Bilgisi + Sayfa Filtre Aksiyonları)
* **Web Arayüzü & Vitrin:** **Next.js 15 (React 19, TypeScript, Tailwind CSS v4, Lucide React)** Minimalist Quiet Luxury Otomotiv Vitrin Stüdyosu (`frontend/`) + Yüzen AI Asistan Widget'ı
* **Veritabanı İstemci Desteği:** DBeaver tam entegrasyonu (`vehicles`, `customer_leads`, `creative_briefs`, `marketing_copies`)
* **Konfigürasyon:** `.env` (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, DATABASE_URL)

## 3. Mimari ve Modüler İş Akışı
1. **Veritabanı Katmanı (`src/db/` & PostgreSQL 5432):**
   - `vehicles`: `package`, `technical_specs` (JSON), `ad_features` (JSON), `damage_expertise` (JSON), `expertise_note`, `image_urls` (JSON), `primary_image_url`.
   - `customer_leads`: `session_id` bazlı tekil müşteri kaydı, ad-soyad, telefon, bütçe, ilgilenilen araç ve konuşma özeti.
   - `creative_briefs`: Marka arketipi, hedef persona, duygusal satış noktaları.
   - `marketing_copies`: Safe & Bold varyantları, kancalar, gövde metinleri, CTA ve hashtagler.
2. **Ana Orkestratör (`main.py`):** Scraper -> AI Marketing Agent -> Web Sunucusu.
3. **Bilişsel AI Satış Danışmanı & Chatbot (`src/agent/chatbot_agent.py` & `/api/chat`):**
   - Türkçe Varlık Tanıma (NER) ve cinsiyet hitap sözlüğü (Ceren Hanım / Tufan Bey / Sayın).
   - Tekil `session_id` ile mükerrersiz lead kaydı.
   - Bütçe esnetme (`5M kadar çıkart`) ve çapraz donanım önerisi (Skoda'dan kış paketli Volvo XC40'a geçiş ve sayfa filtreleme).
4. **Modern Next.js Vitrin & Stüdyo (`frontend/` & `src/web/`):**
   - Orijinal araç galerisi, teknik özellikler paneli, ekspertiz durumu ve AI reklam metin panosu.

## 4. Dokümantasyon Standartları (`docs/`)
* MVP Mimari & Veri Akışı: `docs/2026-08-17_mvp_mimari_veri_akisi_ve_afis_motoru.md`
* Canlı Fotoğraf Çekimi & Çoklu Açı Afişleri: `docs/2026-08-17_canli_katalog_gorsel_cekimi_ve_coklu_aci_afisleri.md`
* Next.js 15 Modern Vitrin & Stüdyo Dönüşümü: `docs/2026-08-18_nextjs_modern_vitrin_ve_studio_donusumu.md`
* Quiet Luxury Afiş Motoru & 3+1 Odaklı Kamera Açıları: `docs/2026-08-18_quiet_luxury_afis_motoru_ve_3_arti_1_aci_guncellemesi.md`
* Akıllı AI Danışman & Müşteri Takip Mimarisi: `docs/2026-08-18_akilli_ai_danisman_ve_musteri_takip_mimarisi.md`
* Bilişsel AI Satış Danışmanı & Dinamik Araç Önerisi: `docs/2026-08-18_bilissel_ai_satis_danismani_ve_dinamik_arac_onerisi.md`
* Türkçe İsim & Varlık Tanıma (NER) ve Doğru Hitap Mimarisi: `docs/2026-08-18_turkce_varlik_tanima_ve_dogru_hitap_sistemi.md`
* Görsel Motoru Temizliği & Kapsamlı Araç Şeması Hazırlığı: `docs/2026-08-18_gorsel_motoru_temizligi_ve_detayli_arac_semasi_hazirligi.md`

## 5. Güncel Durum ve Sürekli Hafıza Kuralları
* **Mevcut Durum:** Sentetik görsel üretim scriptleri ve tabloları temizlendi. `Vehicle` tablosu donanım paketi, teknik özellikler, ilan detay donanımları, hasar/ekspertiz durumu ve orijinal görsel listesiyle zenginleştirildi. Veritabanı sıfırdan oluşturuldu ve yeni veri kaynağı scraper'ı için hazır hale getirildi.
* **Kural:** Her mimari ve işlevsel güncellemeden sonra `PROJECT_MEMORY.md`, `.antigravity_rules.md`, `.cursorrules.md`, `.github/copilot-instructions.md`, `README.md` ve ilgili `docs/` belgesi eksiksiz güncellenmek zorundadır.
