#!/usr/bin/env python3
"""
Arkas 2. El Pazarlama AI - Ana Orkestratör (Main Orchestrator)

Kullanım:
    python main.py                # Scraper -> AI Pazarlama Ajanı -> Web Sunucusu
    python main.py --reset-db     # Veritabanını sıfırlar ve sıfırdan canlı verilerle çalıştırır
    python main.py --scrape-only  # Yalnızca web scraper çalıştırır ve veritabanına kaydeder
    python main.py --generate-only# Yalnızca AI pazarlama brief ve metinlerini üretir
    python main.py --web-only     # Yalnızca Web Vitrin Sunucusunu başlatır
"""

import sys
import shutil
import argparse
import logging
import uvicorn
from config import settings, BASE_DIR, FRONTEND_OUT_DIR
from backend.db.database import SessionLocal, init_db, engine
from backend.db.models import Base, Vehicle, VehicleImage, CreativeBrief, CustomerLead
from backend.scraper.arkas_scraper import ArkasScraper
from backend.agent.marketing_agent import MarketingAgent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("ArkasAI")

def print_banner():
    banner = r"""
  ╔════════════════════════════════════════════════════════════════╗
  ║                 ARKAS 2. EL PAZARLAMA AI                       ║
  ║     Web Scraper • AI Metin Ajanı • Bilişsel AI Asistan & Vitrin║
  ╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def reset_database(db):
    print("\n🧹 Veritabanı sıfırlanıyor...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("      ✓ PostgreSQL tabloları (vehicles, vehicle_images, creative_briefs, customer_leads) başarıyla sıfırlandı.")

def run_scraper(db, limit=settings.MAX_SCRAPE_ITEMS):
    print(f"\n[1/2] 🌐 Web Scraper Çalıştırılıyor ({settings.SCRAPER_BASE_URL})...")
    scraper = ArkasScraper()
    res = scraper.scrape_and_save(db, limit=limit)
    print(f"      ✓ İşlenen: {res['total_processed']} | Yeni: {res['new_added']} | Güncellenen: {res['updated']} | Atlanan (Mükerrer): {res['skipped_duplicate']}")
    return res

def run_marketing_agent(db, limit=settings.MAX_SCRAPE_ITEMS):
    print("\n[2/2] 🤖 AI Pazarlama & Kreatif Metin Ajanı Çalıştırılıyor...")
    agent = MarketingAgent(db)
    count = agent.process_all_pending(limit=limit)
    print(f"      ✓ {count} araç için marka personası, Safe (Dengeli) & Bold (İlgi Çekici) reklam metinleri ve kancalar oluşturuldu.")
    return count

def start_web_server(host=settings.WEB_HOST, port=settings.WEB_PORT):
    ui_type = "Next.js 15 Modern Stüdyo (App Router)" if FRONTEND_OUT_DIR.exists() else "Standart Statik Görsel Vitrini"
    print(f"\n🚀 Web Görsel Vitrini Başlatılıyor: http://localhost:{port}")
    print(f"   ⚡ Arayüz Motoru: {ui_type}")
    print("   (Durdurmak için Ctrl+C tuşlarına basabilirsiniz)\n")
    uvicorn.run("backend.web.server:app", host=host, port=port, reload=True)

def build_frontend():
    import subprocess
    frontend_dir = BASE_DIR / "frontend"
    if frontend_dir.exists():
        print("\n📦 Next.js Frontend derleniyor (`npm run build`)...")
        res = subprocess.run(["npm", "run", "build"], cwd=str(frontend_dir), capture_output=True, text=True)
        if res.returncode == 0:
            print("      ✓ Next.js Frontend başarıyla derlendi ve `frontend/out` klasörüne aktarıldı.")
        else:
            print(f"      ❌ Frontend derleme hatası:\n{res.stderr}")

def main():
    parser = argparse.ArgumentParser(description="Arkas 2. El Pazarlama AI Orchestrator")
    parser.add_argument("--reset-db", action="store_true", help="Tüm veritabanı tablolarını sıfırlar")
    parser.add_argument("--scrape-only", action="store_true", help="Yalnızca scraper çalıştırır")
    parser.add_argument("--generate-only", action="store_true", help="Yalnızca AI reklam metinlerini üretir")
    parser.add_argument("--web-only", action="store_true", help="Yalnızca web sunucusunu başlatır")
    parser.add_argument("--no-web", action="store_true", help="İşlem tamamlandıktan sonra web sunucusunu başlatmadan çıkar")
    parser.add_argument("--build-frontend", action="store_true", help="Next.js arayüzünü derler (npm run build)")
    parser.add_argument("--limit", type=int, default=settings.MAX_SCRAPE_ITEMS, help="İşlenecek maksimum araç sayısı")
    parser.add_argument("--port", type=int, default=settings.WEB_PORT, help="Web sunucu portu")
    parser.add_argument("--host", type=str, default=settings.WEB_HOST, help="Web sunucu hostu")

    args = parser.parse_args()
    print_banner()

    if args.build_frontend:
        build_frontend()
        return

    # Initialize Database Tables
    init_db()
    db = SessionLocal()

    try:
        if args.reset_db:
            reset_database(db)
            run_scraper(db, limit=args.limit)
            run_marketing_agent(db, limit=args.limit)
            if not args.no_web:
                start_web_server(host=args.host, port=args.port)
            else:
                print("\n✨ Veritabanı sıfırlama ve metin üretimi tamamlandı. Çıkış yapılıyor.")
        elif args.scrape_only:
            run_scraper(db, limit=args.limit)
        elif args.generate_only:
            run_marketing_agent(db, limit=args.limit)
        elif args.web_only:
            start_web_server(host=args.host, port=args.port)
        else:
            # Full Pipeline Execution
            run_scraper(db, limit=args.limit)
            run_marketing_agent(db, limit=args.limit)
            if not args.no_web:
                start_web_server(host=args.host, port=args.port)
            else:
                print("\n✨ İşlem tamamlandı. Çıkış yapılıyor.")
    except KeyboardInterrupt:
        print("\n\n👋 Sistem güvenle kapatıldı.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
