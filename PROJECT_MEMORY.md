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
   - 5 Tablolu Temiz Mimari: `vehicles`, `vehicle_images`, `creative_briefs`, `customer_leads`, `test_drives`.
   - `VehicleImage`: Araç detay fotoğrafları (`image_url`, `is_primary`, `display_order`, `caption`).
   - `TestDrive`: Test sürüşü ve showroom randevu kayıtları (`appointment_datetime_text`, `customer_phone`, `status`).
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
* Proje Mimarisi Temizliği, Next.js Public Görsel Yapısı & Test/DB Reset: `docs/2026-08-20_proje_mimarisi_temizligi_ve_nextjs_public_gorsel_yapisi.md`
* Bildirim (Toast) Konumlandırması ve UX Çakışma Düzeltmesi: `docs/2026-08-20_bildirim_konumlandirmasi_ve_ux_cakisma_duzeltmesi.md`
* AI Chatbot "Teşekkür Ederim" Nezaket Kapanışı & Sayfa Filtresi Temizliği: `docs/2026-08-20_chatbot_tesekkur_ve_sayfa_filtresi_temizligi.md`
* AI Satış Danışmanı Kapsamlı Araç Tanıtım & Anlatım Mimarisi: `docs/2026-08-20_ai_danisman_arac_kapsamli_tanitim_ve_anlatim_mimarisi.md`
* Test Sürüşü & Showroom Randevu Mimarisi (test_drives Tablosu & Uçtan Uca Rezervasyon): `docs/2026-08-20_test_surusu_randevu_tablosu_ve_uctan_uca_rezervasyon_mimarisi.md`
* Kasa Tipi Filtreleme, Bağlam Yönetimi & Halüsinasyon Kalkanı: `docs/2026-08-21_kasa_tipi_filtreleme_ve_baglam_yonetimi_guncellemesi.md`
* Customer Leads Araç Bilgisi Senkronizasyonu & Sıfır Bütçe Halüsinasyonu: `docs/2026-08-21_customer_leads_arac_bilgisi_ve_butce_halusinasyon_duzeltmesi.md`

## 5. Güncel Durum ve Sürekli Hafıza Kuralları
* **Mevcut Durum:** 
  - **Customer Leads Araç Bilgisi Senkronizasyonu:** Kullanıcı bir araç için test sürüşü randevusu planladığında veya bir araca odaklandığında (`target_vehicle` / `focused_v`), `customer_leads` tablosundaki `interested_brand`, `interested_model`, `interested_body_type` ve `focused_vehicle_id` alanları eksiksiz ve anlık olarak güncellenir.
  - **Sıfır Bütçe Halüsinasyonu Koruması:** Tarih (`21.08.2026`), saat (`14:00`, `14:00 - 15:00`), telefon numarası (`0532 123 45 67`), kilometre veya beygir gücü gibi ifadelerin yanlışlıkla bütçe (`budget_max`) olarak ayrıştırılması engellenmiştir. Müşteri açıkça bütçe/fiyat belirtmediği sürece `budget_min` ve `budget_max` NULL (None) kalır.
  - **Kasa Tipi ve Doğrudan Filtreleme:** Kullanıcı "Sedan", "SUV", "Hatchback" gibi kasa tipi aradığında doğrudan `body_type` ile eşleştirilir. Kriterdeki araç stokta varsa (örn: Sedan -> Honda City), Çapraz Öneri başlatılmaz; doğrudan stoktaki araç sunulur.
  - **Bağlam Yönetimi & Halüsinasyon Kalkanı:** Kullanıcı açıkça bir model ismi belirtmedikçe asla "incelediğimiz C5 Aircross" veya benzeri uydurma bağlam yaratılmaz. Yeni filtre geldiğinde önceki model odakları sıfırlanır.
  - **Çapraz Öneri Şartları:** Çapraz öneri yalnızca aranan spesifik kriter stokta yoksa yapılır. Şeffaf ve dürüst dil kullanılır; asla "incelediğiniz" denmez.
  - PostgreSQL 17 veritabanına `test_drives` tablosu eklenmiş; `customer_leads` ve `vehicles` tablolarıyla 1-N yabancı anahtar ilişkisi kurulmuştur.
  - Bilişsel AI Satış Danışmanına Türkçe tarih/saat ayrıştırma motoru (`NLUParser.extract_datetime_expression`) ve `APPOINTMENT_REQUEST` / `APPOINTMENT_DATETIME_PROVIDED` niyetleri entegre edilmiştir.
  - **Test Sürüşünde Zorunlu Telefon Kontrolü & Karar Değiştirme:** Sohbetin başında telefon paylaşımı isteğe bağlıdır; ancak test sürüşü planlanacağı zaman aracı rezerve etmek ve danışmanın teyit sağlayabilmesi için telefon numarası **kesinlikle zorunludur**. Müşteri tarih verip ilk başta telefon vermek istemediğinde sistem randevu tarihini hafızada tutar. Müşteri sonradan *"tamam paylaşayım o zaman telefon numaramı"* diyerek karar değiştirdiğinde (`PHONE_AGREEMENT`) bot randevu tarihini hatırlatarak numarasını ister; numara verildiği an `test_drives` tablosuna `CONFIRMED` statüsüyle kaydeder.
  - REST API'ye `GET /api/test-drives` ve `GET /api/leads` uç noktaları eklenmiş; `/api/stats` endpoint'ine `total_test_drives` metriği dahil edilmiştir.
  - AI Satış Danışmanına `VEHICLE_OVERVIEW` intent'i ve `generate_vehicle_executive_presentation` metodu eklenmiştir.
  - AI Chatbot'a `GRATITUDE` intent ve nezaket kapanış akışı eklenmiş ("Teşekkür ederim", "Sağolun" vb. sonrasında robotik selamlama tekrarı engellenmiştir).
  - Test dosyaları `tests/` dizini altında modülerleştirilmiş ve **85 birim/entegrasyon testinin tamamı (%100)** başarıyla koşmaktadır.
  - Next.js 15 prodüksiyon derlemesi (`npm run build` / `frontend/out`) başarıyla tamamlanmıştır.
* **Kural:** Her mimari ve işlevsel güncellemeden sonra `PROJECT_MEMORY.md`, `.antigravity_rules.md`, `.cursorrules.md`, `.github/copilot-instructions.md`, `README.md` ve ilgili `docs/` belgesi eksiksiz güncellenmek zorundadır.
