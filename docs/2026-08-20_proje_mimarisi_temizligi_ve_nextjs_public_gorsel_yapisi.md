# 2026-08-20: Proje Mimarisi Temizliği, Next.js Public Görsel Yapısı & Test/DB Reset Raporu

**Tarih:** 2026-08-20  
**Yazar:** Antigravity AI  
**Kapsam:** Kök dizindeki eski `static/` kalıntılarının tamamen temizlenmesi, araç görsellerinin modern Next.js mimarisine uygun olarak `frontend/public/vehicle_images/` altına taşınması, kök dizindeki testlerin `tests/` dizini altında modülerleştirilmesi, veritabanının ve tüm boru hattının sıfırdan resetlenip 73 birim & entegrasyon testinden geçirilmesi.

---

## 1. Mimari İnceleme ve Yapılan İyileştirmeler

### A. Kök Dizindeki `static/` Karmaşasının Giderilmesi
* **Eski Durum:** Next.js öncesi v1/v2 prototipinden kalan `static/index.html`, `static/css/`, `static/js/` ve `static/vehicle_images/` kök dizinde dağınık durmaktaydı. Next.js 15 App Router (`frontend/`) varken kök dizinde `static/` bulunması mimari bütünlüğü bozuyordu.
* **Yeni Durum:** 
  1. `static/vehicle_images/` içerisindeki tüm showroom araç fotoğrafları doğrudan `frontend/public/vehicle_images/` dizinine aktarıldı.
  2. Kök dizindeki eski `static/` klasörü ve eski HTML/CSS/JS dosyaları tamamen silindi.
  3. `config.py` içinde `FRONTEND_DIR`, `FRONTEND_PUBLIC_DIR`, `FRONTEND_OUT_DIR` ve `VEHICLE_IMAGES_DIR` tanımları yapıldı.
  4. Scraper ve veritabanı kayıtları `/vehicle_images/{external_id}/image_{i}.jpg` formatına güncellendi.
  5. Next.js'in hem `npm run dev` hem de `npm run build` (`out/`) modunda görselleri doğrudan ve optimize sunması sağlandı.
  6. FastAPI (`backend/web/server.py`), `/vehicle_images` endpoint'ini doğrudan `frontend/public/vehicle_images` dizininden mount ederek sunar hale getirildi.

### B. Testlerin Modülerleştirilmesi (`tests/`)
* Kök dizindeki dağınık `tests_chatbot.py`, `tests_chatbot_suite.py` ve `tests_chat_reset_regression.py` dosyaları standart `tests/` paketine taşındı:
  - `tests/test_chatbot.py`
  - `tests/test_chatbot_suite.py`
  - `tests/test_chat_reset_regression.py`
  - `tests/test_architecture_and_assets.py` *(Yeni Mimari & Görsel Doğrulama Testi)*
  - `tests/test_web_server.py` *(Yeni FastAPI & Mount Entegrasyon Testi)*
* `unittest` otomatik keşif (`discover`) ile 73 testin tamamı 1 saniye gibi kısa bir sürede başarıyla koşmaktadır.

---

## 2. Güncel Dizin Yapısı (Senior Standartlarında)

```
arkas_2el_pazarlama_ai/
├── main.py                     # Ana orkestratör (CLI: --reset-db, --build-frontend vb.)
├── config.py                   # Merkezi konfigürasyon (DB, Host, Port, Dizin yolları)
├── requirements.txt            # Python bağımlılıkları (FastAPI, SQLAlchemy, httpx vb.)
├── docker-compose.yml          # PostgreSQL 17 veritabanı konteyneri
├── .env                        # Çevre değişkenleri
├── .env.example                # Örnek çevre değişkenleri
├── PROJECT_MEMORY.md           # Proje mimari hafızası
├── README.md                   # Proje kullanım ve geliştirme kılavuzu
├── .antigravity_rules.md       # Antigravity kuralları
├── .cursorrules.md             # Cursor AI kuralları
├── docs/                       # Tarih bazlı mimari dokümantasyon
├── backend/                    # Python Backend Katmanı
│   ├── agent/                  # AI Pazarlama & Bilişsel AI Satış Danışmanı Motoru
│   │   ├── chatbot/            # Bilişsel Niyet & CRM Motoru (state, nlu, search, tools, planner)
│   │   ├── chatbot_agent.py    # Facade
│   │   └── marketing_agent.py  # 3-Tonlu Metin Üretimi
│   ├── db/                     # Veritabanı & ORM (vehicles, vehicle_images, briefs, leads)
│   ├── scraper/                # Sahibinden & Spoticar S3 veri kazıma motoru
│   └── web/                    # FastAPI REST API & Next.js Mount
├── frontend/                   # Next.js 15 Vitrin & Stüdyo (App Router, Tailwind v4)
│   ├── public/                 # Statik Varlıklar
│   │   ├── vehicle_images/     # Araç Showroom Fotoğrafları (SHBDN-xxxx/image_x.jpg)
│   │   └── placeholder.svg     # Quiet Luxury Araç Görseli Hazırlanıyor Şablonu
│   ├── src/                    # React 19 bileşenleri, hooks ve sayfalar
│   └── out/                    # Next.js Production Derlemesi
└── tests/                      # 73 Kapsamlı Birim ve Entegrasyon Testi
    ├── test_architecture_and_assets.py
    ├── test_chat_reset_regression.py
    ├── test_chatbot.py
    ├── test_chatbot_suite.py
    └── test_web_server.py
```

---

## 3. Doğrulama ve Test Sonuçları

1. **Veritabanı ve Pipeline Sıfırlama (`main.py --reset-db --no-web`):**
   - PostgreSQL 17 veritabanı tabloları sıfırlandı.
   - 5 adet doğrulanmış Arkas Spoticar aracı kazındı.
   - 25 adet HD showroom fotoğrafı `frontend/public/vehicle_images/` dizinine indirildi.
   - AI Pazarlama Motoru ile 5 araca ait Safe, Bold, Story metinleri üretildi.
2. **Next.js Derlemesi (`main.py --build-frontend`):**
   - Next.js 15 statik export derlemesi tamamlandı ve `frontend/out/` dizinine görsellerle birlikte aktarıldı.
3. **Test Paketi (`python -m unittest discover -s tests`):**
   - **73 / 73 Test Başarılı (OK)**.
