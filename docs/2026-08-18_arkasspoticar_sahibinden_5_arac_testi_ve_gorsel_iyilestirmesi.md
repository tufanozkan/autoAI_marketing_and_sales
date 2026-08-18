# Arkas Spoticar — Doğrudan Mağaza URL'si (`arkasspoticar.sahibinden.com`) 5 Araçlık Test & Görsel İyileştirme Raporu

**Tarih:** 18 Ağustos 2026  
**Hedef URL:** `https://arkasspoticar.sahibinden.com` (Kurumsal Arkas Spoticar Mağazası)  
**Kapsam:** Veritabanının sıfırlanması, doğrudan mağazadaki 5 aracın gerçek KM, gerçek TL fiyatları ve tüm orijinal fotoğraflarıyla kaydedilmesi; görsellerin harici referans kısıtlamalarına karşı `no-referrer` politikasıyla güvenceye alınması; 3-tonlu reklam metinlerinin üretilmesi.  
**Durum:** Başarıyla Tamamlandı, PostgreSQL 17'ye Kaydedildi ve Web Vitrininde Yayına Alındı.  

---

## 🚗 Portföye Eklenen 5 Gerçek Araç

1. **2023 Opel Mokka 1.2 T Elegance Otomatik**
   - **Fiyat:** 1.380.000 TL
   - **KM:** 36.100 KM
   - **Ana Görsel:** Kapak fotoğrafı (Sahibinden CDN)
   - **Fotoğraf Sayısı:** 4 Adet Orijinal İlan Fotoğrafı
   - **Ekspertiz:** Hatasız, boyasız ve değişensiz. 12 Ay Spoticar Garantili.

2. **2023 Renault Megane 1.3 TCe Icon EDC + Sunroof**
   - **Fiyat:** 1.680.000 TL
   - **KM:** 51.300 KM
   - **Fotoğraf Sayısı:** 3 Adet Orijinal İlan Fotoğrafı
   - **Ekspertiz:** Sağ ön çamurluk lokal boyalı (Tramer: 3.800 TL).

3. **2023 Fiat Egea Cross 1.6 Multijet Urban DCT**
   - **Fiyat:** 1.415.000 TL
   - **KM:** 38.000 KM
   - **Fotoğraf Sayısı:** 3 Adet Orijinal İlan Fotoğrafı
   - **Ekspertiz:** Hatasız, boyasız ve değişensiz.

4. **2025 Peugeot 408 1.2 PureTech Allure EAT8**
   - **Fiyat:** 1.895.000 TL
   - **KM:** 9.000 KM
   - **Fotoğraf Sayısı:** 3 Adet Orijinal İlan Fotoğrafı
   - **Ekspertiz:** Yalnızca 9.000 KM'de, fabrikasyon hatasız.

5. **2024 Honda City 1.5 i-VTEC Executive CVT**
   - **Fiyat:** 1.365.000 TL
   - **KM:** 50.000 KM
   - **Fotoğraf Sayısı:** 2 Adet Orijinal İlan Fotoğrafı
   - **Ekspertiz:** Hatasız, boyasız ve değişensiz.

---

## 🖼️ Görsel Açılma & Hotlinking Çözümü

* **Sorun:** Sahibinden CDN görselleri (`i0.shbdn.com`), tarayıcıdan doğrudan çağrıldığında `Referer: localhost:8000` başlığını gördüğünde hotlinking engeli uygulayabiliyordu.
* **Çözüm:**
  - `layout.tsx` içerisine `<meta name="referrer" content="no-referrer" />` global başlığı eklendi.
  - `VehicleCard.tsx` ve `CreativeStudioModal.tsx` bileşenlerindeki tüm `<img>` etiketlerine `referrerPolicy="no-referrer"` ve akıllı `onError` fallback mekanizması eklendi.
  - Artık tüm kapak ve galeri görselleri tarayıcıda doğrudan ve sorunsuz açılmaktadır.
