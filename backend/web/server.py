import os
from typing import Optional, List
from fastapi import FastAPI, Depends, Query, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from config import settings, FRONTEND_OUT_DIR, VEHICLE_IMAGES_DIR, FRONTEND_PUBLIC_DIR
from backend.db.database import get_db, init_db
from backend.db.models import Vehicle, VehicleImage, CreativeBrief, CustomerLead, TestDrive
from backend.scraper.arkas_scraper import ArkasScraper
from backend.agent.marketing_agent import MarketingAgent
from backend.agent.chatbot_agent import ChatbotAgent
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    customer_id: Optional[int] = None
    session_id: Optional[str] = None

class ResetChatRequest(BaseModel):
    customer_id: Optional[int] = None
    session_id: Optional[str] = None

app = FastAPI(
    title=settings.APP_NAME,
    version="3.0.0",
    description="AutoAI Showroom - Web Scraper, AI Marketing Agent, Cognitive AI Consultant & Modern Next.js Vitrin"
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

# Mount vehicle images directory from frontend/public/vehicle_images
if VEHICLE_IMAGES_DIR.exists():
    app.mount("/vehicle_images", StaticFiles(directory=str(VEHICLE_IMAGES_DIR)), name="vehicle_images")

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    if FRONTEND_OUT_DIR.exists():
        next_index = FRONTEND_OUT_DIR / "index.html"
        if next_index.exists():
            return FileResponse(str(next_index))
    return {"message": "AutoAI Showroom Backend Aktif. Next.js arayüzü için: python main.py --build-frontend"}

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total_vehicles = db.query(Vehicle).count()
    active_vehicles = db.query(Vehicle).filter(Vehicle.is_active == True).count()
    total_briefs = db.query(CreativeBrief).count()
    total_images = db.query(VehicleImage).count()
    total_leads = db.query(CustomerLead).count()
    total_test_drives = db.query(TestDrive).count()
    
    brands_count = db.query(Vehicle.brand, func.count(Vehicle.id)).group_by(Vehicle.brand).all()
    brands_stats = [{"brand": b, "count": c} for b, c in brands_count]

    return {
        "total_vehicles": total_vehicles,
        "active_vehicles": active_vehicles,
        "total_briefs": total_briefs,
        "total_images": total_images,
        "total_leads": total_leads,
        "total_test_drives": total_test_drives,
        "brands": brands_stats
    }

@app.get("/api/brands")
def get_brands(db: Session = Depends(get_db)):
    brands = db.query(Vehicle.brand).distinct().order_by(Vehicle.brand).all()
    return [b[0] for b in brands if b[0]]

@app.get("/api/vehicles")
def get_vehicles(
    brand: Optional[str] = None,
    model: Optional[str] = None,
    body_type: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_km: Optional[int] = None,
    max_km: Optional[int] = None,
    fuel_type: Optional[str] = None,
    transmission: Optional[str] = None,
    feature: Optional[str] = None,
    is_new: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Vehicle).filter(Vehicle.is_active == True)

    if brand and brand != "all":
        query = query.filter(Vehicle.brand.ilike(f"%{brand}%"))
    if model:
        query = query.filter(Vehicle.model.ilike(f"%{model}%"))
    if body_type and body_type != "all":
        if body_type.upper() == "SUV":
            query = query.filter(
                or_(
                    Vehicle.body_type.ilike("%SUV%"),
                    Vehicle.body_type.ilike("%Crossover%"),
                    Vehicle.model.ilike("%Cross%"),
                    Vehicle.model.ilike("%3008%"),
                    Vehicle.model.ilike("%C5%"),
                    Vehicle.model.ilike("%408%")
                )
            )
        else:
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
    if min_km is not None:
        query = query.filter(Vehicle.km >= min_km)
    if max_km is not None:
        query = query.filter(Vehicle.km <= max_km)
    if fuel_type:
        query = query.filter(Vehicle.fuel_type.ilike(f"%{fuel_type}%"))
    if transmission:
        if transmission.lower() == "automatic":
            query = query.filter(or_(
                Vehicle.transmission.ilike("%otomatik%"),
                Vehicle.transmission.ilike("%eat8%"),
                Vehicle.transmission.ilike("%cvt%"),
                Vehicle.transmission.ilike("%dct%")
            ))
        elif transmission.lower() == "manual":
            query = query.filter(Vehicle.transmission.ilike("%manuel%"))
    if is_new:
        query = query.filter(Vehicle.km == 0)

    vehicles = query.order_by(Vehicle.price.desc()).all()

    if feature:
        feat_norm = feature.lower()
        filtered = []
        for v in vehicles:
            ad_feat = v.ad_features or {}
            flat = []
            for items in ad_feat.values():
                if isinstance(items, list): flat.extend(items)
                elif isinstance(items, str): flat.append(items)
            if any(feat_norm in f.lower() for f in flat):
                filtered.append(v)
        return [v.to_dict() for v in filtered]

    return [v.to_dict() for v in vehicles]

@app.get("/api/leads")
def get_leads(db: Session = Depends(get_db)):
    leads = db.query(CustomerLead).order_by(CustomerLead.updated_at.desc()).all()
    return [l.to_dict() for l in leads]

@app.get("/api/vehicles/{vehicle_id}")
def get_vehicle_detail(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Araç bulunamadı.")
    
    return vehicle.to_dict()

@app.post("/api/pipeline/run")
def trigger_pipeline(db: Session = Depends(get_db)):
    """Triggers Scraper -> Marketing Agent."""
    scraper = ArkasScraper()
    scrape_res = scraper.scrape_and_save(db, limit=settings.MAX_SCRAPE_ITEMS)

    agent = MarketingAgent(db)
    briefs_generated = agent.process_all_pending(limit=settings.MAX_SCRAPE_ITEMS)

    return {
        "status": "success",
        "scrape_stats": scrape_res,
        "briefs_generated": briefs_generated
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

@app.post("/api/chat/reset")
def reset_chat(req: ResetChatRequest, db: Session = Depends(get_db)):
    """
    Explicit Conversation & Vehicle Filter Reset Endpoint.
    """
    agent = ChatbotAgent(db)
    response = agent.reset_session(
        customer_id=req.customer_id,
        session_id=req.session_id
    )
    return response

@app.get("/api/test-drives")
def get_test_drives(
    customer_id: Optional[int] = None,
    session_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all test drive appointments or filter by customer/session.
    """
    query = db.query(TestDrive).order_by(TestDrive.created_at.desc())
    if customer_id:
        query = query.filter(TestDrive.customer_lead_id == customer_id)
    elif session_id:
        lead = db.query(CustomerLead).filter(CustomerLead.session_id == session_id).first()
        if lead:
            query = query.filter(TestDrive.customer_lead_id == lead.id)
        else:
            return []

    results = query.all()
    return [td.to_dict() for td in results]

@app.get("/api/leads")
def get_customer_leads(limit: int = 50, db: Session = Depends(get_db)):
    """
    List customer CRM leads with their test drives and conversation summary.
    """
    leads = db.query(CustomerLead).order_by(CustomerLead.updated_at.desc()).limit(limit).all()
    return [lead.to_dict() for lead in leads]

