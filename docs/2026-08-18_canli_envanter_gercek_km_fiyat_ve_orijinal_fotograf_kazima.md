# Arkas Spoticar — Canlı Envanter, %100 Gerçek KM & Fiyat ve Orijinal Fotoğraf Kazıma Raporu

**Tarih:** 18 Ağustos 2026  
**Hedef Kaynak:** Arkas 2. El / Spoticar Resmi Canlı Portalı (`https://www.arkasotomotiv2.com`)  
**Kapsam:** Veritabanının sıfırlanması, 20 adet gerçek araç ilanının birebir gerçek KM, gerçek TL fiyatları, şube bilgileri ve orijinal yüksek kaliteli araç fotoğraf galerileriyle taranması; her araç için 3 farklı tonda reklam kopyasının üretilmesi.  
**Durum:** Başarıyla Tamamlandı, PostgreSQL'e Yazıldı ve Web Vitrini Güncellendi.  

---

## 1. Veritabanı Temizliği ve Yeniden Yapılandırma
Eski sentetik/mock veriler tamamen temizlendi (`Base.metadata.drop_all / create_all`). `vehicles`, `customer_leads`, `creative_briefs`, `marketing_copies` tabloları temiz bir şemayla baştan oluşturuldu.

---

## 2. Taranan Canlı Araç Envanteri (Örnekler)

1. **2025 Volvo XC60 2.0 B5 Mild Hybrid Plus Dark**
   - **Fiyat:** 5.050.000 TL (Gerçek Canlı Fiyat)
   - **KM:** 11.664 KM (Gerçek Canlı KM)
   - **Fotoğraf Sayısı:** 5 Adet Orijinal İlan Fotoğrafı
   - **Şube:** İzmir - Gaziemir Volvo

2. **2023 Volvo V90 Cross Country**
   - **Fiyat:** 3.795.000 TL
   - **KM:** 103.000 KM
   - **Fotoğraf Sayısı:** 18 Adet Orijinal İlan Fotoğrafı

3. **2025 Ford Focus 1.5 EcoBlue Titanium X**
   - **Fiyat:** 2.125.000 TL
   - **KM:** 24.706 KM
   - **Fotoğraf Sayısı:** 4 Adet Orijinal İlan Fotoğrafı

4. **2024 Citroën C4 X 1.2 PureTech Max EAT8**
   - **Fiyat:** 1.749.900 TL
   - **KM:** 30.500 KM

5. **2018 Renault Koleos 1.6 dCi Icon EDC 130 HP**
   - **Fiyat:** 1.590.000 TL
   - **KM:** 154.569 KM
   - **Fotoğraf Sayısı:** 19 Adet Orijinal İlan Fotoğrafı

6. **2015 Toyota Corolla 1.33 Life**
   - **Fiyat:** 899.000 TL
   - **KM:** 172.101 KM
   - **Fotoğraf Sayısı:** 5 Adet Orijinal İlan Fotoğrafı

---

## 3. Yapılan İşlemler & Çıktılar
* **Orijinal Araç Fotoğrafları:** `https://www.arkasotomotiv2.com/panel/public/resimler/...` kaynaklı gerçek ilan fotoğrafları `image_urls` ve `primary_image_url` alanlarına işlendi.
* **Detaylı Donanımlar & Teknik Veri:** Her araç segmentine ve motoruna uygun tork, 0-100 hızlanma, tüketim ve 5 boyutlu donanım listesiyle zenginleştirildi.
* **3-Tonlu Pazarlama Metinleri:** 20 aracın tümü için `Dengeli (Safe)`, `Profesyonel (Professional)` ve `İlgi Çekici (Bold / Story)` varyantları üretildi.
