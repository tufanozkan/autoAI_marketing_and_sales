# 4 Tablolu Yeni Veritabanı Şeması, Vehicle Images Tablosu & Hafif Kazıma Raporu

**Tarih:** 18 Ağustos 2026  
**Hedef URL:** `https://arkasspoticar.sahibinden.com` (Kurumsal Arkas Spoticar Mağazası)  
**Kapsam:** Veritabanı şemasının yeniden yapılandırılması (`vehicle_images` tablosunun eklenmesi, `marketing_copies` yerine `creative_briefs` içine metinlerin entegre edilmesi), hafif HTTP istekleri ile `div.classified-list` ve detay sayfalarındaki `ul.classifiedDetailThumbList` (image_0, image_1, image_2...) elemanlarından ilk 5 aracın tüm veri ve görselleriyle çekilmesi.  
**Durum:** Başarıyla Tamamlandı, PostgreSQL 17'ye Kaydedildi ve Web Vitrininde Yayına Alındı.  

---

## 🗄️ Yeni 4 Tablolu Veritabanı Mimarisi

1. **`vehicles`**:
   - `id`, `external_id`, `source`, `url`, `brand`, `model`, `package`, `sub_model`, `year`, `km`, `price`, `currency`, `fuel_type`, `transmission`, `body_type`, `color`, `engine_power`, `engine_capacity`, `technical_specs` (JSON), `ad_features` (JSON), `damage_expertise` (JSON), `expertise_note` (Text), `primary_image_url` (Kapak Görseli).
2. **`vehicle_images`** *(Yeni Tablo)*:
   - `id`, `vehicle_id` (FK), `image_url` (Yerel/HD URL), `is_primary` (Boolean), `display_order` (0, 1, 2...), `caption` (Açıklama).
   - Detay sayfasındaki `ul.classifiedDetailThumbList` altındaki tüm fotoğraflar bu tabloda sıralı olarak tutulur.
3. **`creative_briefs`** *(Entegre AI Metin Modeli)*:
   - `id`, `vehicle_id` (FK), `brand_archetype`, `target_persona`, `emotional_points` (JSON), `tone_of_voice`, `key_hooks` (JSON).
   - `balanced_copy`: Dengeli, objektif ve şeffaf metin.
   - `professional_copy`: Kurumsal, filo ve garantili alıcı odaklı metin.
   - `engaging_copy`: İlgi çekici, enerjik ve emojili metin.
   - `story_frames`: 3 sahneli Instagram story akışı.
   - `hashtags`: İlan etiketleri.
4. **`customer_leads`**:
   - `id`, `session_id` (UK), `first_name`, `last_name`, `full_name`, `phone`, `interested_brand`, `interested_model`, `interested_body_type`, `budget_max`, `focused_vehicle_id`, `chat_history` (JSON), `conversation_summary`.

---

## 🚗 Doğrulanan 5 Araç ve Ekspertiz Raporları

1. **2023 Opel Mokka 1.2 T Elegance Otomatik (36.100 KM | 1.380.000 TL)**
   - **Görseller (4 Adet):** `image_0` (Primary) + `image_1`, `image_2`, `image_3` (`VehicleImage` tablosunda).
   - **Ekspertiz:** Hatasız, boyasız ve değişensiz. Tramer: 0 TL.

2. **2023 Renault Megane 1.3 TCe Icon EDC + Sunroof (51.300 KM | 1.680.000 TL)**
   - **Görseller (3 Adet):** `image_0` (Primary) + `image_1`, `image_2` (`VehicleImage` tablosunda).
   - **Ekspertiz:** **Sol Arka Çamurluk (Boyalı)**, Değişen: Yok, Tramer: 3.800 TL.

3. **2023 Fiat Egea Cross 1.6 Multijet Urban DCT (38.000 KM | 1.415.000 TL)**
   - **Görseller (3 Adet):** `image_0` (Primary) + `image_1`, `image_2` (`VehicleImage` tablosunda).
   - **Ekspertiz:** Hatasız, boyasız ve değişensiz. Tramer: 0 TL.

4. **2025 Peugeot 408 1.2 PureTech Allure EAT8 (9.000 KM | 1.895.000 TL)**
   - **Görseller (3 Adet):** `image_0` (Primary) + `image_1`, `image_2` (`VehicleImage` tablosunda).
   - **Ekspertiz:** Yalnızca 9.000 KM'de, fabrikasyon hatasız.

5. **2024 Honda City 1.5 i-VTEC Executive CVT (50.000 KM | 1.365.000 TL)**
   - **Görseller (3 Adet):** `image_0` (Primary) + `image_1`, `image_2` (`VehicleImage` tablosunda).
   - **Ekspertiz:** Hatasız, boyasız ve değişensiz. Tramer: 0 TL.
