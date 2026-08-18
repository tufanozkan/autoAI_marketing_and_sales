# Spoticar.com.tr Arkas İzmir — 5 Açılı Orijinal Galeri & Şeffaf İlan Entegrasyonu

**Tarih:** 18 Ağustos 2026  
**Hedef URL:** `https://www.spoticar.com.tr/ikinci-el-araclar` (Arkas Gaziemir `CT1449T001` & Arkas Karşıyaka `CT1444T001`)  
**Kapsam:** Sahibinden'den alınan doğrulanmış teknik/ekspertiz verilerinin, Spoticar.com.tr portalındaki Arkas bayilerine ait Amazon S3 / Stellantis CDN üzerinde barındırılan **5 açılı orijinal showroom fotoğraflarıyla** eşleştirilmesi ve `vehicle_images` tablosuna kaydedilmesi.  
**Durum:** Başarıyla Tamamlandı, PostgreSQL 17'ye Yazıldı ve Web Vitrininde Yayına Alındı.  

---

## 📸 Spoticar.com.tr'den Çekilen 5 Açılı Orijinal Fotoğraf Standartları

Her araç için 5 farklı açı eksiksiz olarak `VehicleImage` tablosuna kaydedilmiştir:
1. **Açı 1 (`image_0` - Primary):** Ön 3/4 Dış Görünüm (Kapak Fotoğrafı)
2. **Açı 2 (`image_1`):** Arka 3/4 Dış Görünüm
3. **Açı 3 (`image_2`):** İç Mekan & Ön Konsol Görünümü
4. **Açı 4 (`image_3`):** Yan Profil & Koltuk / Döşeme Kondisyonu
5. **Açı 5 (`image_4`):** Kokpit, Direksiyon & Multimedya Ekranı

---

## 🚗 Portföye Eklenen 5 Gerçek Arkas Spoticar Aracı

| # | Marka / Model / Paket | Gerçek KM | Satış Fiyatı | 5 Açılı Orijinal Görseller | Ekspertiz ve Garanti |
|:---|:---|:---:|:---:|:---:|:---|
| **1** | **2025 Citroën C4 X** 1.2 PureTech 130 HP EAT8 MAX | **43.050 KM** | **1.599.900 TL** | 5 Adet Spoticar HD Showroom Fotoğrafı | Hatasız, Boyasız (Tramer: 0 TL) • Garanti PLUS 12 Ay |
| **2** | **2022 Citroën C3** 1.2 PureTech 110 HP EAT6 Shine | **77.650 KM** | **1.120.000 TL** | 5 Adet Spoticar HD Showroom Fotoğrafı | Hatasız, Boyasız (Tramer: 0 TL) • Garanti PLUS 12 Ay |
| **3** | **2024 Fiat Egea** 1.4 Fire Easy Plus | **93.575 KM** | **799.900 TL** | 5 Adet Spoticar HD Showroom Fotoğrafı | Hatasız, Boyasız (Tramer: 0 TL) • Garanti CLASSIC 6 Ay |
| **4** | **2023 Citroën C5 Aircross** 1.5 BlueHDi 130 HP Shine EAT8 | **42.500 KM** | **1.975.000 TL** | 5 Adet Spoticar HD Showroom Fotoğrafı | Hatasız, Boyasız (Tramer: 0 TL) • Garanti PLUS 12 Ay |
| **5** | **2025 Opel Combo** 1.5 D 130 HP Ultimate AT8 | **19.700 KM** | **1.529.900 TL** | 5 Adet Spoticar HD Showroom Fotoğrafı | 19.700 KM, Hatasız, Boyasız • Garanti PLUS 12 Ay |

---

## 🛠️ Neden Bu Yöntem %100 Başarılı Oldu?
* `spoticar.com.tr` üzerindeki görseller doğrudan **Amazon S3 CDN** (`s3.eu-central-1.amazonaws.com/uvpictures-eu-central-1/...`) üzerinde barındırılmaktadır.
* Sahibinden'in uyguladığı dinamik görsel korumaları/engelleri yerine, Spoticar'ın resmi bayi fotoğrafları doğrudan erişilebilir ve her açı için net 5 ayrı fotoğraf sunmaktadır.
* Görseller yerel diske de indirilerek sıfır gecikmeyle web vitrininde gösterilmektedir.
