# Arkas 2. El Pazarlama AI (Automotive AI Marketing & Sales Platform)

Yapay zeka destekli, 2. el araç verilerini toplayıp marka ve müşteri kimliğine uygun **yüksek dönüşümlü pazarlama metinleri, Safe & Bold reklam kreatifleri, orijinal zengin fotoğraf galerisi ve sayfayı dinamik kontrol eden Bilişsel AI Satış Danışmanı** sunan yeni nesil otomotiv platformu.

---

## 🏗️ Mimari ve Dizin Yapısı

```
arkas_2el_pazarlama_ai/
├── main.py                     # Ana orkestratör (Scraper -> AI Metin Ajanı -> Web Sunucusu)
├── config.py                   # Merkezi konfigürasyon, DB bağlantısı, port ve ortam ayarları
├── requirements.txt            # Python bağımlılıkları (FastAPI, SQLAlchemy, psycopg2, httpx)
├── docker-compose.yml          # PostgreSQL 17 veritabanı konteyner yapılandırması
├── .env                        # Çevre değişkenleri ve DB bağlantı bilgileri
├── .env.example                # Örnek çevre değişkenleri şablonu
├── PROJECT_MEMORY.md           # Sürekli güncellenen mimari hafıza
├── README.md                   # Proje dokümantasyonu ve kullanım kılavuzu
├── docs/                       # Tarih bazlı detaylı mimari ve teknik geliştirme dokümanları
├── backend/
│   ├── agent/                  # AI Pazarlama Metin Motoru (MarketingAgent) & Bilişsel AI Danışman (ChatbotAgent)
│   │   ├── brand_rules.py      # Marka arketip kuralları
│   │   ├── chatbot_agent.py    # Facade & Geriye dönük uyumluluk köprüsü
│   │   ├── chatbot/            # Modüler Bilişsel AI Satış Danışmanı Motoru
│   │   │   ├── state.py        # Pydantic State, Criteria, ActionOffer şemaları
│   │   │   ├── nlu.py          # Türkçe NER, Unisex Hitap, Bütçe & Negation ayrıştırıcı
│   │   │   ├── search_engine.py# Parametrik PostgreSQL & JSONB donanım arama motoru
│   │   │   ├── tools.py        # Araç soru-cevap, SSS ve çapraz öneri araçları
│   │   │   ├── planner.py      # Bilişsel niyet planlayıcı ve yanıt orkestratörü
│   │   │   └── agent.py        # ChatbotAgent sınıfı
│   │   └── marketing_agent.py  # 3-tonlu (Dengeli, Kurumsal, İlgi Çekici) metin & Story akışı motoru
│   ├── db/                     # PostgreSQL bağlantısı & SQLAlchemy ORM modelleri
│   │   ├── database.py         # SessionLocal & Otomatik migrasyon
│   │   └── models.py           # Vehicle, VehicleImage, CreativeBrief, CustomerLead, TestDrive ORM modelleri
│   ├── scraper/                # Canlı ilan veri toplama & donanım normalizasyonu
│   │   ├── arkas_scraper.py    # Temel web scraper
│   │   ├── normalizer.py       # Donanım ve teknik alan temizliği
│   │   └── sahibinden_scraper.py# Sahibinden mağaza kazıma & Spoticar S3 görsel eşleştirici
│   └── web/                    # FastAPI REST API & Next.js Statik Mount
│       └── server.py           # /api/chat, /api/leads, /api/test-drives, /api/vehicles, /api/stats, /vehicle_images mount
├── frontend/                   # Next.js 15 (React 19, TypeScript, Tailwind CSS v4) Vitrin & Studio
│   ├── public/                 # Statik Varlıklar (vehicle_images/, placeholder.svg)
│   ├── src/app/                # Next.js App Router (globals.css, layout.tsx, page.tsx)
│   ├── src/components/         # Navbar, StatsSection, FilterToolbar, VehicleCard, ChatbotWidget, CreativeStudioModal
│   └── out/                    # Next.js statik export derlemesi (FastAPI tarafından sunulur)
└── tests/                      # 84 Kapsamlı Birim ve Entegrasyon Testi (Unittest Suite)
```

---

## 🚀 Hızlı Başlangıç

### 1. Ortamı Hazırlayın ve Bağımlılıkları Yükleyin
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Tek Komutla Tüm Sistemi Çalıştırın
```bash
python main.py
```
> Bu komut sırasıyla:
> 1. Web Scraper'ı çalıştırıp araçları detaylı teknik özellikleri ve fotoğraflarıyla PostgreSQL'e kaydeder (`vehicles`).
> 2. AI Marketing Agent ile reklam metinlerini üretir (`creative_briefs`, `marketing_copies`).
> 3. Web Vitrinini ve Bilişsel AI Danışmanı **http://localhost:8000** adresinde başlatır.

---

## 🤖 Bilişsel AI Satış Danışmanı Özellikleri

* **Sıfır Halüsinasyon Prensibi (Zero-Hallucination):** Fiyat, kilometre veya donanım uydurulmaz. PostgreSQL 17 tek ve mutlak gerçeklik kaynağıdır.
* **Gelişmiş Türkçe Varlık Tanıma (NER):** 1000+ isim sözlüğü ve negatif kelime filtresi. "Ceren ben ama numaramı vermiyorum" gibi karmaşık cümleleri tek seferde çözer.
* **Unisex İsim Hitap Yönetimi:** Deniz, Derya, Ege, Özgür gibi unisex isimlerde varsayım yapmaz; kullanıcıya Bey/Hanım tercihini sorar ve oturum boyunca hatırlar.
* **Gelişmiş Bütçe ve Olumsuzlama:** "1.5m üstü" (`min_price`), "1.5m altı" (`max_price`), "dizel olmasın", "manuel istemiyorum" gibi karmaşık Türkçe niyetleri doğru ayrıştırır.
* **Gerçek Sıfır / 2. El Ayrımı:** "Yeni/sıfır araç" talebinde gerçek 0 KM stok kontrolü yapar.
* **Lead Yakalama & Tekil Oturum:** Tekil `session_id` ile `customer_leads` kaydını günceller.
* **Dinamik Çapraz Öneri & Vitrin Filtreleme:** Eksik donanımlarda alternatif araç sunar, onaylandığında vitrini senkronize filtreler (`filter_action`).

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
* `vehicles` : İlan kimliği, marka, model, paket, yıl, km, fiyat, `technical_specs` (JSON), `ad_features` (JSON), `damage_expertise` (JSON), `image_urls` (JSON) ve SHA256 hash'i.
* `customer_leads` : Müşteri iletişim bilgileri, telefon reddi, hitap tercihi, bütçe aralığı, aktif filtreler, JSON sohbet durumu ve AI özeti.
* `creative_briefs` : Marka arketipi, hedef persona, duygusal satış noktaları ve kancalar.
* `marketing_copies` : Instagram post/hikaye metinleri, başlıklar, CTA ve hashtagler (Safe & Bold).

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
* [2026-08-18 Görsel Motoru Temizliği ve Kapsamlı Araç Şeması Hazırlığı](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_gorsel_motoru_temizligi_ve_detayli_arac_semasi_hazirligi.md)
* [2026-08-18 Arkas Spoticar Veri Çıkarma (Parsing) & 3 Tonlu Metin Üretimi](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_arkas_spoticar_veri_cikarma_ve_tonlu_metin_uretimi.md)
* [2026-08-18 Donanımlar Sekmesi Kategorik Görünüm & İstemci Hatası Çözümü](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_donanimlar_kategorik_gosterim_ve_hata_cozumu.md)
* [2026-08-18 Canlı Envanter, %100 Gerçek KM & Fiyat ve Orijinal Fotoğraf Kazıma](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_canli_envanter_gercek_km_fiyat_ve_orijinal_fotograf_kazima.md)
* [2026-08-18 Sahibinden.com "Arkas Spoticar" Gerçek Canlı Veri Kazıma & 3-Tonlu Metin Üretimi](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_sahibinden_arkas_spoticar_canli_kazima_ve_metin_uretimi.md)
* [2026-08-18 Doğrudan Mağaza URL'si (arkasspoticar.sahibinden.com) 5 Araçlık Test & Görsel İyileştirmesi](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_arkasspoticar_sahibinden_5_arac_testi_ve_gorsel_iyilestirmesi.md)
* [2026-08-18 Yerel Görsel İndirme & Ekspertiz Düzeltmesi](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_yerel_gorsel_indirme_ve_ekspertiz_duzeltmesi.md)
* [2026-08-18 4 Tablolu Yeni Şema, Vehicle Images Tablosu & Hafif Kazıma](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_4_tablolu_yeni_sema_ve_vehicle_images_tablosu.md)
* [2026-08-18 Spoticar.com.tr Arkas İzmir 5 Açılı Orijinal Galeri Entegrasyonu](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_spoticar_com_tr_5_acili_orijinal_galeri_entegrasyonu.md)
* [2026-08-18 Sahibinden Öncelikli Canlı Envanter & Spoticar CT1444T001 Görsel Eşleştirmesi](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_sahibinden_oncelikli_spoticar_ct1444t001_eslestirmesi.md)
* [2026-08-18 Spoticar CT1444T001 — Peugeot 408, Honda City & Fiat Egea Orijinal Görsel Yenilemesi](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_spoticar_408_city_egea_gorsel_yenilemesi.md)
* [2026-08-18 Sahibinden %100 Doğrulanmış Canlı İlan Verileri & Spoticar Görsel Eşleştirmesi](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_sahibinden_kesin_dogrulanmis_5_arac_ve_spoticar_eslesmesi.md)
* [2026-08-18 Mimari Refactor — src Dizininden backend Dizinine Geçiş](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_src_dizininin_backend_olarak_yeniden_yapilandirilmasi.md)
* [2026-08-18 Müşteri Odaklı Lüks Showroom Arayüzü Dönüşümü](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_musteri_odakli_showroom_arayuzu_donusumu.md)
* [2026-08-18 Yapay Zeka Satış Danışmanı Beyaz LED Işıklı Buton & Üst Menü Temizliği](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-18_yapay_zeka_danismani_led_isikli_buton_ve_ust_menu_temizligi.md)
* [2026-08-19 Chatbot Kapsamlı Testleri ve Bilişsel Danışman İyileştirmeleri](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-19_chatbot_testleri_ve_akilli_danisman_hata_duzeltmeleri.md)
* [2026-08-19 Türkçe Unisex ve Kapsamlı İsim Tanıma Mimarisi](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-19_turkce_unisex_ve_genisletilmis_isim_tanima_mimarisi.md)
* [2026-08-19 Production AI Satış Danışmanı & Bilişsel Mimari Raporu](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/2026-08-19_production_ai_satis_danismani_ve_bilissel_mimari.md)
* [🌟 Arkas AI Yönetim Kurulu & Yatırımcı Sunumu (Pitch Deck & Script)](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/docs/ARKAS_AI_PROJE_SUNUMU.md)