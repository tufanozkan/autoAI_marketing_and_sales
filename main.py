#!/usr/bin/env python3
"""
Arkas 2. El Pazarlama AI - Ana Orkestratör (Main Orchestrator)

Kullanım:
    python main.py                # Scraper -> AI Pazarlama Ajanı -> Çoklu Açı Afiş Motoru -> Web Sunucusu
    python main.py --reset-db     # Veritabanını sıfırlar ve sıfırdan canlı verilerle çalıştırır
    python main.py --scrape-only  # Yalnızca web scraper çalıştırır ve veritabanına kaydeder
    python main.py --generate-only# Yalnızca AI pazarlama brief/metin ve afişlerini üretir
    python main.py --web-only     # Yalnızca Web Vitrin Sunucusunu başlatır
"""

import sys
import shutil
import argparse
import logging
import uvicorn
from config import settings, POSTERS_DIR
from src.db.database import SessionLocal, init_db, engine
from src.db.models import Base, Vehicle, CreativeBrief, MarketingCopy, Poster
from src.scraper.arkas_scraper import ArkasScraper
from src.agent.marketing_agent import MarketingAgent
from src.agent.poster_engine import PosterEngine

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
  ║       Web Scraper • AI Kreatif Ajanı • Afiş Motoru & Vitrin    ║
  ╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def reset_database(db):
    print("\n🧹 Veritabanı ve eski afişler sıfırlanıyor...")
    # Drop all and recreate
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Clean generated posters directory
    if POSTERS_DIR.exists():
        for f in POSTERS_DIR.glob("*.png"):
            try:
                f.unlink()
            except Exception:
                pass
    print("      ✓ PostgreSQL tabloları ve afiş deposu başarıyla sıfırlandı.")

def run_scraper(db, limit=settings.MAX_SCRAPE_ITEMS):
    print(f"\n[1/3] 🌐 Web Scraper Çalıştırılıyor ({settings.SCRAPER_BASE_URL})...")
    scraper = ArkasScraper()
    res = scraper.scrape_and_save(db, limit=limit)
    print(f"      ✓ İşlenen: {res['total_processed']} | Yeni: {res['new_added']} | Güncellenen: {res['updated']} | Atlanan (Mükerrer): {res['skipped_duplicate']}")
    return res

def run_marketing_agent(db, limit=settings.MAX_SCRAPE_ITEMS):
    print("\n[2/3] 🤖 AI Pazarlama & Kreatif Sub-Agent Çalıştırılıyor...")
    agent = MarketingAgent(db)
    count = agent.process_all_pending(limit=limit)
    print(f"      ✓ {count} araç için marka personası, Safe/Bold reklam metinleri ve kancalar oluşturuldu.")
    return count

def run_poster_engine(db, limit=settings.MAX_SCRAPE_ITEMS):
    print("\n[3/3] 🎨 Yüksek Çözünürlüklü Çoklu Açı Afiş & Banner Motoru Çalıştırılıyor...")
    poster_engine = PosterEngine(db)
    count = poster_engine.render_all_pending(limit=limit)
    print(f"      ✓ {count} araç için 5'er farklı açı afişi (Ön, Far Detay, Arka Profil, İç Mekan, Banner) başarıyla üretildi.")
    return count

def start_web_server(host=settings.WEB_HOST, port=settings.WEB_PORT):
    print(f"\n🚀 Web Görsel Vitrini Başlatılıyor: http://localhost:{port}")
    print("   (Durdurmak için Ctrl+C tuşlarına basabilirsiniz)\n")
    uvicorn.run("src.web.server:app", host=host, port=port, reload=False)

def main():
    parser = argparse.ArgumentParser(description="Arkas 2. El Pazarlama AI Orchestrator")
    parser.add_argument("--reset-db", action="store_true", help="Tüm veritabanı tablolarını ve afişleri sıfırlar")
    parser.add_argument("--scrape-only", action="store_true", help="Yalnızca scraper çalıştırır")
    parser.add_argument("--generate-only", action="store_true", help="Yalnızca AI metin ve afiş üretir")
    parser.add_argument("--web-only", action="store_true", help="Yalnızca web sunucusunu başlatır")
    parser.add_argument("--limit", type=int, default=settings.MAX_SCRAPE_ITEMS, help="İşlenecek maksimum araç sayısı")
    parser.add_argument("--port", type=int, default=settings.WEB_PORT, help="Web sunucu portu")
    parser.add_argument("--host", type=str, default=settings.WEB_HOST, help="Web sunucu hostu")

    args = parser.parse_args()
    print_banner()

    # Initialize Database Tables
    init_db()
    db = SessionLocal()

    try:
        if args.reset_db:
            reset_database(db)
            run_scraper(db, limit=args.limit)
            run_marketing_agent(db, limit=args.limit)
            run_poster_engine(db, limit=args.limit)
            start_web_server(host=args.host, port=args.port)
        elif args.scrape_only:
            run_scraper(db, limit=args.limit)
        elif args.generate_only:
            run_marketing_agent(db, limit=args.limit)
            run_poster_engine(db, limit=args.limit)
        elif args.web_only:
            start_web_server(host=args.host, port=args.port)
        else:
            # Full Pipeline Execution
            run_scraper(db, limit=args.limit)
            run_marketing_agent(db, limit=args.limit)
            run_poster_engine(db, limit=args.limit)
            start_web_server(host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("\n\n👋 Sistem güvenle kapatıldı.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
