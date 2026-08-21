# 🚗 AutoAI Showroom — AI-Powered Automotive Marketing & Sales Consultant Platform

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js 15](https://img.shields.io/badge/Frontend-Next.js%2015-black.svg?style=flat&logo=next.js)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%2017-336791.svg?style=flat&logo=postgresql)](https://www.postgresql.org)
[![Tailwind CSS v4](https://img.shields.io/badge/Styling-Tailwind%20CSS%20v4-38B2AC.svg?style=flat&logo=tailwind-css)](https://tailwindcss.com)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat&logo=python)](https://python.org)
[![Tests Passing](https://img.shields.io/badge/Tests-85%20Passed-brightgreen.svg?style=flat)]()

**AutoAI Showroom**, ikinci el otomotiv envanterini toplayan, her araç için **3 farklı reklam personası (Dengeli, Kurumsal, İlgi Çekici) ve sosyal medya afiş kancaları üreten**, 5 açılı yüksek çözünürlüklü vitrin sunan ve web vitrinini canlı olarak filtreleyip test sürüşü randevuları organize eden **Bilişsel Yapay Zeka Satış Danışmanı** içeren uçtan uca akıllı bir otomotiv pazarlama platformudur.

---

## ✨ Temel Özellikler

### 1. 🤖 Bilişsel AI Satış Danışmanı (Cognitive AI Sales Consultant)
* **Türkçe NER & Akıllı Hitap:** 1.000+ Türkçe isim veritabanı ile müşterinin adını, soyadını tanır. Unisex isimlerde (*Deniz, Derya, Özgür*) nezaketle hitap tercihini sorar ve oturum boyunca hatırlar.
* **Akıllı Bütçe ve Olumsuzluk Ayrıştırma:** *"1.5m altı"*, *"2 milyon bütçem var"*, *"dizel olmasın"*, *"manuel istemiyorum"* gibi karmaşık bütçe ve olumsuz filtreleri hatasız olarak parametrik SQL sorgularına dönüştürür.
* **Sıfır Halüsinasyon ve Sayfa Kontrolü:** Sadece stokta gerçekten bulunan araçları önerir. Sohbet sırasında arayüzdeki Next.js filtrelerini arka planda gerçek zamanlı günceller.
* **Test Sürüşü & Randevu Yönetimi:** Tarih/saat tespit motoru (*"Yarın saat 14:00"* / *"21 Ağustos 15:00"*) ile randevuları PostgreSQL `test_drives` tablosuna kaydeder. Telefon paylaşımı istemeyen müşterilere randevusuz doğrudan showroom ziyaret alternatifleri sunar.

### 2. 🎨 AI Kreatif Pazarlama Motoru (Marketing Copy Generator)
* **3 Farklı Reklam Tonu:**
  * **Safe (Dengeli):** Güven, ekspertiz güvencesi ve konfor odaklı klasik reklam kurgusu.
  * **Professional (Kurumsal):** Finansman, TCO ve teknik verimlilik odaklı net metin.
  * **Bold (İlgi Çekici):** Sosyal medya, Instagram Reels ve TikTok için dinamik hooklar, emoji zenginliği ve doğrudan harekete geçirici mesajlar (CTA).
* **Story & Post Akışları:** 5 açılı orijinal showroom fotoğraflarıyla uyumlu 3 adımlı Instagram Story senaryoları üretir.

### 3. 🏎️ Modern Next.js 15 & Tailwind CSS v4 Dijital Showroom
* **Quiet Luxury UI Tasarımı:** Sıcak keten/bej zemin, alabaster kartlar ve şampanya detaylarıyla modern tasarım.
* **5 Açılı Orijinal Fotoğraf Galerisi:** Her araç için ön, arka, kokpit, yan profil ve konsol fotoğrafları.
* **Kreatif Stüdyo Modu:** Tek tıkla açılan modalda aracın tüm teknik detayları, 100+ nokta ekspertiz raporu ve üretilen AI reklam kreatifleri.

---

## 🏗️ Mimari ve Dizin Yapısı

```
auto_ai_showroom/
├── main.py                     # Ana orkestratör (Scraper -> AI Metin Ajanı -> Web Sunucusu)
├── config.py                   # Merkezi konfigürasyon, DB bağlantısı, port ve ortam ayarları
├── requirements.txt            # Python bağımlılıkları (FastAPI, SQLAlchemy, psycopg2, httpx)
├── docker-compose.yml          # PostgreSQL veritabanı konteyner yapılandırması
├── .env.example                # Örnek çevre değişkenleri şablonu
├── README.md                   # Proje dokümantasyonu ve kullanım kılavuzu
├── backend/
│   ├── agent/                  # AI Pazarlama Metin Motoru & Bilişsel AI Danışman
│   │   ├── brand_rules.py      # Marka arketip kuralları ve tonlama şablonları
│   │   ├── chatbot_agent.py    # Facade & Geriye dönük uyumluluk köprüsü
│   │   ├── chatbot/            # Modüler Bilişsel AI Satış Danışmanı Motoru
│   │   │   ├── state.py        # Pydantic State, Criteria, ActionOffer şemaları
│   │   │   ├── nlu.py          # Türkçe NER, Unisex Hitap, Bütçe & Tarih ayrıştırıcı
│   │   │   ├── search_engine.py# Parametrik PostgreSQL & JSONB donanım arama motoru
│   │   │   ├── tools.py        # Araç soru-cevap, SSS ve çapraz öneri araçları
│   │   │   ├── planner.py      # Bilişsel niyet planlayıcı ve yanıt orkestratörü
│   │   │   └── agent.py        # ChatbotAgent sınıfı
│   │   └── marketing_agent.py  # 3-tonlu pazarlama metni ve reklam brief motoru
│   ├── db/                     # PostgreSQL bağlantısı & SQLAlchemy ORM modelleri
│   │   ├── database.py         # SessionLocal & Otomatik tablo başlatma
│   │   └── models.py           # Vehicle, VehicleImage, CreativeBrief, CustomerLead, TestDrive ORM modelleri
│   ├── scraper/                # Canlı ilan veri toplama & donanım normalizasyonu
│   │   ├── arkas_scraper.py    # Showroom veri toplayıcı
│   │   ├── normalizer.py       # Donanım ve teknik alan temizliği
│   │   └── sahibinden_scraper.py# Doğrulanmış test seti & görsel indirici
│   └── web/                    # FastAPI REST API & Next.js Statik Mount
│       └── server.py           # /api/chat, /api/leads, /api/test-drives, /api/vehicles, /api/stats
├── frontend/                   # Next.js 15 (React 19, TypeScript, Tailwind CSS v4) Vitrin & Studio
│   ├── public/                 # Statik Varlıklar (vehicle_images/, placeholder.svg)
│   ├── src/app/                # Next.js App Router (globals.css, layout.tsx, page.tsx)
│   ├── src/components/         # Navbar, FilterToolbar, VehicleCard, ChatbotWidget, CreativeStudioModal
│   └── out/                    # Next.js statik export derlemesi (FastAPI tarafından sunulur)
└── tests/                      # 85 Kapsamlı Birim ve Entegrasyon Testi (Unittest Suite)
```

---

## 🚀 Hızlı Başlangıç

### 1. Depoyu Klonlayın ve Ortamı Hazırlayın

```bash
git clone https://github.com/kullanici_adiniz/auto-ai-showroom.git
cd auto-ai-showroom

# Python sanal ortamı oluşturun ve aktifleştirin
python3 -m venv .venv
source .venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### 2. Çevre Değişkenlerini Ayarlayın

```bash
cp .env.example .env
```

`.env` dosyasındaki veritabanı bağlantı bilgilerini kendi ortamınıza göre güncelleyin. İsteğe bağlı olarak Gemini/OpenAI API anahtarınızı ekleyebilirsiniz (API anahtarı olmasa dahi yerleşik zengin şablon motoruyla %100 çevrimdışı çalışabilir).

### 3. Veritabanını Başlatın (Docker)

```bash
docker-compose up -d
```

### 4. Tek Komutla Sistemi Çalıştırın

```bash
# Veritabanını kurar, araç verilerini işler, kreatifleri üretir ve vitrini açar:
python main.py
```

Web vitrinine tarayıcınızdan erişin:
👉 **http://localhost:8000**

---

## 🖥️ CLI Kullanım Seçenekleri

`main.py` dosyasını farklı ihtiyaçlarınıza göre parametrelerle çalıştırabilirsiniz:

| Komut | Açıklama |
| :--- | :--- |
| `python main.py` | Standart Akış: Scraper -> AI Pazarlama Ajanı -> Web Sunucusu |
| `python main.py --reset-db` | Veritabanı tablolarını sıfırlar ve test setini sıfırdan oluşturur |
| `python main.py --scrape-only` | Yalnızca web veri toplayıcıyı çalıştırır |
| `python main.py --generate-only` | Yalnızca AI pazarlama brief ve reklam metinlerini üretir |
| `python main.py --web-only` | Yalnızca FastAPI & Next.js vitrin sunucusunu başlatır |
| `python main.py --build-frontend` | Next.js arayüzünü derler (`frontend/out` klasörüne aktarır) |
| `python main.py --limit 10` | İşlenecek araç sayısını sınırlar |

---

## 🧪 Testleri Çalıştırma

Projede NLU ayrıştırıcı, diyalog akışları, randevu motoru, REST API ve statik varlıkları doğrulayan **85 adet kapsamlı birim ve entegrasyon testi** bulunmaktadır.

```bash
# Tüm testleri çalıştırmak için:
.venv/bin/python -m unittest discover tests
```

---

## 🌐 REST API Uç Noktaları

| Metot | Uç Nokta | Açıklama |
| :--- | :--- | :--- |
| `POST` | `/api/chat` | Bilişsel AI Danışman ile diyalog ve filtreleme yanıtı |
| `POST` | `/api/chat/reset` | Sohbet oturumunu ve aktif araç filtrelerini sıfırlama |
| `GET` | `/api/vehicles` | Filtrelenebilir araç listesi ve galeri bilgisi |
| `GET` | `/api/vehicles/{id}` | Tek bir aracın teknik, ekspertiz ve kreatif detayları |
| `GET` | `/api/leads` | Müşteri ad, telefon ve tercih özeti listesi |
| `GET` | `/api/test-drives` | Onaylanan test sürüşü randevuları |
| `GET` | `/api/stats` | Envanter, marka dağılımı ve lead istatistikleri |
| `POST` | `/api/pipeline/run` | Veri toplama ve kreatif üretim döngüsünü tetikleme |

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) altında açık kaynak olarak sunulmaktadır.