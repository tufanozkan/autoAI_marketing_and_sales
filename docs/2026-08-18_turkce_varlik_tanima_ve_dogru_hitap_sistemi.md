# Arkas 2. El Pazarlama AI — Gelişmiş Türkçe İsim & Varlık Tanıma (NER) ve Doğru Hitap Mimarisi

**Tarih:** 18 Ağustos 2026  
**Kapsam:** Türkçe İsim & Soyisim Ayrıştırma, Cinsiyet & Hitap Bilgi Tabanı (Hanım / Bey / Sayın), Telefon Reddetme Niyeti (Negative Phone Intent)  
**Durum:** Tamamlandı, Test Edildi ve Canlıda  

---

## 1. Problem ve Çözüm

### 1.1. Yaşanan Problem
Kullanıcı `"ceren ayruk - telefon numaramı vermek istemiyorum"` yazdığında, eski sistem `"telefon"` kelimesini isim olarak algılayıp *"Merhaba Telefon Bey"* şeklinde hatalı ve profesyonellikten uzak bir yanıt vermekteydi.

### 1.2. Uygulanan Çözüm
1. **Gelişmiş Türkçe Varlık Tanıma (Turkish Named Entity Parser):**
   - Tire (`-`), eğik çizgi (`/`), noktalı virgül (`;`) gibi ayraçlarla gelen girdiler segmentlere ayrıştırılır.
   - Stopword ve eylem filtreleri uygulanarak gerçek isim/soyisim (`Ceren Ayruk`) izole edilir.
2. **Telefon Reddetme Niyeti (Negative Phone Intent):**
   - *"numaramı vermek istemiyorum"*, *"telefon yok"*, *"paylaşmak istemiyorum"* gibi ifadeler özel bir niyet olarak algılanır.
   - Telefon zorlanmaz, *"Telefon paylaşımı tercih edilmedi"* olarak nezaketle kaydedilir.
3. **Akıllı Cinsiyet & Hitap Sözlüğü (Gender & Honorific Mapping):**
   - Kapsamlı Türkçe kadın ve erkek isim tabanı (`FEMALE_NAMES`, `MALE_NAMES`) entegre edildi.
   - `Ceren` ➔ **Ceren Hanım**
   - `Tufan` ➔ **Tufan Bey**
   - Bilinmeyen veya unisex isimler ➔ **Sayın [İsim]**

---

## 2. Doğrulanan Örnek Test Çıktıları

| Girdi | Ayrıştırılan Varlık | Bot Yanıtı |
| :--- | :--- | :--- |
| `ceren ayruk - telefon numaramı vermek istemiyorum` | `first_name: Ceren`, `last_name: Ayruk`, `declined_phone: True` | *"Çok memnun oldum Ceren Hanım (Telefon paylaşımı tercih edilmedi)! Bilgilerinizi güvenle kaydettim."* |
| `Tufan Özkan - 05078958517` | `first_name: Tufan`, `last_name: Özkan`, `phone: 05078958517` | *"Çok memnun oldum Tufan Bey (Telefon: 05078958517)! Bilgilerinizi güvenle kaydettim."* |
| `Ayşe Yılmaz` | `first_name: Ayşe`, `last_name: Yılmaz` | *"Çok memnun oldum Ayşe Hanım! Bilgilerinizi güvenle kaydettim."* |
| `Burak Can Demir / numara vermek istemiyorum` | `first_name: Burak`, `last_name: Can Demir`, `declined_phone: True` | *"Çok memnun oldum Burak Bey (Telefon paylaşımı tercih edilmedi)! Bilgilerinizi güvenle kaydettim."* |
