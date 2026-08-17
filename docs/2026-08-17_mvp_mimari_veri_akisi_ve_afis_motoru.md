# Arkas 2. El Pazarlama AI - MVP Mimari, Veri Akışı ve Afiş Motoru Dokümantasyonu
**Doküman Tarihi:** 17 Ağustos 2026  
**Versiyon:** 1.0.0 (MVP)  
**Yazar:** Kıdemli Yazılım Mimarı & Antigravity AI  

---

## 1. Giriş ve Proje Vizyonu

**Arkas 2. El Pazarlama AI**, 2. el otomotiv pazarındaki araç ilan verilerini ham teknik özellik listeleri olmaktan çıkarıp; marka kimliği, hedef müşteri personası ve duygusal satış argümanlarına (emotional selling points) dayalı **yüksek dönüşümlü reklam metinleri ve profesyonel pazarlama afişleri** üreten yeni nesil bir yapay zeka platformudur.

### Temel İlke
> *"Bir araç kataloğu gibi değil, otomotiv pazarlama ajansı gibi düşün."*

Geleneksel ilanlar yalnızca kilometre, beygir gücü veya boya durumunu sıralarken; bu platform her aracın temsil ettiği yaşam tarzını, güvenliğini, konforunu veya performansını öne çıkararak potansiyel alıcıda satın alma arzusu uyandırır.

---

## 2. Uçtan Uca Sistem Mimarisi

Sistem, sorumlulukların net olarak ayrıldığı (Separation of Concerns) 5 ana katmandan meydana gelir:

```
                                  [ Web İlan Kaynağı / Arkas 2. El ]
                                                  │
                                                  ▼
                                      ┌──────────────────────┐
                                      │  src/scraper/        │
                                      │  - Canlı Scraper     │
                                      │  - Normalizer        │
                                      │  - SHA-256 Hasher    │
                                      └──────────┬───────────┘
                                                 │
                                                 ▼
                                      ┌──────────────────────┐
                                      │  PostgreSQL 17 DB    │ ◄─── [ DBeaver GUI ]
                                      │  (localhost:5432)    │      (Tabloları Yönetme)
                                      └──────────┬───────────┘
                                                 │
                     ┌───────────────────────────┴───────────────────────────┐
                     ▼                                                       ▼
        ┌─────────────────────────┐                             ┌─────────────────────────┐
        │  src/agent/ (Metin)     │                             │  src/agent/ (Afiş)      │
        │  - Brand Rules Engine   │                             │  - Pillow Render Engine │
        │  - Brief Sentezi        │                             │  - 1080x1350 Post       │
        │  - Safe & Bold Metinler │                             │  - 1200x630 Banner      │
        └────────────┬────────────┘                             └────────────┬────────────┘
                     │                                                       │
                     └───────────────────────────┬───────────────────────────┘
                                                 │
                                                 ▼
                                      ┌──────────────────────┐
                                      │  src/web/ & static/  │
                                      │  - FastAPI REST API  │
                                      │  - Otomotiv Vitrini  │
                                      │  - Izgara & İndirme  │
                                      └──────────────────────┘
```

---

## 3. Veri Akışı (Data Flow Pipeline) - Adım Adım

Verinin ilk keşfedilme anından kullanıcının ekranında bir afiş ve reklam metni olarak görünmesine kadar geçen süreç:

### Adım 1: İlan Toplama (Scraping)
* `src/scraper/arkas_scraper.py` modülü `https://www.arkas2el.com` veya hedef ilan listeleme sayfasına HTTP istekleri gönderir.
* Canlı ağ kısıtlamaları veya erişim engelleri durumunda sistem, kesintisiz çalışmayı garanti eden 8 farklı markadan (Volvo, BMW, Mercedes-Benz, Peugeot, Opel, Volkswagen, Audi, Renault) oluşan zengin ve gerçekçi bir veri kümesine otomatik geçiş yapar.

### Adım 2: Veri Normalizasyonu ve Temizliği (`src/scraper/normalizer.py`)
* **Fiyat Temizliği:** `"4.850.000 TL"` veya `"1.450.000,00 TRY"` gibi metinler ayrıştırılarak sayısal `float` (`4850000.00`) ve para birimi `TRY/TL` haline getirilir.
* **Kilometre & Yıl:** Metin içindeki noktalar ve boşluklar temizlenerek tam sayı (`int`) formatına dönüştürülür.
* **Marka & Donanım Standardizasyonu:** Marka adları (örn. `"vw"` ➔ `"Volkswagen"`, `"mercedes"` ➔ `"Mercedes-Benz"`) ve donanım maddeleri normalize edilir.

### Adım 3: Idempotent Veritabanı Yazımı ve SHA-256 İçerik Hash'i
* Her aracın temel alanlarından (`brand + model + year + km + price + features + primary_image_url`) benzersiz bir **SHA-256 Hash** değeri hesaplanır.
* **Mükerrerlik Kontrolü:** İlan veritabanında zaten varsa ve hash değeri değişmemişse işlem atlanır (veritabanına gereksiz yazma yapılmaz).
* **Güncelleme Kontrolü:** Fiyat veya donanım değiştiyse veritabanındaki kayıt güncellenir.
* **Yeni Kayıt:** İlan ilk kez görülüyorsa `vehicles` tablosuna yeni satır olarak eklenir.

---

## 4. Veritabanı Katmanı & DBeaver Entegrasyonu

Proje, kurumsal standartlarda **PostgreSQL 17** veritabanı kullanmaktadır.

### DBeaver Bağlantı Parametreleri
* **Host:** `localhost` (veya `127.0.0.1`)
* **Port:** `5432`
* **Database:** `arkas_marketing_db`
* **Username:** `postgres`
* **Password:** `postgres`

### Veritabanı Şeması ve Tabloları

```sql
-- 1. Araç Ana Tablosu
CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR(100) UNIQUE NOT NULL,
    source VARCHAR(100) DEFAULT 'Arkas 2. El',
    url VARCHAR(500),
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    sub_model VARCHAR(150),
    year INT NOT NULL,
    km INT NOT NULL,
    price FLOAT NOT NULL,
    currency VARCHAR(10) DEFAULT 'TL',
    fuel_type VARCHAR(50),
    transmission VARCHAR(50),
    body_type VARCHAR(50),
    color VARCHAR(50),
    features JSON DEFAULT '[]'::json,
    expertise_note TEXT,
    image_urls JSON DEFAULT '[]'::json,
    primary_image_url VARCHAR(1000),
    content_hash VARCHAR(64) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Pazarlama Brief Tablosu
CREATE TABLE creative_briefs (
    id SERIAL PRIMARY KEY,
    vehicle_id INT REFERENCES vehicles(id) ON DELETE CASCADE,
    brand_archetype VARCHAR(100) NOT NULL,
    target_persona VARCHAR(255) NOT NULL,
    emotional_points JSON DEFAULT '[]'::json,
    tone_of_voice VARCHAR(100) NOT NULL,
    key_hooks JSON DEFAULT '[]'::json,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Reklam ve Sosyal Medya Metinleri Tablosu
CREATE TABLE marketing_copies (
    id SERIAL PRIMARY KEY,
    vehicle_id INT REFERENCES vehicles(id) ON DELETE CASCADE,
    variant VARCHAR(20) DEFAULT 'safe', -- 'safe' veya 'bold'
    headline VARCHAR(255) NOT NULL,
    hook VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    cta VARCHAR(150) NOT NULL,
    story_frames JSON DEFAULT '[]'::json,
    hashtags JSON DEFAULT '[]'::json,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Üretilen Afiş ve Banner Tablosu
CREATE TABLE posters (
    id SERIAL PRIMARY KEY,
    vehicle_id INT REFERENCES vehicles(id) ON DELETE CASCADE,
    poster_type VARCHAR(50) DEFAULT 'instagram_post', -- 'instagram_post' veya 'banner'
    file_path VARCHAR(500) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    title VARCHAR(255) NOT NULL,
    badge_text VARCHAR(100),
    theme_color VARCHAR(50) DEFAULT '#E30613',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 5. AI Pazarlama & Kreatif Sub-Agent (`src/agent/`)

Pazarlama motoru iki temel bileşenden oluşur:

### 1. Marka Arketip Kılavuzu (`src/agent/brand_rules.py`)
Platformda tanımlı markalar için kurumsal pazarlama kılavuzları uygulanır:
* **Volvo:** Güvenlik, aile koruması, İskandinav zarafeti, huzur ve uzun ömürlü trust.
* **BMW:** Saf sürüş zevki, M Sport dinamizmi, güç, başarı ve prestij.
* **Mercedes-Benz:** Üst düzey lüks, kusursuz konfor, yönetici sınıfı prestij.
* **Audi:** Teknoloji, inovasyon, fütüristik quattro hakimiyeti ve modern zeka.
* **Peugeot:** i-Cockpit fütüristik kabin, göz alıcı tasarım ve şehir şıklığı.
* **Opel:** Alman sağlamlığı, Pure Panel dijital kokpit, akılcı fiyat/performans.
* **Volkswagen:** Zamansız tasarım, istikrar ve yüksek ikinci el değeri.
* **Renault:** Akıllı şehir mobilitesi, ekonomik sürüş ve dinamizm.

### 2. Çift Varyantlı Reklam Metinleri Üretimi
Her araç için iki farklı alıcı psikolojisine hitap eden metin üretilir:
1. **Safe (Kurumsal & Şeffaf):** Arkas 2. El ekspertiz güvencesine, servis geçmişine ve rasyonel donanım faydalarına odaklanır.
2. **Bold (Duygusal & Yaşam Tarzı):** Tutkuya, aracın sunduğu statüye, sürüş hissine ve aciliyet kurgusuna odaklanır.
3. **Instagram Story Akışı:** 3 aşamalı (Kanca ➔ Donanım/Deneyim ➔ Fırsat/CTA) hikaye senaryosu.
4. **Hashtag Kümesi:** Marka, model ve kampanya bazlı dinamik etiketler.

---

## 6. Yüksek Çözünürlüklü Afiş & Banner Render Motoru (`src/agent/poster_engine.py`)

Pillow (Python Imaging Library) kullanılarak piksel düzeyinde profesyonel grafik afişler üretilir.

### Katman Katman Render Mantığı:
1. **Degrade Arka Plan:** Koyu lüks arduvaz mavisi (`#0F172A` - Slate 900) zemin üzerine sağ üst köşeden yayılan ambient radyal ışık efekti.
2. **Kurumsal Başlık Şeridi:** Üstte Arkas Kırmızısı (`#E30613`) yuvarlatılmış hap rozet ("ARKAS 2. EL GÜVENCESİYLE") ve sağda model yılı rozeti (`2023 MODEL`).
3. **Fotoğraf Kartı & Maske:** Aracın yüksek çözünürlüklü fotoğrafı çekilir, 30px yuvarlatılmış köşe maskesiyle kırpılır, arkasına cam efektli ince kenarlık ve gölge uygulanır.
4. **Tipografi & Hiyerarşi:**
   - Kırmızı renkte büyük harf marka etiketi (`VOLVO`, `BMW` vb.).
   - Beyaz renkte kalın model adı (`XC90 2.0 B5 AWD Inscription`).
   - 3 adet koyu gri donanım hapı: `📍 Kilometre`, `⛽ Yakıt Tipi`, `⚙️ Şanzıman`.
5. **Öne Çıkan Donanım Maddeleri:** Aracın en vurucu 3 özelliği (`• Bowers & Wilkins Ses`, `• Panoramik Cam Tavan` vb.) madde işaretleriyle sıralanır.
6. **Alt Fiyat & Eylem Kartı (Footer Bar):**
   - Arkas Kırmızısı zemin üzerine 58pt ekstra kalın beyaz fiyat (`4.850.000 TL`).
   - "Detaylar & Randevu İçin Hemen İletişime Geçin" alt başlığı.
   - Sağ tarafta beyaz buton içinde kırmızı yazı: `"İNCELE & AL >"`.

### Üretilen Formatlar:
* **Instagram Dikey Post:** `1080 x 1350 px` (4:5 Format) ➔ `static/generated_posters/poster_{id}_post.png`
* **Web & Sosyal Banner:** `1200 x 630 px` (16:9 Format) ➔ `static/generated_posters/poster_{id}_banner.png`

---

## 7. Web Görsel Vitrini & REST API (`src/web/` & `static/`)

FastAPI backend sunucusu ve Vanilla CSS/JS tabanlı modern kullanıcı arayüzü:

### REST API Uç Noktaları
* `GET /api/stats` : Toplam araç, aktif afiş, reklam metni ve marka sayıları.
* `GET /api/brands` : Veritabanındaki benzersiz markaların listesi.
* `GET /api/vehicles?brand=...&body_type=...&search=...` : Filtrelenmiş araç ve kreatif listesi.
* `GET /api/vehicles/{id}` : Tek bir aracın brief, metin ve afiş detayları.
* `POST /api/pipeline/run` : Scraper + AI Agent + Afiş Motorunu web üzerinden anında tetikler.
* `POST /api/pipeline/generate-single/{id}` : Seçilen araç için afiş ve metinleri tek tıkla yeniden üretir.

### Ön Yüz (Frontend) Özellikleri
* **Lüks Otomotiv Teması:** Arkas Kırmızı (`#E30613`), Gece Mavisi (`#002B49`) ve Koyu Zemin (`#0B1120`).
* **Anlık Filtreleme:** Marka sekmelerine tıklandığında veya kasa tipi seçildiğinde sayfa yenilenmeden ızgaranın güncellenmesi.
* **Detay Modalı:**
  * 4:5 Instagram ve 16:9 Banner arasında anlık geçiş.
  * Tek tıkla yüksek çözünürlüklü PNG indirme.
  * Safe / Bold / Story metin sekmeleri.
  * Panoya kopyalama (Clipboard API) ve toast bildirimi.
  * "⚡ Yeniden Üret" butonu.

---

## 8. CLI ve Çalıştırma Komutları

```bash
# 1. Sanal ortamı aktif etme
source .venv/bin/activate

# 2. Tüm sistemi uçtan uca çalıştırma (Scraper -> AI -> Afiş -> Web UI)
python main.py

# 3. Yalnızca Web Scraper'ı çalıştırma
python main.py --scrape-only

# 4. Yalnızca AI Metin ve Afiş Motorunu çalıştırma
python main.py --generate-only

# 5. Yalnızca Web Görsel Vitrinini ayağa kaldırma
python main.py --web-only
```

---

## 9. Gelecek Fazlar & Genişletme Planı

1. **Gelişmiş LLM Entegrasyonu:** Claude 3.5 Sonnet / OpenAI GPT-4o API anahtarları eklenerek daha dinamik ve yaratıcı metin varyasyonlarının üretilmesi.
2. **Sosyal Medya Dağıtım Motoru:** Onaylanan afiş ve metinlerin Instagram / Meta Graph API üzerinden otomatik zamanlanıp paylaşılması.
3. **Arka Plan Değiştirme (AI Inpainting):** Araç fotoğraflarının stüdyo veya doğa arka planlarına yapay zeka ile otomatik yerleştirilmesi.
