import os
from typing import Optional, List
from fastapi import FastAPI, Depends, Query, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from config import settings, STATIC_DIR, FRONTEND_OUT_DIR
from src.db.database import get_db, init_db
from src.db.models import Vehicle, CreativeBrief, MarketingCopy, CustomerLead
from src.scraper.arkas_scraper import ArkasScraper
from src.agent.marketing_agent import MarketingAgent
from src.agent.chatbot_agent import ChatbotAgent
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    customer_id: Optional[int] = None
    session_id: Optional[str] = None

app = FastAPI(
    title=settings.APP_NAME,
    version="3.0.0",
    description="Arkas 2. El Pazarlama AI - Web Scraper, AI Metin Ajanı, Bilişsel AI Danışman & Modern Next.js Vitrini"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Next.js _next static assets if exported
if FRONTEND_OUT_DIR.exists() and (FRONTEND_OUT_DIR / "_next").exists():
    app.mount("/_next", StaticFiles(directory=str(FRONTEND_OUT_DIR / "_next")), name="next_static")

# Mount static directory for general assets
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    if FRONTEND_OUT_DIR.exists():
        next_index = FRONTEND_OUT_DIR / "index.html"
        if next_index.exists():
            return FileResponse(str(next_index))
    
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "Arkas 2. El Pazarlama AI Backend Aktif."}

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total_vehicles = db.query(Vehicle).count()
    active_vehicles = db.query(Vehicle).filter(Vehicle.is_active == True).count()
    total_copies = db.query(MarketingCopy).count()
    total_leads = db.query(CustomerLead).count()
    
    brands_count = db.query(Vehicle.brand, func.count(Vehicle.id)).group_by(Vehicle.brand).all()
    brands_stats = [{"brand": b, "count": c} for b, c in brands_count]

    return {
        "total_vehicles": total_vehicles,
        "active_vehicles": active_vehicles,
        "total_copies": total_copies,
        "total_leads": total_leads,
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
                Vehicle.package.ilike(search_term),
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

    data = vehicle.to_dict()
    data["brief"] = brief.to_dict() if brief else None
    data["copies"] = [c.to_dict() for c in copies]
    return data

@app.post("/api/pipeline/run")
def trigger_pipeline(db: Session = Depends(get_db)):
    """Triggers Scraper -> Marketing Agent."""
    scraper = ArkasScraper()
    scrape_res = scraper.scrape_and_save(db, limit=settings.MAX_SCRAPE_ITEMS)

    agent = MarketingAgent(db)
    copies_generated = agent.process_all_pending(limit=settings.MAX_SCRAPE_ITEMS)

    return {
        "status": "success",
        "scrape_stats": {
            "total": scrape_res["total_processed"],
            "new": scrape_res["new_added"],
            "updated": scrape_res["updated"],
            "skipped": scrape_res["skipped_duplicate"]
        },
        "copies_generated": copies_generated
    }

@app.post("/api/chat")
def chat_with_agent(req: ChatRequest, db: Session = Depends(get_db)):
    """
    Cognitive AI Sales Consultant Endpoint.
    """
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Mesaj boş olamaz.")

    agent = ChatbotAgent(db)
    response = agent.process_message(
        message=req.message,
        customer_id=req.customer_id,
        session_id=req.session_id
    )
    return response

@app.get("/api/leads")
def get_leads(db: Session = Depends(get_db)):
    leads = db.query(CustomerLead).order_by(CustomerLead.created_at.desc()).all()
    return [l.to_dict() for l in leads]
