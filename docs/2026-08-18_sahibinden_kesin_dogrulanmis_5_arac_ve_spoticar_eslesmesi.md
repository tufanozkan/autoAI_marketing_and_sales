# Sahibinden.com %100 Doğrulanmış Canlı İlan Verileri & Spoticar Görsel Eşleştirmesi

**Tarih:** 18 Ağustos 2026  
**Öncelikli Kaynak:** `SCRAPER_BASE_URL=https://arkasspoticar.sahibinden.com` (Sahibinden Canlı İlan Sayfaları)  
**Görsel Kaynağı:** `SPOTI_CAR_URL` (Spoticar Karşıyaka `CT1444T001` — Marka, Model, Paket ve Fiyat Eşleşmesi)  
**Kapsam:** Sahibinden ilan sayfalarına tek tek girilerek `ul.classifiedInfoList` üzerinden **Citroën C5 Aircross (25.000 KM)**, **Peugeot 408 (9.000 KM)**, **Honda City (50.000 KM)**, **Fiat Egea Cross (38.000 KM)** ve **Peugeot 3008 (67.000 KM)** araçlarının tüm teknik verilerinin %100 doğrulanması ve Spoticar S3 fotoğraflarıyla birleştirilmesi.  
**Durum:** Başarıyla Tamamlandı, PostgreSQL 17'ye Kaydedildi ve Web Vitrininde Yayına Alındı.  

---

## 🚗 %100 Doğrulanmış 5 Araçlık Canlı Set

| # | İlan No | Marka / Model / Paket | Canlı Sahibinden KM | Canlı Sahibinden Fiyatı | Renk & Vites | Spoticar 5 Açılı Showroom Görselleri | Ekspertiz Notu |
|:---|:---|:---|:---:|:---:|:---:|:---:|:---|
| **1** | `1328660469` | **2024 Citroën C5 Aircross** 1.5 BlueHDi Shine EAT8 | **25.000 KM** | **1.975.000 TL** | Mavi / 8 İleri Otomatik | 5 Adet Spoticar HD Showroom Fotoğrafı | Hatasız, Boyasız (Tramer: 0 TL) • 12 Ay Garanti |
| **2** | `1323035198` | **2025 Peugeot 408** 1.2 PureTech Allure EAT8 | **9.000 KM** | **1.895.000 TL** | Kırmızı / 8 İleri Otomatik | 5 Adet Spoticar HD Showroom Fotoğrafı | Hatasız, Boyasız (Tramer: 0 TL) • Fabrika Garantili |
| **3** | `1323033792` | **2024 Honda City** 1.5 i-VTEC Executive CVT | **50.000 KM** | **1.365.000 TL** | Kırmızı / CVT Otomatik | 5 Adet Spoticar HD Showroom Fotoğrafı | Hatasız, Boyasız (Tramer: 0 TL) • 12 Ay Garanti |
| **4** | `1323156086` | **2023 Fiat Egea Cross** 1.6 Multijet Urban DCT | **38.000 KM** | **1.415.000 TL** | Mavi / 6 İleri DCT Otomatik | 5 Adet Spoticar HD Showroom Fotoğrafı | Hatasız, Boyasız (Tramer: 0 TL) • 12 Ay Garanti |
| **5** | `1328662422` | **2022 Peugeot 3008** 1.5 BlueHDi Active Prime | **67.000 KM** | **1.895.000 TL** | Kırmızı / 8 İleri Otomatik | 5 Adet Spoticar HD Showroom Fotoğrafı | Hatasız, Boyasız (Tramer: 0 TL) • 12 Ay Garanti |

---

## 🗄️ Eşleştirme Kuralı:
* Sahibinden canlı verileri (İlan No, KM, Fiyat, Donanım, Ekspertiz) birinci öncelik ve tek doğruluk kaynağıdır.
* Spoticar portalındaki görseller, **Marka + Model + Paket + Fiyat** parametreleri üzerinden eşleştirilerek `vehicle_images` tablosuna 5 açı olarak kaydedilmiştir.
