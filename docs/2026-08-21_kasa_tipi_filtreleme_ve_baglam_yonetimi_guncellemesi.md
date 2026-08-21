# Kasa Tipi Filtreleme, Bağlam Yönetimi ve Halüsinasyon Kalkanı Güncellemesi

**Tarih:** 21 Ağustos 2026  
**Kapsam:** `backend/agent/chatbot/` (NLU, Planner, Search Engine, Tools), Kasa Tipi (Sedan/SUV/Hatchback) Eşleştirmesi, Çapraz Öneri Şartları, Halüsinasyon Önleyici Bağlam Kalkanı ve Regresyon Testleri.

---

## 1. Problem ve Kullanıcı İhtiyacı

Önceki chatbot akışında iki kritik bağlam ve filtreleme problemi tespit edilmiştir:
1. **Yanlış Çapraz Öneri & Stok Göz Ardı Etme:** Kullanıcı *"sedan araç yok mu?"* veya *"sedan araç var mı?"* diye sorduğunda, veritabanında **Honda City (Sedan)** bulunmasına rağmen önceki oturumdan kalan veya varsayılan aktif araç odağı (örneğin Citroën C5 Aircross - SUV) nedeniyle bot Sedan aracı doğrudan listelemek yerine gereksiz çapraz öneri yapabiliyor veya C5 Aircross hakkında bilgi vermeye çalışıyordu.
2. **Uydurma / Yanıltıcı Bağlam İfadesi ("İncelediğimiz ..."):** Kullanıcı belirli bir modeli açıkça sormamış olsa bile bot yanıtlarında *"İncelediğimiz Citroën C5 Aircross..."* gibi ifadeler kullanarak kullanıcıda sanki o araca bakıyormuş algısı yaratıyordu.

---

## 2. Mimari Kurallar ve Uygulanan Çözüm

### KURAL 1: Kasa Tipi ve Filtreleme (NLU & Search Engine)
* Kullanıcı "Sedan", "SUV", "Hatchback", "Crossover" gibi bir kasa tipi aradığında, bu doğrudan PostgreSQL `vehicles` tablosundaki `body_type` alanı ile eşleştirilir.
* Eğer kullanıcının aradığı kasa tipinde (örneğin **Sedan**) araç stokta varsa (**Honda City**), Çapraz Öneri (Cross-Recommendation) akışı **kesinlikle başlatılmaz**; doğrudan stoktaki araç listelenir.

### KURAL 2: Bağlam Yönetimi ve Halüsinasyon Önleyici Kalkan
* Kullanıcı açıkça bir model ismi belirtmedikçe (Örn: *"C5 Aircross hakkında bilgi ver"*), asla *"incelediğimiz Citroën C5 Aircross"* veya benzeri bir uydurma bağlam yaratılmaz.
* Kullanıcı yeni bir filtre veya soru sorduğunda (*"sedan araç yok mu?"*), `customer_leads` ve oturum hafızasındaki eski model/çapraz öneri odakları sıfırlanır (`state.vehicle_query.model = None`, `state.active_vehicle_id = None`). Yalnızca yeni sorguya odaklanılır.
* `resolve_active_vehicle` fonksiyonundan rastgele/varsayılan ilk araca düşme davranışı kaldırıldı; model belirtilmemişse aktif araç `None` kalır.

### KURAL 3: Çapraz Öneri (Cross-Recommendation) Şartları
* Çapraz öneri **SADECE** aranan spesifik kriter (örn: stokta olmayan bir kasa tipi, bütçe aşımı veya eksik donanım) stokta bulunmadığında yapılır.
* Öneri dili şeffaf ve doğrudan kurgulanmıştır:  
  *"İstediğiniz kriterde Hatchback araç şu anda stoklarımızda bulunmuyor. Ancak filtreleri esnetirseniz portföyümüzdeki alternatif modellerimiz (Citroën C5 Aircross, Peugeot 408, Honda City) mevcuttur."*  
  Asla *"incelediğiniz / incelediğimiz"* denmez.

---

## 3. Kod Değişiklikleri ve Düzeltmeler

1. **`backend/agent/chatbot/tools.py`**:
   - `generate_vehicle_executive_presentation` ve `answer_vehicle_aspects` metotlarındaki tüm *"incelediğimiz"* ifadeleri temizlendi.
2. **`backend/agent/chatbot/search_engine.py`**:
   - `resolve_active_vehicle` metoduna `body_type` önceliği eklendi; varsayılan rastgele C5 Aircross fallback'i kaldırıldı.
3. **`backend/agent/chatbot/planner.py`**:
   - Yeni `body_type` veya `brand` filtresi geldiğinde eski `model` ve `active_vehicle_id` sıfırlandı.
   - `is_explicit_search` tespit mantığı güçlendirilerek *"sedan araç yok mu?"* gibi soruların yanlışlıkla tekil araç detayına sapması engellendi.
   - Arama sonucu boş döndüğünde şeffaf çapraz öneri metni üretildi.

---

## 4. Test ve Kalite Güvencesi

`tests/test_chatbot_suite.py` dosyasına 2 yeni kapsamlı test eklendi:
* **`test_33_sedan_direct_match_no_cross_recommendation`**: Sedan aramasında doğrudan Honda City sunulduğu ve çapraz öneri başlatılmadığı doğrulandı.
* **`test_34_multi_turn_body_type_reset_from_suv_to_sedan`**: C5 Aircross detayından sonra gelen Sedan aramasında eski odağın sıfırlandığı; ardından stokta olmayan Hatchback aramasında şeffaf alternatif sunulduğu doğrulandı.

```bash
.venv/bin/python -m unittest discover -s tests -v
----------------------------------------------------------------------
Ran 84 tests in 1.547s

OK (Tüm 84 test %100 başarılı)
```
