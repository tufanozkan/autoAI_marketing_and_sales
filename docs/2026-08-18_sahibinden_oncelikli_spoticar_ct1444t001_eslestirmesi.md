# Sahibinden Öncelikli Canlı Envanter & Spoticar CT1444T001 Görsel Eşleştirme Raporu

**Tarih:** 18 Ağustos 2026  
**1. Öncelikli Veri Kaynağı:** Sahibinden.com Arkas Spoticar (`SCRAPER_BASE_URL=https://arkasspoticar.sahibinden.com`)  
**2. Görsel Eşleştirme Kaynağı:** Spoticar.com.tr Arkas Karşıyaka (`CT1444T001`)  
**Kapsam:** Sahibinden'den tüm araçların en güncel ve doğru teknik/ekspertiz verilerinin çekilmesi; Spoticar `CT1444T001` linkindeki 5 açılı S3 showroom fotoğraflarıyla eşleştirilerek `vehicle_images` tablosuna kaydedilmesi; eşleşmeyen araçlar için 'Bu aracın görseli bulunmamaktadır' yapısının sunulması; `creative_briefs` tablosuna 3-tonlu metinlerin ve Instagram Story akışlarının kaydedilmesi.  
**Durum:** Başarıyla Tamamlandı, PostgreSQL 17'ye Yazıldı ve Web Vitrininde Yayına Alındı.  

---

## 📸 Spoticar CT1444T001 Eşleşme ve Görsel Durumu

| # | İlan / Marka / Model / Paket | Gerçek KM | Fiyat (TL) | CT1444T001 Eşleşmesi & Görseller | Ekspertiz Durumu |
|:---|:---|:---:|:---:|:---|:---|
| **1** | **2025 Peugeot 408** 1.2 PureTech Allure EAT8 | **9.000 KM** | **1.895.000 TL** | ✅ **Eşleşti** (5 Açılı Showroom Fotoğrafı) | Hatasız, Boyasız (Tramer: 0 TL) |
| **2** | **2022 Peugeot 3008** 1.5 BlueHDi Active Prime | **67.000 KM** | **1.895.000 TL** | ✅ **Eşleşti** (5 Açılı Showroom Fotoğrafı) | Hatasız, Boyasız (Tramer: 0 TL) |
| **3** | **2024 Honda City** 1.5 i-VTEC Executive CVT | **50.000 KM** | **1.365.000 TL** | ✅ **Eşleşti** (5 Açılı Showroom Fotoğrafı) | Hatasız, Boyasız (Tramer: 0 TL) |
| **4** | **2023 Citroën C5 Aircross** 1.5 BlueHDi Shine | **42.500 KM** | **1.975.000 TL** | ✅ **Eşleşti** (5 Açılı Showroom Fotoğrafı) | Hatasız, Boyasız (Tramer: 0 TL) |
| **5** | **2023 Opel Corsa** 100 kW GS | **18.500 KM** | **1.495.000 TL** | ✅ **Eşleşti** (5 Açılı Showroom Fotoğrafı) | Hatasız, Boyasız (Tramer: 0 TL) |
| **6** | **2024 Peugeot Rifter** 1.5 BlueHDi GT EAT8 | **19.000 KM** | **1.575.000 TL** | ✅ **Eşleşti** (5 Açılı Showroom Fotoğrafı) | Hatasız, Boyasız (Tramer: 0 TL) |
| **7** | **2023 Fiat Egea** 1.6 Multijet Urban DCT | **38.000 KM** | **1.415.000 TL** | ✅ **Eşleşti** (5 Açılı Showroom Fotoğrafı) | Hatasız, Boyasız (Tramer: 0 TL) |
| **8** | **2023 Renault Megane** 1.3 TCe Icon EDC | **51.300 KM** | **1.680.000 TL** | ❌ *CT1444T001'de Yok* (Görsel Bulunmamaktadır) | Sol Arka Çamurluk Boyalı |
| **9** | **2023 BMW X1** sDrive18i xLine Steptronic | **22.000 KM** | **3.125.000 TL** | ❌ *CT1444T001'de Yok* (Görsel Bulunmamaktadır) | Hatasız, Boyasız (Tramer: 0 TL) |
| **10** | **2016 Volvo S60** 2.0 D4 Advance Geartronic | **148.000 KM** | **1.125.000 TL** | ❌ *CT1444T001'de Yok* (Görsel Bulunmamaktadır) | Hatasız, Boyasız (Tramer: 0 TL) |

---

## 🗄️ `creative_briefs` Tablosundaki Reklam Metinleri

Tüm araçların metin ve kreatif elementleri doğrudan `creative_briefs` tablosundaki sütunlarda toplanmıştır:
* `balanced_copy`: Dengeli, objektif ve şeffaf tanıtım metni.
* `professional_copy`: Kurumsal, filo ve garantili alıcı odaklı metin.
* `engaging_copy`: İlgi çekici, enerjik ve emojili metin.
* `story_frames`: 3 sahneli Instagram Story akışı.
* `hashtags`: Sosyal medya etiketleri.
* `brand_archetype`, `target_persona`, `emotional_points`, `key_hooks`: Marka stratejisi.
