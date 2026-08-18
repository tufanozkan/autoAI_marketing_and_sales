# Mimari Refactor — `src/` Dizininden `backend/` Dizinine Geçiş Raporu

**Tarih:** 18 Ağustos 2026  
**Kapsam:** Proje kök dizinindeki modüler Python kodlarının `src/` isimlendirmesinden, temiz Fullstack mimari standardı olan **`backend/`** isimlendirmesine geçirilmesi, tüm import ve modül yollarının güncellenmesi ve sistem testlerinin yapılması.  
**Durum:** Başarıyla Tamamlandı, Test Edildi ve Doğrulandı.  

---

## 🏛️ Yeni Dizin & Paket Mimarisi

```
arkas_2el_pazarlama_ai/
├── backend/                    # Python Backend Katmanı
│   ├── agent/                  # AI Pazarlama Metin Motoru & Bilişsel AI Asistan
│   │   ├── brand_rules.py      # Marka arketip kuralları
│   │   ├── chatbot_agent.py    # Türkçe NER, tekil oturum takibi, dinamik araç önerisi
│   │   └── marketing_agent.py  # 3-tonlu metinler ve Instagram Story akışı
│   ├── db/                     # PostgreSQL bağlantısı & SQLAlchemy ORM
│   │   ├── database.py         # SessionLocal & Engine yönetimi
│   │   └── models.py           # Vehicle, VehicleImage, CreativeBrief, CustomerLead ORM modelleri
│   ├── scraper/                # Canlı ilan kazıma ve görsel eşleştirme
│   │   ├── arkas_scraper.py    # Genel scraper altyapısı
│   │   ├── normalizer.py       # Donanım ve teknik özellik normalizasyonu
│   │   └── sahibinden_scraper.py# Sahibinden canlı verileri & Spoticar S3 görsel eşleştirici
│   └── web/                    # FastAPI REST API & Next.js Mount
│       └── server.py           # /api/chat, /api/leads, /api/vehicles, /api/stats
├── frontend/                   # Next.js 15 (React 19, TypeScript, Tailwind CSS v4) Vitrin & Studio
│   ├── src/app/                # Next.js App Router
│   ├── src/components/         # Vitrin bileşenleri ve stüdyo modalları
│   └── out/                    # Statik derleme çıktısı
├── main.py                     # Ana Orkestratör (`backend.web.server:app` uvicorn sunucusu)
├── config.py                   # Pydantic Settings ortam ayarları
├── .env                        # PostgreSQL & Scraper bağlantı parametreleri
└── docs/                       # Mimari dokümantasyon
```

---

## 🔍 Yapılan Güncellemeler:
1. `src/` klasörü `backend/` olarak yeniden adlandırıldı (`git mv src backend`).
2. Tüm Python modüllerinde `from src.` importları `from backend.` olarak güncellendi.
3. `main.py` dosyasındaki uvicorn başlatma komutu `"backend.web.server:app"` olarak ayarlandı.
4. `.antigravity_rules.md`, `.cursorrules.md`, `.github/copilot-instructions.md`, `PROJECT_MEMORY.md` ve `README.md` dosyaları yeni `backend/` mimarisine senkronize edildi.
5. Veritabanı ve API endpoint testleri çalıştırılarak %100 sorunsuz çalıştığı doğrulandı.
