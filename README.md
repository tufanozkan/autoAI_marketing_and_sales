# Arkas 2. El Pazarlama AI (Automotive AI Marketing & Sales Platform)

Yapay zeka destekli, 2. el araç verilerini toplayıp marka ve müşteri kimliğine uygun **yüksek dönüşümlü pazarlama kreatifleri, Quiet Luxury afişler ve sayfayı dinamik kontrol eden Bilişsel AI Satış Danışmanı** sunan yeni nesil otomotiv platformu.

---

## 🏗️ Mimari ve Dizin Yapısı

```
arkas_2el_pazarlama_ai/
├── main.py                     # Ana orkestratör (Scraper -> AI Agent -> Quiet Luxury Motoru -> Web Sunucusu)
├── config.py                   # Merkezi konfigürasyon, DB bağlantısı, renkler ve boyutlar
├── requirements.txt            # Python bağımlılıkları (FastAPI, SQLAlchemy, psycopg2, Pillow, BeautifulSoup4)
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
│   └── 2026-08-18_bilissel_ai_satis_danismani_ve_dinamik_arac_onerisi.md
├── src/
│   ├── db/                     # Veritabanı katmanı
│   │   ├── database.py         # SQLAlchemy engine, connection pool ve session yönetimi
│   │   └── models.py           # Vehicle, CustomerLead, CreativeBrief, MarketingCopy, Poster ORM modelleri
│   ├── scraper/                # Veri toplama ve normalizasyon
│   │   ├── arkas_scraper.py    # Canlı scraper & garantili fallback veri seti
│   │   └── normalizer.py       # Fiyat, KM, donanım temizleyici ve SHA256 içerik hash'i
│   ├── agent/                  # Pazarlama zenginleştirme & Bilişsel AI Asistan
│   │   ├── brand_rules.py      # Marka arketip kuralları (Volvo, BMW, Mercedes, Peugeot vb.)
│   │   ├── marketing_agent.py  # Persona, Safe & Bold reklam metinleri ve kancalar
│   │   ├── poster_engine.py    # Quiet Luxury afiş ve banner motoru
│   │   └── chatbot_agent.py    # Bilişsel AI Satış Danışmanı (Lead alma, DB RAG, bütçe esnetme, donanım önerisi)
│   └── web/                    # Web sunucusu & REST API
│       └── server.py           # FastAPI REST API (/api/chat, /api/leads, /api/vehicles vb.) ve Next.js mount
├── frontend/                   # Next.js 15 Modern Lüks Vitrin ve Stüdyo (App Router)
│   ├── src/app/                # Next.js App Router (globals.css, layout.tsx, page.tsx)
│   ├── src/components/         # Navbar, StatsSection, FilterToolbar, VehicleCard, ChatbotWidget, CreativeStudioModal
│   └── out/                    # Statik export çıktısı (FastAPI tarafından servis edilir)
└── static/
    └── generated_posters/      # Üretilen yüksek çözünürlüklü afişler (.png)
```

---

## 🚀 Hızlı Başlangıç

### 1. Ortamı Hazırlayın ve Bağımlılıkları Yükleyin
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Frontend Bağımlılıklarını Kurun ve Derleyin (Opsiyonel / Geliştirme İçin)
```bash
cd frontend
npm install
npm run build
cd ..
```

### 3. Tek Komutla Tüm Sistemi Çalıştırın
```bash
python main.py
```
> Bu komut sırasıyla:
> 1. Web Scraper'ı çalıştırıp canlı Arkas kataloğunu PostgreSQL'e kaydeder (`vehicles`).
> 2. AI Marketing Agent ile reklam metinlerini üretir (`creative_briefs`, `marketing_copies`).
> 3. Quiet Luxury motoru ile afişleri hazırlar (`posters`).
> 4. Web Vitrinini ve Bilişsel AI Asistanı **http://localhost:8000** adresinde başlatır.

---

## 🤖 Bilişsel AI Satış Danışmanı & Chatbot Özellikleri

* **Lead Yakalama & Tekil Oturum:** Müşterinin ad, soyad ve telefonunu alarak `customer_leads` tablosunda tek bir oturum kaydı (`session_id`) açar.
* **Doğrudan İnsansı Q&A:** Vites, kilometre, ekspertiz ve yakıt sorularına şablon değil net ve samimi yanıt verir.
* **Bütçe Esnetme (Budget Expansion):** *"Fiyat aralığını 5m kadar çıkart"* dendiğinde bütçeyi günceller, portföydeki tüm araçları donanım ayrıcalıklarıyla sunar.
* **Çapraz Donanım Önerisi:** Odaktaki araçta (Skoda Kamiq) direksiyon/koltuk ısıtma yoksa takılı kalmaz; portföyü tarayıp bu donanıma sahip **Volvo XC40 Plus Dark** modeline geçiş yapar ve sayfayı Volvo için anında filtreler.
* **Showroom Özeti:** DBeaver üzerinden satış ekibinin müşterinin ne istediğini tek bakışta görebileceği `conversation_summary` üretir.

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
* `customer_leads` : Müşteri iletişim bilgileri, ilgilenilen marka/kasa, bütçe, tam sohbet dökümü ve AI sohbet özeti.
* `vehicles` : İlan kimliği, marka, model, yıl, km, fiyat, donanım listesi, görsel URL'leri ve SHA256 içerik hash'i.
* `creative_briefs` : Marka arketipi, hedef persona, duygusal satış noktaları ve kancalar.
* `marketing_copies` : Instagram post/hikaye metinleri, başlıklar, CTA ve hashtagler (Safe & Bold).
* `posters` : Üretilen afişlerin yerel dosya yolları ve web önizleme URL'leri.

---

## ⚙️ Modüler CLI Seçenekleri

| Komut | Açıklama |
| :--- | :--- |
| `python main.py` | Scraper ➔ AI Agent ➔ Afiş Motoru ➔ Web Sunucusunu uçtan uca çalıştırır. |
| `python main.py --reset-db --limit 5` | Veritabanını sıfırlar, 5 araçlık test seti çeker ve sunucuyu açar. |
| `python main.py --reset-db --no-web --limit 5` | Veritabanını sıfırlar, 5 aracı işler ve sunucuyu açmadan çıkar. |
| `python main.py --scrape-only` | Yalnızca web scraper'ı çalıştırır ve veritabanını günceller. |
| `python main.py --generate-only` | Veritabanındaki araçlar için reklam metinlerini üretir. |
| `python main.py --web-only` | Yalnızca Web Vitrin Sunucusunu ayağa kaldırır. |
| `python main.py --build-frontend` | Next.js arayüzünü derler (`npm run build`). |

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