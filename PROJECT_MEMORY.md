# PROJECT_MEMORY.md - Arkas 2. El Pazarlama AI

## 1. Proje Özeti ve Vizyon
* **Proje Adı:** Automotive AI Marketing Platform (Arkas 2. El Pazarlama AI)
* **Amaç:** 2. el araç ilan verilerini toplayarak salt teknik özellik listelemek yerine; marka kimliği, hedef kitle ve duygusal satış noktalarına (emotional selling points) dayalı yüksek dönüşümlü reklam metinleri, görsel konseptler, afişler ve sosyal medya kreatifleri üreten yapay zeka destekli pazarlama platformu.
* **Ana Felsefe:** "Bir araç kataloğu gibi değil, otomotiv pazarlama ajansı gibi düşün."

## 2. Teknoloji Yığını (Tech Stack)
* **Çekirdek Dil:** Python 3.11+ (FastAPI, SQLAlchemy 2.0, Pillow, BeautifulSoup4, Requests, Pydantic v2)
* **Veritabanı:** PostgreSQL 17 (Host: `localhost`, Port: `5432`, DB: `arkas_marketing_db`, User: `postgres`, Password: `postgres`)
* **Konteyner Altyapısı:** `docker-compose.yml` (PostgreSQL 17)
* **Görsel / Afiş Render Motoru:** Pillow Tabanlı Grafik Motoru (1080x1350 Instagram 4:5 Post & 1200x630 Web/Sosyal Medya Banner)
* **Web Arayüzü & Vitrin:** Vanilla JS / Modern CSS3 Lüks Otomotiv Vitrin Stüdyosu
* **Veritabanı İstemci Desteği:** DBeaver tam entegrasyonu
* **Konfigürasyon:** `.env` (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, DATABASE_URL)

## 3. Mimari ve Modüler İş Akışı
1. **Veritabanı Katmanı (`src/db/` & PostgreSQL 5432):** DBeaver ve dış GUI araçlarıyla doğrudan bağlanılabilir; `vehicles`, `creative_briefs`, `marketing_copies` ve `posters` tabloları aktiftir.
2. **Ana Orkestratör (`main.py`):** Tek komutla (`python main.py`) sırasıyla tüm adımları tetikler veya bağımsız CLI bayraklarıyla (`--scrape-only`, `--generate-only`, `--web-only`) çalışır.
3. **Web Scraper Modülü (`src/scraper/`):** İlanları çeker, normalize eder, SHA256 içerik hash'i ile mükerrerlik olmadan PostgreSQL'e kaydeder.
4. **Pazarlama & Afiş Sub-Agent (`src/agent/`):** Marka ve segment arketip kurallarını (Volvo güvenliği, BMW sürüş hazzı, Mercedes prestiji vb.) işleyerek Safe/Bold reklam metinleri, kancalar ve yüksek çözünürlüklü afişler üretir.
5. **Web Görsel Vitrini (`src/web/` & `static/`):** PostgreSQL'den beslenen marka/model/kasa tipi filtrelemeli, anlık arama destekli ve afiş indirme özellikli şık bir ızgara (grid) sunar.

## 4. Dokümantasyon Standartları (`docs/`)
* Yapılan tüm mimari kararlar ve geliştirmeler `docs/YYYY-MM-DD_konu.md` standardıyla detaylı şekilde arşivlenmektedir.
* İlk MVP dokümantasyonu: `docs/2026-08-17_mvp_mimari_veri_akisi_ve_afis_motoru.md`

## 5. Güncel Durum ve Kararlar
* **Mevcut Durum:** Sistem tamamen PostgreSQL 17 (localhost:5432) üzerinde çalışmakta, `.env` ayrıştırılmış değişkenleri desteklemekte, tüm gereksiz dosyalar temizlenmiş ve afişler kusursuz render edilmektedir.
* **Sıradaki Adım:** İhtiyaç halinde LLM API entegrasyonları (Claude/OpenAI), sosyal medya dağıtım modülleri ve ek şablon varyantlarının geliştirilmesi.
