# 2026-08-20: AI Satış Danışmanı Kapsamlı Araç Tanıtım, Anlatım & Bilişsel Bilgi Aktarımı Mimarisi

**Tarih:** 2026-08-20  
**Yazar:** Antigravity AI  
**Kapsam:** AI Satış Danışmanının kullanıcı belirli bir araç hakkında bilgi istediğinde (*"Peugeot 3008 hakkında bilgi alabilir miyim"*, *"bilgi almak istiyorum işte detaylı anlatır mısın bana"*, *"bu aracı anlatır mısın"*, *"Citroën C5 Aircross detayları"*) sadece tek satırlık ilan listelemek ya da karşılama mesajına düşmek yerine; gerçek bir üst düzey otomotiv danışmanı gibi aracın tüm donanım, performans, ekspertiz ve Arkas Spoticar güvencelerini kapsamlı ve yapılandırılmış bir şekilde sunması.

---

## 1. Tespit Edilen Problem ve Kök Neden Analizi

* **Problem 1 (Tek Satırlık Arama Tekrarı):**
  - Kullanıcı *"Peugeot 3008 hakkında bilgi alabilir miyim"* dediğinde, NLU sadece marka ve modeli algılayıp `VEHICLE_SEARCH` olarak sınıflandırıyordu.
  - Chatbot aracı tanıtmak yerine sanki kullanıcı ilk defa arama yapmış gibi tek satırlık liste formatında yanıt veriyor ve *"Araçların detaylarını doğrudan bana sorabilirsiniz"* diyerek kullanıcının zaten sorduğu soruyu yanıtsız bırakıyordu.

* **Problem 2 (Takip Sorusunda Hafıza Kaybı ve Karşılama Sıfırlaması):**
  - Kullanıcı *"bilgi almak istiyorum işte detaylı anlatır mısın bana"* diye devam ettiğinde, sorguda doğrudan marka/model adı geçmediği için NLU intent'i boş kalıyor ve bot fallback karşılama dalına düşerek *"Merhaba Ceylan Hanım! Size nasıl yardımcı olabilirim? Arkas Spoticar portföyümüzdeki araçlarımızın donanım, ekspertiz..."* diyordu.

---

## 2. Geliştirilen Mimari ve Çözümler

### A. NLU ve Intent Seviyesinde Araç Tanıtım / Bilgi Algılama (`VEHICLE_OVERVIEW`)
* [`backend/agent/chatbot/nlu.py`](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/backend/agent/chatbot/nlu.py):
  - `extract_question_aspects` metoduna `"overview"` boyutu eklendi.
  - *"bilgi alabilir miyim"*, *"detaylı anlatır mısın"*, *"hakkında bilgi"*, *"aracı anlat"*, *"özellikleri neler"*, *"tanıtır mısın"*, *"nasıl bir araç"* kalıpları analiz edilerek `VEHICLE_OVERVIEW` ve `VEHICLE_DETAIL` intentleri üretildi.

### B. Danışman Düzeyinde Kapsamlı Araç Sunumu Metodu
* [`backend/agent/chatbot/tools.py`](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/backend/agent/chatbot/tools.py):
  - `ChatbotTools.generate_vehicle_executive_presentation(vehicle, salutation, db)` metodu eklendi:
    1. **Fiyat, KM, Motor, Vites, Tüketim, Bagaj**
    2. **Öne Çıkan Konfor, Güvenlik ve Multimedya Donanımları**
    3. **Ekspertiz Durumu (Boya, Değişen, Tramer 0 TL)**
    4. **Arkas Spoticar 100+ Nokta Kontrolü ve 12 Ay Garanti Güvencesi**
    5. **Test Sürüşü & Takas / Kredi Teklif Çağrısı (CTA)**

### C. Bilişsel Intent Planner Yönlendirmesi
* [`backend/agent/chatbot/planner.py`](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/backend/agent/chatbot/planner.py):
  - `is_asking_info` mantığı entegre edildi. Kullanıcı bilgi istediğinde sorgu arama filtresi olarak değil, doğrudan odaklanılan aktif araç (`focused_v` / `state.active_vehicle_id`) üzerinden detaylı tanıtım olarak cevaplanır.

---

## 3. Test ve Doğrulama

* [`tests/test_vehicle_overview_consultant_flow.py`](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/tests/test_vehicle_overview_consultant_flow.py) yazılarak kullanıcının ilettiği tam akış uçtan uca test edildi.
* Tüm test suite'i başarıyla çalıştırıldı (**75 / 75 OK**).
* Next.js 15 prodüksiyon derlemesi (`npm run build` -> `frontend/out`) hatasız tamamlandı.
