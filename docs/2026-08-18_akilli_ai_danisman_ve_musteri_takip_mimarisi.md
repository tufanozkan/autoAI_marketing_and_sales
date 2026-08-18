# Arkas 2. El Pazarlama AI — Akıllı AI Danışman & Müşteri Takip (Lead Generation) Mimarisi

**Tarih:** 18 Ağustos 2026  
**Kapsam:** Chatbot Asistanı (`ChatbotAgent`), Çift Katmanlı Bilgi Motoru (DB + Web), Sayfa Filtreleme Aksiyonları, Müşteri Lead Tablosu (`CustomerLead`)  
**Durum:** Tamamlandı & Canlı Test Edildi  

---

## 1. Müşteri & Lead Yönetim Modeli (`CustomerLead`)
PostgreSQL 17 veritabanına `customer_leads` tablosu eklendi:
- `id`, `first_name`, `last_name`, `full_name`, `phone`
- `interested_brand`, `interested_model`, `interested_body_type`, `budget_max`
- `chat_history`: JSON formatında tam soru-cevap kronolojisi
- `conversation_summary`: Showroom ve satış ekibinin müşterinin talebini tek bakışta görebileceği AI özeti (örn: *"Müşteri: Tufan Özkan | Tel: 05321112233 | Marka: Skoda | Kasa: SUV | Bütçe: 1.500.000 TL | Önerilen: KAMIQ"*).

---

## 2. Çift Katmanlı Bilgi Motoru & Sayfa Kontrol Ajanı (`ChatbotAgent`)
1. **Müşteri Karşılama:** Bot açıldığında kullanıcıyı sıcak bir dille karşılar; ad, soyad ve yeni araç bildirimleri için telefon numarası ister.
2. **PostgreSQL DB Arama:** Bütçe, marka, kasa tipi veya donanım filtreleriyle stoktaki araçları listeler.
3. **Dinamik Sayfa Kontrolü (`filter_action`):** Chatbot kullanıcının talebine göre (`1.5M altı SUV bakıyorum` vb.) ana sayfadaki vitrini eş zamanlı olarak filtreler.
4. **Canlı Otomotiv Bilgi Ağı:** Veritabanında olmayan genel/teknik sorularda (yakıt tüketimi, kronik arıza analizi, fabrika verileri):
   > *"ℹ️ Bu teknik bilgiyi yerel stok veritabanımızda yer almadığı için güncel otomotiv ağından derleyerek sizinle paylaşıyorum:"*
   özel bilgilendirme kancasıyla yanıt verir.

---

## 3. Frontend: Yüzen Minimalist AI Bot Arayüzü (`ChatbotWidget`)
- Sağ altta mat antrasit & şampanya altın nefes alan hover mikro-animasyonlu yuvarlak tetikleyici.
- Genişletilebilir lüks sohbet penceresi, hızlı soru butonları, anlık filtre senkronizasyonu ve sohbet sıfırlama seçeneği.
