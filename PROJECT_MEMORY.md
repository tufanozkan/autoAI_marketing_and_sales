# PROJECT_MEMORY.md - Arkas 2. El Pazarlama AI

## 1. Proje Özeti ve Vizyon
* **Proje Adı:** Automotive AI Marketing Platform (Arkas 2. El Pazarlama AI)
* **Amaç:** 2. el araç ilan verilerini toplayarak salt teknik özellik listelemek yerine; marka kimliği, hedef kitle ve duygusal satış noktalarına (emotional selling points) dayalı yüksek dönüşümlü reklam metinleri, görsel konseptler, afişler ve sosyal medya kreatifleri üreten yapay zeka destekli pazarlama platformu.
* **Ana Felsefe:** "Bir araç kataloğu gibi değil, otomotiv pazarlama ajansı ve uzman satış danışmanı gibi düşün."

## 2. Teknoloji Yığını (Tech Stack)
* **Çekirdek Dil:** Python 3.11+ (FastAPI, SQLAlchemy 2.0, Pillow, BeautifulSoup4, Requests, Pydantic v2)
* **Veritabanı:** PostgreSQL 17 (Host: `localhost`, Port: `5432`, DB: `arkas_marketing_db`, User: `postgres`, Password: `postgres`)
* **Konteyner Altyapısı:** `docker-compose.yml` (PostgreSQL 17)
* **AI Danışman & Bilişsel Niyet Motoru:** `ChatbotAgent` (Cognitive Intent Classifier, Dynamic Cross-Vehicle Recommendation, Budget Expansion, Context-Aware Active Memory, PostgreSQL RAG + Canlı Ağ Bilgisi + Sayfa Filtre Aksiyonları)
* **Web Arayüzü & Vitrin:** **Next.js 15 (React 19, TypeScript, Tailwind CSS v4, Lucide React)** Minimalist Quiet Luxury Otomotiv Vitrin Stüdyosu (`frontend/`) + Yüzen AI Asistan Widget'ı
* **Veritabanı İstemci Desteği:** DBeaver tam entegrasyonu (`customer_leads`, `vehicles`, `creative_briefs`, `marketing_copies`, `posters`)
* **Konfigürasyon:** `.env` (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, DATABASE_URL)

## 3. Mimari ve Modüler İş Akışı
1. **Veritabanı Katmanı (`src/db/` & PostgreSQL 5432):** DBeaver ve dış GUI araçlarıyla doğrudan bağlanılabilir; `vehicles`, `creative_briefs`, `marketing_copies`, `posters` ve `customer_leads` tabloları aktiftir.
2. **Ana Orkestratör (`main.py`):** Tek komutla (`python main.py`) sırasıyla tüm adımları tetikler veya bağımsız CLI bayraklarıyla (`--reset-db`, `--scrape-only`, `--generate-only`, `--web-only`, `--no-web`, `--build-frontend`) çalışır.
3. **Canlı Web Scraper Modülü (`src/scraper/`):** `https://www.arkasotomotiv2.com` üzerindeki gerçek ilanları ve orijinal araç fotoğraflarını (`panel/public/resimler/`) çeker, normalize eder, SHA256 içerik hash'i ile mükerrerlik olmadan PostgreSQL'e kaydeder.
4. **Bilişsel AI Satış Danışmanı & Chatbot (`src/agent/chatbot_agent.py` & `/api/chat`):**
   - Karşılama akışında ad, soyad ve telefon numarasını alarak `customer_leads` tablosuna tekil `session_id` ile kaydeder (aynı sohbette tek satır).
   - **Bilişsel Niyet Analizi:** Bütçe artırma isteklerini (`5M kadar çıkart`), donanım bazlı öneri taleplerini (`direksiyon ısıtmalı araç öner`), araç bazlı spesifik soruları (`KM, vites, ekspertiz, yakıt`) doğru sınıflandırır.
   - **Çapraz Donanım Önerisi:** Odaktaki araçta (Skoda Kamiq) istenen donanım (direksiyon/koltuk ısıtma) yoksa takılı kalmaz; portföyü tarayıp bu donanıma sahip **Volvo XC40 Plus Dark** modeline geçiş yapar ve sayfayı Volvo'ya filtreler.
   - Müşterinin ne istediğini özetleyen `conversation_summary` oluşturur.
5. **Modern Next.js Vitrin & Kreatif Stüdyosu (`frontend/` & `src/web/`):** 
   - Minimalist Quiet Luxury tasarım sistemi, anlık arama (`⌘K`), marka ve kasa filtreleri.
   - 16:9 geniş web vitrini ve sosyal medya metin panosu.
   - Sağ altta yüzen nefes alan AI danışman butonu.

## 4. Dokümantasyon Standartları (`docs/`)
* Yapılan tüm mimari kararlar ve geliştirmeler `docs/YYYY-MM-DD_konu.md` standardıyla detaylı şekilde arşivlenmektedir:
* MVP Mimari & Veri Akışı: `docs/2026-08-17_mvp_mimari_veri_akisi_ve_afis_motoru.md`
* Canlı Fotoğraf Çekimi & Çoklu Açı Afişleri: `docs/2026-08-17_canli_katalog_gorsel_cekimi_ve_coklu_aci_afisleri.md`
* Next.js 15 Modern Vitrin & Stüdyo Dönüşümü: `docs/2026-08-18_nextjs_modern_vitrin_ve_studio_donusumu.md`
* Quiet Luxury Afiş Motoru & 3+1 Odaklı Kamera Açıları: `docs/2026-08-18_quiet_luxury_afis_motoru_ve_3_arti_1_aci_guncellemesi.md`
* Akıllı AI Danışman & Müşteri Takip Mimarisi: `docs/2026-08-18_akilli_ai_danisman_ve_musteri_takip_mimarisi.md`
* Bilişsel AI Satış Danışmanı & Dinamik Araç Önerisi: `docs/2026-08-18_bilissel_ai_satis_danismani_ve_dinamik_arac_onerisi.md`
* Türkçe İsim & Varlık Tanıma (NER) ve Doğru Hitap Mimarisi: `docs/2026-08-18_turkce_varlik_tanima_ve_dogru_hitap_sistemi.md`

## 5. Güncel Durum ve Sürekli Hafıza Kuralları
* **Mevcut Durum:** Bilişsel AI satış danışmanı, Türkçe varlık tanıma (NER), cinsiyete göre doğru hitap (Hanım/Bey/Sayın), tekil session takibi, bütçe esnetme ve sayfa filtresiyle tam entegre çalışmaktadır.
* **Kural:** Her mimari ve işlevsel güncellemeden sonra `PROJECT_MEMORY.md`, `.antigravity_rules.md`, `.cursorrules.md`, `.github/copilot-instructions.md`, `README.md` ve ilgili `docs/` belgesi eksiksiz güncellenmek zorundadır.
