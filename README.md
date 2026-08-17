# Arkas 2. El Pazarlama AI (Automotive AI Marketing Platform)

Yapay zeka destekli, 2. el araç verilerini toplayıp marka ve müşteri kimliğine uygun **yüksek dönüşümlü pazarlama kreatifleri, reklam metinleri ve profesyonel afişler** üreten otomotiv pazarlama platformu.

---

## 🏗️ Mimari ve Dizin Yapısı

```
arkas_2el_pazarlama_ai/
├── main.py                     # Ana orkestratör (Scraper -> AI Sub-Agent -> Afiş Motoru -> Web Vitrini)
├── config.py                   # Merkezi konfigürasyon, DB bağlantısı, renkler ve boyutlar
├── requirements.txt            # Python bağımlılıkları (FastAPI, SQLAlchemy, psycopg2, Pillow, BeautifulSoup4)
├── docker-compose.yml          # PostgreSQL 17 veritabanı konteyner yapılandırması
├── .env                        # Çevre değişkenleri ve DB bağlantı bilgileri
├── .env.example                # Örnek çevre değişkenleri şablonu
├── PROJECT_MEMORY.md           # Sürekli güncellenen mimari hafıza
├── README.md                   # Proje dokümantasyonu ve kullanım kılavuzu
├── docs/                       # Tarih bazlı detaylı mimari ve teknik geliştirme dokümanları
│   └── 2026-08-17_mvp_mimari_veri_akisi_ve_afis_motoru.md
├── src/
│   ├── db/                     # Veritabanı katmanı
│   │   ├── database.py         # SQLAlchemy engine, connection pool ve session yönetimi
│   │   └── models.py           # Vehicle, CreativeBrief, MarketingCopy, Poster ORM modelleri
│   ├── scraper/                # Veri toplama ve normalizasyon
│   │   ├── arkas_scraper.py    # Canlı scraper & garantili fallback veri seti
│   │   └── normalizer.py       # Fiyat, KM, donanım temizleyici ve SHA256 içerik hash'i
│   ├── agent/                  # Pazarlama zenginleştirme & afiş motoru
│   │   ├── brand_rules.py      # Marka arketip kuralları (Volvo, BMW, Mercedes, Peugeot vb.)
│   │   ├── marketing_agent.py  # Persona, Safe & Bold reklam metinleri ve kancalar
│   │   └── poster_engine.py    # Pillow tabanlı 1080x1350 Instagram & 1200x630 Banner afiş render motoru
│   └── web/                    # Web sunucusu & API
│       └── server.py           # FastAPI REST API ve statik dosya sunucusu
└── static/                     # Web arayüzü ve üretilen görseller
    ├── index.html              # Modern afiş vitrini ve filtreleme stüdyosu
    ├── css/style.css           # Arkas kurumsal renkleri ve lüks karanlık tema
    ├── js/app.js               # Dinamik ızgara, modal, filtre ve indirme mantığı
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

### 2. PostgreSQL Veritabanını Başlatın (Opsiyonel / Gerekirse)
Yerel PostgreSQL 17 servisi çalışmıyorsa Docker veya Homebrew ile başlatabilirsiniz:
```bash
# Docker ile:
docker compose up -d

# veya macOS Homebrew ile:
brew services start postgresql@17
```

### 3. Tek Komutla Tüm Sistemi Çalıştırın
```bash
python main.py
```
> Bu komut sırasıyla:
> 1. Web Scraper'ı çalıştırıp araçları PostgreSQL'e kaydeder (`vehicles`).
> 2. AI Sub-Agent ile marka kimliğine göre pazarlama brief'i ve Safe/Bold reklam metinlerini üretir (`creative_briefs`, `marketing_copies`).
> 3. Pillow motoru ile yüksek çözünürlüklü Instagram Post (4:5) ve Web Banner afişlerini render eder (`posters`).
> 4. Web Görsel Vitrinini **http://localhost:8000** adresinde başlatır.

---

## 🗄️ DBeaver / PostgreSQL Bağlantı Bilgileri

PostgreSQL veritabanına DBeaver veya herhangi bir SQL istemcisinden bağlanmak için `.env` dosyasındaki ayarlar:

| Parametre | Değer |
| :--- | :--- |
| **Host** | `localhost` veya `127.0.0.1` |
| **Port** | `5432` |
| **Database** | `arkas_marketing_db` |
| **Username** | `postgres` |
| **Password** | `postgres` |

### PostgreSQL Tablo Yapısı
* `vehicles` : İlan kimliği, marka, model, yıl, km, fiyat, donanım listesi, görsel URL'si ve SHA256 içerik hash'i.
* `creative_briefs` : Marka arketipi, hedef persona, duygusal satış noktaları ve kancalar.
* `marketing_copies` : Instagram post/hikaye metinleri, başlıklar, CTA ve hashtagler (Safe & Bold).
* `posters` : Üretilen yüksek çözünürlüklü afişlerin yerel dosya yolları ve web önizleme URL'leri.

---

## ⚙️ Modüler CLI Seçenekleri

| Komut | Açıklama |
| :--- | :--- |
| `python main.py` | Scraper ➔ AI Agent ➔ Afiş Motoru ➔ Web Sunucusunu uçtan uca çalıştırır. |
| `python main.py --scrape-only` | Yalnızca web scraper'ı çalıştırır ve veritabanını günceller. |
| `python main.py --generate-only` | Veritabanındaki araçlar için reklam metinlerini ve afişleri üretir. |
| `python main.py --web-only` | Yalnızca Web Vitrin Sunucusunu ayağa kaldırır. |
| `python main.py --port 8080` | Özel port ile başlatır. |

---

## 📚 Dokümantasyon

Tüm mimari detaylar, veri akışı ve bileşen analizleri `docs/` klasöründe tarih sırasıyla saklanmaktadır:
* [2026-08-17 MVP Mimari, Veri Akışı ve Afiş Motoru Dokümanı](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-17_mvp_mimari_veri_akisi_ve_afis_motoru.md)