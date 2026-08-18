# Arkas 2. El Pazarlama AI — Next.js 15 Modern Vitrin & Stüdyo Dönüşümü

**Tarih:** 18 Ağustos 2026  
**Kapsam:** Frontend Mimarisi, Tasarım Sistemi, Next.js 15 App Router & API Entegrasyonu  
**Durum:** Tamamlandı & Production-Ready  

---

## 1. Mimari Genel Bakış
Mevcut statik HTML/CSS/JS vitrini; **Next.js 15 (React 19, TypeScript, Tailwind CSS v4, Lucide React)** altyapısına taşınarak minimalist, yenilikçi ve lüks otomotiv ajansı standartlarına kavuşturulmuştur.

Tüm frontend kod tabanı kök dizini kirletmeden `frontend/` klasörü altında izole edilmiştir.

### Dizin Yapısı:
- `frontend/src/app/`:
  - `page.tsx`: Ana vitrin, arama/filtreleme çubuğu, araç listeleme ve istatistik kartları.
  - `layout.tsx`: Plus Jakarta Sans tipografisi, meta etiketleri ve sıcak lüks tema.
  - `globals.css`: Sıcak mimari keten bej (`#F7F5F0`), saf alabaster beyaz (`#FFFFFF`), fırçalanmış gümüş/taş gri (`#E6E2D8`), şampanya altın (`#C2A676`) ve derin kömür/antrasit (`#18181B`) quiet luxury renk sistemi.
- `frontend/src/components/`:
  - `layout/Navbar.tsx`: Marka başlığı, ⌘K hızlı arama kısayolu, yenileme ve pipeline tetikleyici.
  - `showcase/StatsSection.tsx`: Canlı veritabanı KPI sayaçları.
  - `showcase/FilterToolbar.tsx`: Anlık arama, Kasa tipi filtresi, Marka hapları ve Izgara/Kompakt liste görünüm seçici.
  - `showcase/VehicleCard.tsx`: Kart üzerinden doğrudan 5 farklı açıyı önizleme (hover/tık), hızlı afiş indirme ve stüdyoya yönlendirme.
  - `studio/CreativeStudioModal.tsx`: Yüksek çözünürlüklü 5 açılı afiş görsel motoru (Ön, Far, Arka, Kokpit, 16:9 Banner) ve çok kanallı AI reklam metin laboratuvarı (Safe, Bold, Story).
  - `studio/PipelineProgressModal.tsx`: Scraper ve afiş üretim sürecini adım adım canlı gösteren modal.
  - `ui/ToastNotification.tsx`: Minimalist kopyalama/indirme/hata bildirim kutusu.

---

## 2. API & FastAPI Entegrasyonu
- **Proxy / Rewrites:** `frontend/next.config.ts` aracılığıyla geliştirme (`npm run dev`) sırasında `/api/*` ve `/static/*` istekleri `http://127.0.0.1:8000` adresine yönlendirilir.
- **Statik Export (`output: 'export'`):** `npm run build` ile `frontend/out` klasörüne statik HTML/JS/CSS çıktısı üretilir.
- **FastAPI Entegrasyonu:** `src/web/server.py` FastAPI sunucusu, `frontend/out` klasörü mevcut olduğunda modern Next.js uygulamasını doğrudan `http://localhost:8000` adresinde servis eder.

---

## 3. Çalıştırma Komutları

```bash
# 1. Tek Komutla Her Şeyi Başlatma (FastAPI + Next.js Vitrini):
python main.py

# 2. Frontend'i Tekrar Derlemek İçin:
python main.py --build-frontend
# veya
cd frontend && npm run build

# 3. Next.js Geliştirme Sunucusu (Hot Reload):
cd frontend && npm run dev
```
