# Customer Leads Araç Bilgisi Senkronizasyonu ve Sıfır Bütçe Halüsinasyonu Düzeltmesi

**Tarih:** 21 Ağustos 2026  
**Kapsam:** `customer_leads` Tablosu Model/Marka Senkronizasyonu, `extract_budget` Sıfır Halüsinasyon Koruması ve Randevu Entegrasyonu.

---

## 1. Problem Tanımı ve Kullanıcı Geri Bildirimi

1. **`customer_leads` Araç Bilgisinin Eksik Kalması:**
   Kullanıcı bir araç seçip (örn: Peugeot 408 veya Citroën C5 Aircross) test sürüşü randevusu oluşturduğunda, `test_drives` tablosuna kayıt atılmasına rağmen `customer_leads` tablosundaki `interested_brand`, `interested_model` ve `interested_body_type` sütunları boş (`NULL`) kalıyordu.
2. **Bütçe Halüsinasyonu (`budget_max` Kirliliği):**
   Kullanıcı test sürüşü planlarken tarih (*"21.08.2026 - 14:00"*), saat (*"saat 14:00"* / *"14:00 ile 15:00 arası"*) veya telefon numarası (*"0532 111 22 33"*) paylaştığında, `NLUParser.extract_budget` fonksiyonundaki esnek regex eşleşmeleri bu sayıları bütçe olarak yorumluyor ve `lead.budget_max` alanına 53 milyon TL veya 21 milyon TL gibi gerçek dışı değerler yazıyordu.

---

## 2. Çözüm ve Mimari Düzenlemeler

### A. Customer Leads Tablosu Senkronizasyonu
[`backend/agent/chatbot/planner.py`](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/backend/agent/chatbot/planner.py) içerisinde araç odağı veya test sürüşü hedef aracı (`target_vehicle` / `focused_v`) belirlendiği her akışta (tarih sağlama, randevu talebi, telefon paylaşımı, araç genel bakışı):
```python
if target_vehicle:
    state.active_vehicle_id = target_vehicle.id
    lead.focused_vehicle_id = target_vehicle.id
    lead.interested_brand = target_vehicle.brand
    lead.interested_model = target_vehicle.model
    lead.interested_body_type = target_vehicle.body_type
```
bütünlüğü sağlandı. Böylece randevu alan müşterinin `customer_leads` kaydında hangi marka, model ve kasa tipiyle ilgilendiği eksiksiz saklanır.

### B. Bütçe Çıkarımında Sıfır Halüsinasyon (Zero-Hallucination) Koruması
[`backend/agent/chatbot/nlu.py`](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/backend/agent/chatbot/nlu.py) altındaki `extract_budget` metodu güçlendirildi:
1. Bütçe taranmadan önce metindeki telefon numaraları, tarihler (`DD.MM.YYYY`, `DD/MM/YYYY`, `DD-MM-YYYY`), saatler (`HH:MM`, `saat HH:MM`) ve kilometre/motor ifadeleri ayıklandı.
2. Standart rakamların bütçe kabul edilmesi için metinde açıkça para birimi (`TL`, `lira`) veya bütçe anahtar kelimeleri (`bütçe`, `fiyat`, `param`, `limiti`, `nakit`, `kredi`, `tutar`) bulunması şart koşuldu.
3. Müşteri açıkça fiyat/bütçe belirtmediği sürece `budget_min` ve `budget_max` alanları **kesinlikle `None` (NULL)** kalmaktadır.

---

## 3. Test ve Doğrulama

[`tests/test_test_drive_appointments.py`](file:///Users/tufanozkan/Documents/arkas_projects/arkas_2el_pazarlama_ai/tests/test_test_drive_appointments.py) içerisine `test_08_customer_leads_fields_and_no_budget_hallucination_on_test_drive` testi eklendi.

Doğrulanan senaryo:
- `Peugeot 408 için yarın saat 15:00 randevu alabilir miyim numaram 05321112233`
- `TestDrive`: `vehicle.model == "408"`, `status == "CONFIRMED"`, `customer_phone == "05321112233"`.
- `CustomerLead`: `interested_brand == "Peugeot"`, `interested_model == "408"`, `interested_body_type == "SUV"`, `focused_vehicle_id == td.vehicle_id`.
- `budget_min == None`, `budget_max == None` (Sıfır halüsinasyon).

```bash
.venv/bin/python -m unittest discover -s tests -v
----------------------------------------------------------------------
Ran 85 tests in 1.476s

OK (Tüm 85 test %100 başarılı)
```
