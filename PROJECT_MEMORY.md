# PROJECT_MEMORY.md - Arkas 2. El Pazarlama AI

## 1. Proje Özeti ve Vizyon
* **Proje Adı:** Automotive AI Marketing Platform (Arkas 2. El Pazarlama AI)
* **Amaç:** 2. el araç verilerini toplayarak salt teknik özellik listelemek yerine; marka kimliği, hedef kitle ve duygusal satış noktalarına (emotional selling points) dayalı yüksek dönüşümlü reklam metinleri, kancalar ve hikayeler üreten, zengin orijinal fotoğraflarla sergileyen ve sayfayı dinamik kontrol eden Bilişsel AI Satış Danışmanı sunan yeni nesil platform.
* **Ana Felsefe:** "Bir araç kataloğu gibi değil, otomotiv pazarlama ajansı ve uzman satış danışmanı gibi düşün."

## 2. Teknoloji Yığını (Tech Stack)
* **Çekirdek Dil:** Python 3.11+ (FastAPI, SQLAlchemy 2.0, BeautifulSoup4, Requests, Pydantic v2)
* **Veritabanı:** PostgreSQL 17 (Host: `localhost`, Port: `5432`, DB: `arkas_marketing_db`, User: `postgres`, Password: `postgres`)
* **AI Metin Motoru:** `MarketingAgent` (Safe / Dengeli & Bold / İlgi Çekici reklam metinleri, kancalar, hikaye akışları)
* **AI Danışman & Bilişsel Niyet Motoru:** `ChatbotAgent` (Cognitive Intent Classifier, Turkish NER & Honorifics, Dynamic Cross-Vehicle Recommendation, Budget Expansion, Context-Aware Active Memory, PostgreSQL RAG + Canlı Ağ Bilgisi + Sayfa Filtre Aksiyonları)
* **Web Arayüzü & Vitrin:** **Next.js 15 (React 19, TypeScript, Tailwind CSS v4, Lucide React)** Minimalist Quiet Luxury Otomotiv Vitrin Stüdyosu (`frontend/`) + Yüzen AI Asistan Widget'ı
* **Veritabanı İstemci Desteği:** DBeaver tam entegrasyonu (`vehicles`, `customer_leads`, `creative_briefs`, `marketing_copies`)
* **Konfigürasyon:** `.env` (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, DATABASE_URL)

## 3. Mimari ve Modüler İş Akışı
1. **Veritabanı Katmanı (`backend/db/` & PostgreSQL 5432):**
   - 4 Tablolu Temiz Mimari: `vehicles`, `vehicle_images`, `creative_briefs`, `customer_leads`.
   - `VehicleImage`: Araç detay fotoğrafları (`image_url`, `is_primary`, `display_order`, `caption`).
2. **Kreatif & Metin Motoru (`backend/agent/marketing_agent.py`):**
   - Marka personasına göre 3-tonlu metinler (`balanced_copy`, `professional_copy`, `engaging_copy`), 3 sahneli Instagram Story akışları ve etiketler doğrudan `creative_briefs` tablosuna yazılır.
3. **Bilişsel AI Satış Danışmanı & Chatbot (`backend/agent/chatbot_agent.py` & `/api/chat`):**
   - Türkçe NER, Hanım/Bey hitap kuralı, tekil `session_id` bazlı `customer_leads` güncellemesi, dinamik çapraz model önerisi, bütçe esnetme ve sayfa filtreleme aksiyonları (`filter_action`).
4. **Modern Next.js Vitrin & Stüdyo (`frontend/` & `backend/web/`):**
   - Quiet Luxury tasarım dili, 5 açılı görsel galerisi, 4 metin sekmesi, "Bu aracın görseli bulunmamaktadır" rozeti ve yüzen AI Danışman Widget'ı.

## 4. Dokümantasyon Standartları (`docs/`)
* MVP Mimari & Veri Akışı: `docs/2026-08-17_mvp_mimari_veri_akisi_ve_afis_motoru.md`
* Canlı Fotoğraf Çekimi & Çoklu Açı Afişleri: `docs/2026-08-17_canli_katalog_gorsel_cekimi_ve_coklu_aci_afisleri.md`
* Next.js 15 Modern Vitrin & Stüdyo Dönüşümü: `docs/2026-08-18_nextjs_modern_vitrin_ve_studio_donusumu.md`
* Quiet Luxury Afiş Motoru & 3+1 Odaklı Kamera Açıları: `docs/2026-08-18_quiet_luxury_afis_motoru_ve_3_arti_1_aci_guncellemesi.md`
* Akıllı AI Danışman & Müşteri Takip Mimarisi: `docs/2026-08-18_akilli_ai_danisman_ve_musteri_takip_mimarisi.md`
* Bilişsel AI Satış Danışmanı & Dinamik Araç Önerisi: `docs/2026-08-18_bilissel_ai_satis_danismani_ve_dinamik_arac_onerisi.md`
* Türkçe İsim & Varlık Tanıma (NER) ve Doğru Hitap Mimarisi: `docs/2026-08-18_turkce_varlik_tanima_ve_dogru_hitap_sistemi.md`
* Görsel Motoru Temizliği & Kapsamlı Araç Şeması Hazırlığı: `docs/2026-08-18_gorsel_motoru_temizligi_ve_detayli_arac_semasi_hazirligi.md`
* Arkas Spoticar Veri Çıkarma (Parsing) & 3 Tonlu Metin Üretimi: `docs/2026-08-18_arkas_spoticar_veri_cikarma_ve_tonlu_metin_uretimi.md`
* Donanımlar Sekmesi Kategorik Görünüm & İstemci Hatası Çözümü: `docs/2026-08-18_donanimlar_kategorik_gosterim_ve_hata_cozumu.md`
* Canlı Envanter, %100 Gerçek KM & Fiyat ve Orijinal Fotoğraf Kazıma: `docs/2026-08-18_canli_envanter_gercek_km_fiyat_ve_orijinal_fotograf_kazima.md`
* Sahibinden.com "Arkas Spoticar" Gerçek Canlı Veri Kazıma & 3-Tonlu Metin Üretimi: `docs/2026-08-18_sahibinden_arkas_spoticar_canli_kazima_ve_metin_uretimi.md`
* Doğrudan Mağaza URL'si (`arkasspoticar.sahibinden.com`) 5 Araçlık Test & Görsel İyileştirmesi: `docs/2026-08-18_arkasspoticar_sahibinden_5_arac_testi_ve_gorsel_iyilestirmesi.md`
* Yerel Görsel İndirme & Ekspertiz Düzeltmesi: `docs/2026-08-18_yerel_gorsel_indirme_ve_ekspertiz_duzeltmesi.md`
* 4 Tablolu Yeni Şema, Vehicle Images Tablosu & Hafif Kazıma: `docs/2026-08-18_4_tablolu_yeni_sema_ve_vehicle_images_tablosu.md`
* Spoticar.com.tr Arkas İzmir 5 Açılı Orijinal Galeri Entegrasyonu: `docs/2026-08-18_spoticar_com_tr_5_acili_orijinal_galeri_entegrasyonu.md`
* Sahibinden Öncelikli Canlı Envanter & Spoticar CT1444T001 Görsel Eşleştirmesi: `docs/2026-08-18_sahibinden_oncelikli_spoticar_ct1444t001_eslestirmesi.md`
* Spoticar CT1444T001 — Peugeot 408, Honda City & Fiat Egea Orijinal Görsel Yenilemesi: `docs/2026-08-18_spoticar_408_city_egea_gorsel_yenilemesi.md`
* Sahibinden %100 Doğrulanmış Canlı İlan Verileri & Spoticar Görsel Eşleştirmesi: `docs/2026-08-18_sahibinden_kesin_dogrulanmis_5_arac_ve_spoticar_eslesmesi.md`
* Mimari Refactor — `src/` Dizininden `backend/` Dizinine Geçiş: `docs/2026-08-18_src_dizininin_backend_olarak_yeniden_yapilandirilmasi.md`
* Müşteri Odaklı Lüks Showroom Arayüzü Dönüşümü: `docs/2026-08-18_musteri_odakli_showroom_arayuzu_donusumu.md`
* Yapay Zeka Satış Danışmanı Beyaz LED Işıklı Buton & Üst Menü Temizliği: `docs/2026-08-18_yapay_zeka_danismani_led_isikli_buton_ve_ust_menu_temizligi.md`
* Yönetim Kurulu & Pitch Deck Sunumu: `docs/ARKAS_AI_PROJE_SUNUMU.md`
* Chatbot Kapsamlı Testleri ve Bilişsel Danışman İyileştirmeleri: `docs/2026-08-19_chatbot_testleri_ve_akilli_danisman_hata_duzeltmeleri.md`
* Türkçe Unisex ve Kapsamlı İsim Tanıma (NER) Mimarisi: `docs/2026-08-19_turkce_unisex_ve_genisletilmis_isim_tanima_mimarisi.md`
* Production AI Satış Danışmanı & Bilişsel Mimari Raporu: `docs/2026-08-19_production_ai_satis_danismani_ve_bilissel_mimari.md`

## 5. Güncel Durum ve Sürekli Hafıza Kuralları
* **Mevcut Durum:** 
  - AI Satış Danışmanı monolitik yapıdan modüler `backend/agent/chatbot/` bilişsel mimarisine (`state.py`, `nlu.py`, `search_engine.py`, `tools.py`, `planner.py`, `agent.py`) dönüştürülmüştür.
  - PostgreSQL 17 `CustomerLead` tablosuna `phone_declined`, `honorific_preference`, `budget_min`, `budget_max`, `active_filters`, `conversation_state_json` sütunları eklenmiş ve otomatik migrasyon devreye alınmıştır.
  - Türkçe NER, Unisex hitap tercihi sorma/hatırlama, Bütçe alt/üst/aralık ayrıştırma, Olumsuzlama (negation) kontrolü, Sıfır/2. el ayrımı, Çapraz donanım önerisi ve Next.js `filter_action` senkronizasyonu tamamlanmıştır.
  - 53 adet unittest ve konuşma akış testi ile %100 doğruluk sağlanmıştır (`tests_chatbot.py`, `tests_chatbot_suite.py`).
  - Next.js 15 prodüksiyon derlemesi (`npm run build`) başarıyla tamamlanmıştır.
* **Kural:** Her mimari ve işlevsel güncellemeden sonra `PROJECT_MEMORY.md`, `.antigravity_rules.md`, `.cursorrules.md`, `.github/copilot-instructions.md`, `README.md` ve ilgili `docs/` belgesi eksiksiz güncellenmek zorundadır.
