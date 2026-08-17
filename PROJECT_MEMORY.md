# PROJECT_MEMORY.md - Arkas 2. El Pazarlama AI

## 1. Proje Özeti ve Vizyon
* **Proje Adı:** Automotive AI Marketing Platform (Arkas 2. El Pazarlama AI)
* **Amaç:** 2. el araç ilan verilerini toplayarak salt teknik özellik listelemek yerine; marka kimliği, hedef kitle ve duygusal satış noktalarına (emotional selling points) dayalı yüksek dönüşümlü reklam metinleri, görsel konseptler, afişler ve sosyal medya kreatifleri üreten yapay zeka destekli pazarlama platformu.
* **Ana Felsefe:** "Bir araç kataloğu gibi değil, otomotiv pazarlama ajansı gibi düşün."

## 2. Teknoloji Yığını (Tech Stack)
* **Core / Data / ML Backend:** Python (LightGBM, TensorFlow, Data Scraping/Processing)
* **API / Middleware Backend:** Node.js (Express / NestJS / Fastify)
* **Frontend & Görselleştirme:** Next.js (Modern UI, Dynamic/Aesthetic)
* **Veritabanı:** PostgreSQL (İlişkisel + JSONB esnek şema)
* **Kuyruk / Önbellek (Öneri):** Redis + BullMQ / Celery (Asenkron AI/ML işleri ve API rate-limit optimizasyonu için)
* **AI Servisleri:** Claude API, OpenAI API (ve görsel üretim modelleri)
* **Yönetim & CLI:** Antigravity CLI (`agu` / `agy`)

## 3. Temel Modüller & Mimari Bileşenler
1. **Veri Toplama & Çıkarma (Scraping / Ingestion):** Hedef pazar yerlerinden araç ilan verilerinin çekilmesi ve normalize edilmesi.
2. **Araç Veri Deposu (Database Layer):** Araç künyesi, teknik donanım ve pazarlama metadatalarının PostgreSQL üzerinde saklanması.
3. **Pazarlama & Segment Zenginleştirme (Marketing Enrichment Engine):** Marka (Volvo, BMW, Mercedes vb.) ve Segment (SUV, Sedan vb.) kılavuzlarına göre müşteri personası ve duygusal argümanların eşleştirilmesi.
4. **AI İçerik & Kreatif Motoru (Generative AI Layer):** İlan metinleri, sosyal medya postları, reklam kancaları ve görsel konsept istemleri üretimi.
5. **Görsel / Banner Üretim Hattı (Creative Asset Pipeline):** İlan görselleri veya yapay zeka arka plan/şablon tasarımları ile pazarlama afişleri oluşturma.
6. **Yönetim Paneli & API (Dashboard & API):** İlan yönetimi, kreatif önizleme, dışa aktarma ve kampanya yönetimi arayüzü.

## 4. Güncel Durum ve Kararlar
* **Mevcut Durum:** Proje başlangıç aşamasında, kural ve standart dosyaları incelendi, hafıza dosyası başlatıldı.
* **Sıradaki Adım:** Kullanıcı ile mimari geliştirme planının netleştirilmesi ve ilk fazın (Scraping/Veritabanı/Servis iskeleti) tasarlanması.
