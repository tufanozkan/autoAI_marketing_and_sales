# Arkas 2. El Pazarlama AI — Görsel Motoru Temizliği & Kapsamlı Araç Şeması Hazırlığı

**Tarih:** 18 Ağustos 2026  
**Kapsam:** Sentetik Afiş Motorunun (`PosterEngine`) Kaldırılması, Orijinal İlan Galerisi Entegrasyonu, Kapsamlı Araç Veritabanı Şeması (`technical_specs`, `ad_features`, `damage_expertise`), Safe & Bold Metin Motorunun Korunması  
**Durum:** Tamamlandı, Veritabanı Temizlendi ve Yeni Veri Kaynağı İçin Hazır  

---

## 1. Mimari Değişiklikler ve Temizlik

1. **Sentetik Görsel / Afiş Motorunun Kaldırılması:**
   - `src/agent/poster_engine.py` silindi.
   - `static/generated_posters/` dizini temizlendi.
   - `posters` tablosu PostgreSQL'den kaldırıldı (`DROP TABLE IF EXISTS posters CASCADE`).
   - Sistem artık sentetik afiş üretmek yerine yeni veri kaynağından gelen **yüksek kaliteli orijinal ilan fotoğraflarını** doğrudan sergileyecek şekilde uyarlandı.

2. **Kapsamlı Yeni Araç Şeması (`Vehicle` Modeli):**
   - `package`: Donanım Paketi (örn: Elite, Plus Dark, Style, Titanium).
   - `technical_specs`: JSON formatında motor gücü, tork, yakıt tüketimi, hızlanma, çekiş sistemi ve bagaj hacmi gibi tüm teknik veriler.
   - `ad_features`: JSON formatında ilan detaylarında bulunan konfor, güvenlik, iç ve dış donanım listesi.
   - `damage_expertise`: JSON formatında boyalı parçalar, değişen parçalar ve tramer hasar kaydı.
   - `expertise_note`: Arkas 2. El güvence ve ekspertiz özeti.
   - `image_urls` & `primary_image_url`: Orijinal araç fotoğrafları listesi.

3. **Pazarlama Metin & Kreatif Motorunun Korunması (`MarketingAgent`):**
   - **Safe (Dengeli / Profesyonel):** Güven, garanti ve kurumsal değerleri öne çıkaran reklam metinleri.
   - **Bold (İlgi Çekici / Cesur):** Tutku, prestij, macera ve duygusal kancaları öne çıkaran reklam metinleri.
   - **Story Akışı:** 3 sahneli Instagram Story video/metin konseptleri.

4. **Frontend & Vitrin Stüdyosu Güncellemesi:**
   - `VehicleCard.tsx` ve `CreativeStudioModal.tsx` bileşenleri orijinal araç galerisiyle, sekmeli teknik özellikler, ekspertiz durumu ve donanım paneliyle yenilendi.
   - `npm run build` ile Next.js export'u başarıyla alındı.

---

## 2. PostgreSQL Tablo Yapısı (Güncel)

| Tablo Adı | Açıklama |
| :--- | :--- |
| `vehicles` | Detaylı araç kimliği, paket, motor/şanzıman, teknik özellikler JSON, donanımlar JSON, hasar/ekspertiz JSON, orijinal fotoğraf URL'leri. |
| `customer_leads` | Tekil `session_id` bazlı müşteri ad-soyad, telefon, ilgilenilen marka/kasa, bütçe, tam sohbet dökümü ve AI sohbet özeti. |
| `creative_briefs` | Marka arketipi, hedef persona, duygusal satış noktaları ve kancalar. |
| `marketing_copies` | Safe (Dengeli) ve Bold (İlgi Çekici) reklam metinleri, kancalar, CTA'lar ve hashtagler. |
