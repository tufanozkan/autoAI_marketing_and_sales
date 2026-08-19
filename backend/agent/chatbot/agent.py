import logging
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from backend.db.models import CustomerLead, Vehicle
from .planner import ResponsePlanner
from .nlu import NLUParser
from .search_engine import VehicleSearchEngine
from .tools import ChatbotTools

logger = logging.getLogger(__name__)

class ChatbotAgent:
    """
    Arkas Spoticar Bilişsel AI Satış Danışmanı & Otomotiv Asistanı:
    - Türkçe Varlık Tanıma (NER: Hanım/Bey/Unisex/Sayın)
    - Çift Cinsiyetli (Unisex) İsimleri Tespit Edip Tercih Sorabilme
    - Çoklu Niyet (Multi-Intent) & Olumsuzlama (Negation) Çıkarımı
    - Gelişmiş Türkçe Bütçe Ayrıştırma (1.5m üstü vs 1.5m altı vs aralık)
    - Dinamik PostgreSQL JSONB Donanım ve Araç Arama Motoru
    - Sıfır Araç / Yeni Araç Ayrımı & Güvenli Stok Doğrulama
    - Çapraz Model & Donanım Önerisi (Cross-Recommendation)
    - Zengin Frontend Filtre Senkronizasyonu (FilterAction)
    """

    def __init__(self, db: Session):
        self.db = db

    def process_message(
        self,
        message: str,
        customer_id: Optional[int] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        return ResponsePlanner.plan_and_execute(
            db=self.db,
            message=message,
            customer_id=customer_id,
            session_id=session_id
        )

    def reset_session(
        self,
        customer_id: Optional[int] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        return ResponsePlanner.reset_session(
            db=self.db,
            customer_id=customer_id,
            session_id=session_id
        )

    # Legacy Compatibility Wrappers
    def get_or_create_customer(self, customer_id: Optional[int] = None, session_id: Optional[str] = None) -> CustomerLead:
        lead, _ = ResponsePlanner.load_or_create_state(self.db, customer_id, session_id)
        return lead

    def _extract_contact_info(self, text: str, has_existing_name: bool = False) -> Dict[str, Any]:
        phone, phone_declined, clean_text = NLUParser.extract_phone(text)
        first_name, last_name, full_name = NLUParser.extract_name(clean_text, has_existing_name)
        crit = NLUParser.extract_vehicle_criteria(text)
        
        extracted = {}
        if phone: extracted["phone"] = phone
        if phone_declined: extracted["declined_phone"] = True
        if first_name:
            extracted["first_name"] = first_name
            extracted["last_name"] = last_name or ""
            extracted["full_name"] = full_name or first_name
        if crit.max_price is not None:
            extracted["budget_max"] = crit.max_price
        elif crit.min_price is not None:
            extracted["budget_max"] = crit.min_price
        if crit.brand: extracted["interested_brand"] = crit.brand
        if crit.body_type: extracted["interested_body_type"] = crit.body_type
        return extracted
