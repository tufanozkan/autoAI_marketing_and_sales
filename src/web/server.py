import os
from typing import Optional, List
from fastapi import FastAPI, Depends, Query, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from config import settings, STATIC_DIR, POSTERS_DIR
from src.db.database import get_db, init_db
from src.db.models import Vehicle, Poster, CreativeBrief, MarketingCopy
from src.scraper.arkas_scraper import ArkasScraper
from src.agent.marketing_agent import MarketingAgent
from src.agent.poster_engine import PosterEngine

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Arkas 2. El Pazarlama AI - Web Scraper, Afiş Motoru & Görsel Vitrini"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory for images, CSS, JS
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "Arkas 2. El Pazarlama AI Backend Aktif. static/index.html bulunamadı."}

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total_vehicles = db.query(Vehicle).count()
    active_vehicles = db.query(Vehicle).filter(Vehicle.is_active == True).count()
    total_posters = db.query(Poster).count()
    total_copies = db.query(MarketingCopy).count()
    
    brands_count = db.query(Vehicle.brand, func.count(Vehicle.id)).group_by(Vehicle.brand).all()
    brands_stats = [{"brand": b, "count": c} for b, c in brands_count]

    return {
        "total_vehicles": total_vehicles,
        "active_vehicles": active_vehicles,
        "total_posters": total_posters,
        "total_copies": total_copies,
        "brands": brands_stats
    }

@app.get("/api/brands")
def get_brands(db: Session = Depends(get_db)):
    brands = db.query(Vehicle.brand).distinct().order_by(Vehicle.brand).all()
    return [b[0] for b in brands if b[0]]

@app.get("/api/vehicles")
def get_vehicles(
    brand: Optional[str] = Query(None),
    body_type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Vehicle).filter(Vehicle.is_active == True)

    if brand and brand != "all":
        query = query.filter(Vehicle.brand.ilike(f"%{brand}%"))
    if body_type and body_type != "all":
        query = query.filter(Vehicle.body_type.ilike(f"%{body_type}%"))
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Vehicle.brand.ilike(search_term),
                Vehicle.model.ilike(search_term),
                Vehicle.sub_model.ilike(search_term),
                Vehicle.color.ilike(search_term)
            )
        )
    if min_price is not None:
        query = query.filter(Vehicle.price >= min_price)
    if max_price is not None:
        query = query.filter(Vehicle.price <= max_price)

    vehicles = query.order_by(Vehicle.price.desc()).all()
    return [v.to_dict() for v in vehicles]

@app.get("/api/vehicles/{vehicle_id}")
def get_vehicle_detail(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Araç bulunamadı.")
    
    brief = db.query(CreativeBrief).filter(CreativeBrief.vehicle_id == vehicle_id).first()
    copies = db.query(MarketingCopy).filter(MarketingCopy.vehicle_id == vehicle_id).all()
    posters = db.query(Poster).filter(Poster.vehicle_id == vehicle_id).all()

    data = vehicle.to_dict()
    data["brief"] = brief.to_dict() if brief else None
    data["copies"] = [c.to_dict() for c in copies]
    data["posters"] = [p.to_dict() for p in posters]
    return data

@app.post("/api/pipeline/run")
def trigger_pipeline(db: Session = Depends(get_db)):
    """Triggers the full pipeline: Scraper -> Marketing Agent -> Poster Engine."""
    # 1. Scrape
    scraper = ArkasScraper()
    scrape_res = scraper.scrape_and_save(db, limit=settings.MAX_SCRAPE_ITEMS)

    # 2. Marketing Agent
    agent = MarketingAgent(db)
    copies_generated = agent.process_all_pending(limit=settings.MAX_SCRAPE_ITEMS)

    # 3. Poster Engine
    poster_engine = PosterEngine(db)
    posters_rendered = poster_engine.render_all_pending(limit=settings.MAX_SCRAPE_ITEMS)

    return {
        "status": "success",
        "scrape_stats": {
            "total": scrape_res["total_processed"],
            "new": scrape_res["new_added"],
            "updated": scrape_res["updated"],
            "skipped": scrape_res["skipped_duplicate"]
        },
        "copies_generated": copies_generated,
        "posters_rendered": posters_rendered
    }

@app.post("/api/pipeline/generate-single/{vehicle_id}")
def generate_single_creative(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Araç bulunamadı.")
    
    # Run Agent
    agent = MarketingAgent(db)
    agent_res = agent.process_vehicle(vehicle)

    # Run Poster Engine
    poster_engine = PosterEngine(db)
    posters = poster_engine.generate_all_posters_for_vehicle(vehicle)

    return {
        "status": "success",
        "vehicle_id": vehicle_id,
        "brief": agent_res["brief"],
        "copies_count": len(agent_res["copies"]),
        "posters": [p.to_dict() for p in posters]
    }
