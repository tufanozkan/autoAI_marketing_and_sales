# Arkas 2. El Pazarlama AI — Bilişsel AI Satış Danışmanı & Dinamik Araç Öneri Mimarisi

**Tarih:** 18 Ağustos 2026  
**Kapsam:** Bilişsel Niyet Analizi (Intent Engine), Dinamik Araç Değiştirme & Çapraz Donanım Arama, Bütçe Esnetme, Tekil Oturum Takibi (`session_id`)  
**Durum:** Tamamlandı, Test Edildi ve Canlıda  

---

## 1. Mimari Genel Bakış ve Çözülen Problemler

Önceki chatbot versiyonunda yaşanan kalıp yanıt verme, tek bir araçta takılı kalma ve mükerrer veritabanı kaydı açma sorunları, **Bilişsel Niyet Analiz Motoru (Cognitive Intent Engine)** ile tamamen çözülmüştür.

```
                                [Kullanıcı Mesajı]
                                        │
                                        ▼
                           [Bilişsel Niyet Ayrıştırıcı]
                                        │
    ┌───────────────────┬───────────────┴───────────────┬───────────────────┐
    ▼                   ▼                               ▼                   ▼
[1. Bütçe Güncelleme]  [2. Donanım/Araç Önerisi]   [3. Doğrudan Soru]  [4. Stok Filtreleme]
("5M kadar çıkart")     ("direksiyon ısıtmalı öner") ("otomatik mi, km") ("1.5M altı SUV")
    │                   │                               │                   │
    ▼                   ▼                               ▼                   ▼
[Bütçeyi Yükselt &     [Portföyü Tara &                [Odaktaki Araçtan   [DB Sorgula &
 Tüm Araçları Kıyasla]  Volvo XC40'a Geç / Odak Değiştir] Net Cevap Ver]    Sayfayı Filtrele]
    │                   │                               │                   │
    └───────────────────┴───────────────┬───────────────┴───────────────────┘
                                        │
                                        ▼
                    [Müşteri Lead & Sohbet Özeti Güncellemesi]
                    (PostgreSQL: `customer_leads` Tekil Kayıt)
```

---

## 2. Bilişsel Niyet Sınıflandırma (Intent Classification)

### 2.1. Donanım Odaklı Çapraz Öneri Niyeti (`is_recommendation_request`)
* **Kullanıcı İfadesi:** *"O zaman direksiyon ısıtması olan bir araç önerir misin bana?"* / *"Direksiyon ısıtma olan araç yok mu sayfanızda?"*
* **Çalışma Mantığı:**
  1. Odaktaki araçta (örn: Skoda Kamiq) bu donanım yoksa takılı kalmaz.
  2. Tüm Arkas 2. El portföyünü tarar.
  3. Kış paketine sahip **Volvo XC40 Plus Dark** modelini tespit eder.
  4. Odak aracını (`focused_vehicle_id`) Volvo olarak günceller.
  5. Sayfadaki filtreyi eş zamanlı olarak Volvo'ya çeker ve kullanıcıya donanım detaylarını açıklar.

### 2.2. Bütçe Esnetme Niyeti (`is_budget_update`)
* **Kullanıcı İfadesi:** *"Fiyat aralığını 5m kadar çıkart"* / *"Bütçemi 5 milyona yükselt"*
* **Çalışma Mantığı:**
  1. `"fiyat"` kelimesini mevcut aracın liste fiyatı olarak yorumlamaz; bütçe artırımı olduğunu anlar.
  2. Müşterinin bütçesini `5.000.000 TL` olarak günceller.
  3. Portföydeki tüm uygun araçları (Volvo XC40, Skoda Kamiq, Ford Transit, Courier, Ranger) donanım farklarıyla listeler.
  4. Sayfa filtre aksiyonunu (`max_price: 5000000`) tetikler.

### 2.3. Doğrudan Araç Detayı Yanıtları (`_answer_vehicle_specific_question`)
* **Şanzıman:** *"Evet Tufan Bey, 2023 model Skoda Kamiq aracımız 7 ileri çift kavramalı DSG Otomatik şanzımana sahiptir."*
* **Kilometre:** *"İncelediğimiz Skoda Kamiq aracımız yalnızca 2.021 KM'dedir. Sıfır kondisyonundadır."*
* **Koltuk/Direksiyon Isıtma:** *"İncelediğimiz Skoda Kamiq Elite paketinde koltuk/direksiyon ısıtma bulunmamaktadır (bu donanımlar üst paket olan Premium veya kış paketinde yer alır). Ancak çift bölgeli dijital klima, 8 inç multimedya ve LED farlar standarttır."*
* **Ekspertiz:** *"Aracımız Arkas 2. El 100+ nokta ekspertiz ve kilometre garantilidir. Tüm kontrolleri yetkili servis standartlarında yapılmıştır."*

---

## 3. Tekil Oturum ve DB Tekilleştirme (`session_id`)
* Frontend (`ChatbotWidget.tsx`) `sessionStorage` üzerinde benzersiz bir `session_id` (`session_177140...`) tutar.
* Backend `get_or_create_customer` metodu bu ID üzerinden aynı oturumu bulur.
* Sohbette 10 mesaj yazılsa dahi veritabanında **tek bir satır** açılır ve `chat_history`, `conversation_summary`, `budget_max`, `focused_vehicle_id` alanları sürekli güncel tutulur.

---

## 4. Örnek Doğrulanmış Diyalog Akışı

| Adım | Kullanıcı Mesajı | AI Yanıtı & Sistem Aksiyonu |
| :--- | :--- | :--- |
| **1** | *"Tufan Özkan - 05078958517"* | Müşteri adını ve telefonunu `customer_leads` tablosuna kaydeder, *"Çok memnun oldum Tufan Bey!"* diyerek karşılar. |
| **2** | *"Aslında daha çok 1.5m altı suv bakıyorum"* | Sayfayı `body_type: SUV, max_price: 1.5M` olarak filtreler ve Skoda Kamiq'i önerir. |
| **3** | *"Skoda Kamiq km ve vites"* | 7 İleri DSG Otomatik vites detayını açıklar. |
| **4** | *"kaç kmde araç"* | 2.021 KM olduğunu ve garanti durumunu belirtir. |
| **5** | *"peki direksiyon ısıtma var mı?"* | Elite pakette olmadığını, hangi donanımların standart olduğunu listeler. |
| **6** | *"o zaman direksiyon ısıtması olan bir araç önerir misin bana?"* | **Dinamik Odak Değişimi:** Portföyü tarayıp **Volvo XC40 Plus Dark** modelini öne çıkarır, sayfayı Volvo'ya filtreler. |
| **7** | *"fiyat aralığını 5m kadar çıkart"* | Bütçeyi 5M TL'ye çeker, portföydeki tüm araçları donanım ayrıcalıklarıyla sunar. |
| **8** | *"direksiyon ısıtma olan araç yok mu? sayfanızda"* | Kış paketli Volvo XC40 modelini teyit eder ve ekspertiz/finansman detayına davet eder. |
