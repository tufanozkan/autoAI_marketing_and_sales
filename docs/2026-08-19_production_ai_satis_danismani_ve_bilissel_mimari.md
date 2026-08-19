# Production AI Satış Danışmanı & Bilişsel Mimari Raporu

**Tarih:** 19 Ağustos 2026  
**Kapsam:** Arkas 2. El / Arkas Spoticar AI Satış Danışmanı Chatbot Çekirdeğinin Baştan Sona Yeniden Tasarımı, Modüler Bilişsel Mimari Kurulumu, PostgreSQL 17 Veritabanı Şeması Genişletmesi, Gelişmiş Türkçe NLU/NER Motoru ve Uçtan Uca Entegrasyon.

---

## 1. Yönetici Özeti ve Mimari Vizyon

Mevcut monolitik `ChatbotAgent` yapısındaki kırılgan `if/elif` ve regex mantığı, çok adımlı konuşmalarda bağlam kaybı, Türkçe isim ve olumsuzlama (negation) ayrıştırma hataları, hayal ürünü veri riskleri ve frontend ile senkronize olmayan filtreleme sorunları tespit edilmiş ve **tamamen modüler, bilişsel (cognitive) ve production-grade** bir mimariyle baştan inşa edilmiştir.

### Temel Prensipler & Başarılan Hedefler
1. **Sıfır Halüsinasyon Prensibi (Zero-Hallucination):** Araç fiyatları, kilometreleri, şanzıman ve motor tipleri ile donanım paketleri asla yapay zeka tarafından tahmin edilmez veya uydurulmaz. PostgreSQL 17 veritabanı tek ve mutlak gerçeklik kaynağıdır (Single Source of Truth).
2. **Gelişmiş Türkçe Doğal Dil Anlama (NLU/NER):** 
   - 1000'den fazla Türkçe erkek, kadın ve unisex isim sözlüğü.
   - İsim olmayan günlük/otomotiv kelimelerinin ("telefonumu", "vermiyorum", "istemiyorum", "aracınızın", "suv" vb.) müşteri adı olarak algılanmasını önleyen negatif kara liste (Negative Blacklist).
   - "Ceren ben ama telefon numaramı vermiyorum" gibi karmaşık cümlelerde hem ismi ("Ceren") hem de telefon paylaşmama niyetini (`phone_declined=True`) aynı anda ayrıştırabilme.
   - Çift cinsiyetli (unisex: Deniz, Derya, Ege, Özgür, Görkem vb.) isimlerde cinsiyet varsayımı yapmadan kullanıcıya tercih sorma ("Deniz Bey mi, Deniz Hanım mı?") ve verilen tercihi oturum boyunca hafızada koruma.
3. **Gelişmiş Türkçe Bütçe & Olumsuzlama Motoru:**
   - "1.5m üstü SUV" ifadesini alt sınır (`min_price=1.500.000 TL`), "1.5 milyon altı" ifadesini üst sınır (`max_price=1.500.000 TL`) olarak algılama.
   - "1.2 - 1.8 milyon", "1 milyon 500 bin TL", "1.500.000 TL", "2m", "800 bin" gibi tüm yaygın formatları eksiksiz dönüştürme.
   - "Dizel olmasın", "manuel istemiyorum", "cam tavan olmasın" gibi olumsuzlama (negation) ifadelerini tespit edip arama kriterlerinden çıkarma veya tersine çevirme.
4. **Çoklu Niyet (Multi-Intent) & Çok Açılı Soru-Cevap:**
   - "Peugeot 408 kilometresi ve vitesi nedir?" gibi soruları tek bir yanıtta hem km hem şanzıman detaylarıyla eksiksiz yanıtlama.
   - Aktif incelenen aracı bağlamda tutarak (Context Persistence) devam sorularında ("Cam tavan var mı?", "Bagajı kaç litre?") doğru araca referans verme.
5. **Çapraz Model & Donanım Önerisi (Cross-Recommendation):**
   - İncelenen araçta istenen donanım yoksa (örn. Honda City'de cam tavan), portföydeki cam tavanlı alternatifleri (Citroën C5 Aircross) önerme ve "Öyle yapalım" onayında vitrini otomatik filtreleme.
6. **Sıfır Araç / Yeni Araç Ayrımı & Güvenlik:**
   - "Yeni araç istiyorum", "Sıfır araç göster" isteklerinde kullanılmış araçları sıfırmış gibi sunmak yerine gerçek 0 KM stok kontrolü yapma ve portföyde sıfır araç yoksa dürüstçe bilgilendirip 12 ay garantili 2. el alternatiflerini sunma.

---

## 2. Mimari Yapı & Yeni Dizin Düzeni

Monolitik 950 satırlık kod, `backend/agent/chatbot/` altında sorumlulukların net ayrıldığı 5 ana modüle bölünmüştür:

```
backend/
├── agent/
│   ├── chatbot_agent.py             # Geriye dönük uyumluluk ve ana facade
│   └── chatbot/
│       ├── __init__.py              # Modüler paket dışa aktarımları
│       ├── state.py                 # Pydantic tabanlı durum modelleri (State, Criteria, Offer)
│       ├── nlu.py                   # Türkçe NER, NLU, Bütçe, Negation, Intent ayrıştırıcı
│       ├── search_engine.py         # Parametrik PostgreSQL & JSONB donanım sorgulayıcı
│       ├── tools.py                 # Soru-cevap araçları, SSS, donanım & çapraz öneri araçları
│       ├── planner.py               # Bilişsel niyet planlayıcı ve yanıt orkestratörü
│       └── agent.py                 # ChatbotAgent sınıfı
├── db/
│   ├── models.py                    # CustomerLead şeması (phone_declined, budget_min, vb.)
│   └── database.py                  # Otomatik veritabanı şema migrasyonu
└── web/
    └── server.py                    # Zenginleştirilmiş /api/vehicles, /api/leads, /api/chat
```

---

## 3. Veritabanı Şeması Değişiklikleri

`CustomerLead` tablosuna aşağıdaki sütunlar eklenmiş ve `backend/db/database.py` içinde otomatik `ALTER TABLE ADD COLUMN IF NOT EXISTS` migrasyonu devreye alınmıştır:

| Sütun | Tip | Açıklama |
|---|---|---|
| `phone_declined` | `Boolean` | Müşterinin telefon paylaşmayı reddettiğini takip eder (Tekrar sormayı engeller) |
| `honorific_preference` | `String(20)` | Unisex isimler için müşterinin hitap tercihi (`BEY`, `HANIM`, `SAYIN`) |
| `budget_min` | `Float` | Müşterinin belirttiği alt bütçe sınırı (örn: 1.5M TL üstü) |
| `budget_max` | `Float` | Müşterinin belirttiği üst bütçe sınırı (örn: 2.0M TL altı) |
| `active_filters` | `JSONB / JSON` | Vitrine uygulanan aktif filtre sözlüğü |
| `conversation_state_json` | `JSONB / JSON` | Pydantic `ConversationState` nesnesinin oturumlar arası kalıcılığı |

---

## 4. Frontend & Backend Filtreleme Entegrasyonu

AI Satış Danışmanı bir filtreleme uyguladığında (`filter_action`), Next.js vitrinine aşağıdaki zengin sözleşme aktarılmaktadır:

```typescript
export interface FilterAction {
  brand?: string;
  model?: string;
  body_type?: string;
  min_price?: number | null;
  max_price?: number | null;
  min_km?: number | null;
  max_km?: number | null;
  fuel_type?: string;
  transmission?: string;
  features?: string[];
  is_new?: boolean;
  search?: string;
}
```

Next.js `page.tsx` bileşeni `handleApplyFilterFromAI` ile bu parametreleri yakalar ve `/api/vehicles` endpoint'i üzerinden vitrini anında dinamik olarak günceller.

---

## 5. Root Cause Hata Analizi ve Düzeltmeleri

### Bug #1: Yanlış İsim & Hatalı Hitap ("Telefonumu Bey")
* **Kök Neden (Root Cause):** 
  1. Önceki NLU motorunda "ben X" veya "X ben" kalıbı yakalandığında, X token'ının gerçek bir Türkçe isim olup olmadığı sözlük düzeyinde (`is_valid_turkish_name`) doğrulanmıyordu. "Telefonumu vermek istemiyorum" cümlesinde "telefonumu" token'ı veya telefon ret ifadeleri maskelenmediğinde isim adayı olarak seçilebiliyordu.
  2. Hitap çözümleme (`resolve_honorific`) fonksiyonunda isim bulunamadığında veya bilinmeyen bir ad olduğunda, sistem "Bey" varsayımına düşebiliyordu.
* **Uygulanan Çözüm (Fix):**
  1. İki aşamalı doğrulama (Two-pass NER): İsim adayı yalnızca `ALL_TURKISH_NAMES` (1000+ isim) sözlüğünde mevcutsa kabul edilir. Bilinmeyen kelimeler asla isim olarak kabul edilmez.
  2. Telefon ret ifadeleri ("telefonumu vermek istemiyorum", "numara vermicem" vb.) isim ayrıştırma öncesi maskelenir.
  3. Kesin kural: İsim yoksa veya bilinmiyorsa hitap ASLA "BEY" veya "HANIM" olamaz (`honorific = None`, `get_salutation() = "Değerli Müşterimiz"`).

### Bug #2: Bütçe Aralık Filtrelemesi ("1.5m ile 2m arası")
* **Kök Neden (Root Cause):**
  1. Bütçe aralık regex'i `r"(\d+(?:[.,]\d+)?)\s*(?:-|ile)\s*(\d+(?:[.,]\d+)?)\s*(?:milyon|m\b)"` ilk sayının sonundaki `m` veya `milyon` birimini (örn: `1.5m`) kapsayamadığı için aralık eşleşmesi başarısız oluyordu.
  2. Aralık eşleşmeyince tekil sayı eşleştiriciye düşüyor ve "1.5m" değerini yakalayıp `max_price = 1.500.000 TL` olarak atıyordu.
  3. Ayrıca `"1.5m'den fazla"` ifadesindeki `"den fazla"` tamlaması, `"en fazla"` kelimesiyle alt dize çakışması (substring collision) yaşayarak yanlışlıkla üst sınır (`is_max`) olarak algılanıyordu.
* **Uygulanan Çözüm (Fix):**
  1. Zengin birim ve format destekli `extract_budget` parser'ı geliştirildi: `1.5m ile 2m`, `1.5 milyon ile 2 milyon`, `1.500.000 - 2.000.000`, `1.5M-2M`, `1.5 ile 2 milyon`, `1 milyon 500 bin ile 2 milyon` formatlarının tamamı `min_price = 1.500.000 TL, max_price = 2.000.000 TL` olarak doğru ayrıştırılmaktadır.
  2. Sınır belirleme belirteçleri tam sözcük sınırları (`\b...\b`) ile izole edildi.
  3. Planner criteria merge mantığında yeni bütçe geldiğinde eski çelişen sınırlar temizlenerek overwrite edilmesi sağlandı.

---

## 6. Test ve Doğrulama Sonuçları

Sistem iki kapsamlı test paketi ile doğrulanmıştır:
1. `tests_chatbot.py`: 19 temel regresyon testi.
2. `tests_chatbot_suite.py`: 34 adet detaylı unit ve regresyon testi + çok turlu gerçek müşteri konuşma simülasyonu.

### Test Özeti
```bash
.venv/bin/python -m unittest tests_chatbot.py tests_chatbot_suite.py
----------------------------------------------------------------------
Ran 53 tests in 0.769s

OK
```

### Frontend Derleme Doğrulaması
```bash
npm run build
----------------------------------------------------------------------
✓ Compiled successfully
✓ Generating static pages (5/5)
✓ Exporting (3/3)
```

---

## 7. Sonuç

Arkas 2. El / Arkas Spoticar AI Satış Danışmanı; Türkçe konuşma dilini en ince detayına kadar anlayan, müşteri tercihlerini ve bağlamını asla unutmayan, PostgreSQL 17 envanteri ile %100 senkronize ve güvenilir, production seviyesinde kurumsal bir bilişsel mimariye kavuşturulmuştur.
