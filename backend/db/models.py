from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime,
    Text, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from .database import Base

class Vehicle(Base):
    """
    Arkas Spoticar 2. El Araç Modeli:
    - Teknik Özellikler, Donanımlar (5 Boyutlu), Ekspertiz & Hasar Raporu
    - 'images' ilişkisi ile VehicleImage tablosuna bağlanır (1-to-N)
    - 'brief' ilişkisi ile CreativeBrief tablosuna bağlanır (1-to-1)
    """
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(100), unique=True, index=True, nullable=False)
    source = Column(String(100), default="Sahibinden Arkas Spoticar")
    url = Column(String(500), nullable=True)

    # Core specs
    brand = Column(String(100), index=True, nullable=False)
    model = Column(String(100), index=True, nullable=False)
    package = Column(String(200), nullable=True)
    sub_model = Column(String(200), nullable=True)
    year = Column(Integer, index=True, nullable=False)
    km = Column(Integer, index=True, nullable=False)
    price = Column(Float, index=True, nullable=False)
    currency = Column(String(10), default="TL")

    # Additional attributes
    fuel_type = Column(String(50), nullable=True)
    transmission = Column(String(50), nullable=True)
    body_type = Column(String(50), nullable=True)
    color = Column(String(50), nullable=True)
    engine_power = Column(String(50), nullable=True)
    engine_capacity = Column(String(50), nullable=True)

    # Rich JSON attributes
    technical_specs = Column(JSON, default=dict)
    ad_features = Column(JSON, default=dict)
    damage_expertise = Column(JSON, default=dict)
    expertise_note = Column(Text, nullable=True)

    # Primary Cover Image
    primary_image_url = Column(String(500), nullable=True)

    # Metadata & Tracking
    content_hash = Column(String(64), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    images = relationship("VehicleImage", back_populates="vehicle", cascade="all, delete-orphan", order_by="VehicleImage.display_order")
    brief = relationship("CreativeBrief", back_populates="vehicle", uselist=False, cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "external_id": self.external_id,
            "source": self.source,
            "url": self.url,
            "brand": self.brand,
            "model": self.model,
            "package": self.package,
            "sub_model": self.sub_model,
            "year": self.year,
            "km": self.km,
            "price": self.price,
            "currency": self.currency,
            "fuel_type": self.fuel_type,
            "transmission": self.transmission,
            "body_type": self.body_type,
            "color": self.color,
            "engine_power": self.engine_power,
            "engine_capacity": self.engine_capacity,
            "technical_specs": self.technical_specs or {},
            "ad_features": self.ad_features or {},
            "damage_expertise": self.damage_expertise or {},
            "expertise_note": self.expertise_note,
            "primary_image_url": self.primary_image_url,
            "images": [img.to_dict() for img in self.images] if self.images else [],
            "image_urls": [img.image_url for img in self.images] if self.images else ([self.primary_image_url] if self.primary_image_url else []),
            "brief": self.brief.to_dict() if self.brief else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

class VehicleImage(Base):
    """
    Araca ait tüm görsellerin tutulduğu tablo (ul.classifiedDetailThumbList / image_0, image_1...)
    """
    __tablename__ = "vehicle_images"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    caption = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    vehicle = relationship("Vehicle", back_populates="images")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "image_url": self.image_url,
            "is_primary": self.is_primary,
            "display_order": self.display_order,
            "caption": self.caption,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class CreativeBrief(Base):
    """
    Her araca özel stratejik analiz, persona ve üretilen 3-tonlu reklam metinleri:
    - balanced_copy (Dengeli / Şeffaf)
    - professional_copy (Kurumsal / Saygın)
    - engaging_copy (İlgi Çekici / Enerjik)
    - story_frames (Instagram Story Akışı)
    """
    __tablename__ = "creative_briefs"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), unique=True, nullable=False)
    brand_archetype = Column(String(100), nullable=False)
    target_persona = Column(String(150), nullable=False)
    emotional_points = Column(JSON, default=list)
    tone_of_voice = Column(String(100), nullable=False)
    key_hooks = Column(JSON, default=list)

    # Generated copy texts for 3 tones
    balanced_copy = Column(Text, nullable=True)
    professional_copy = Column(Text, nullable=True)
    engaging_copy = Column(Text, nullable=True)
    story_frames = Column(JSON, default=list)
    hashtags = Column(JSON, default=list)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    vehicle = relationship("Vehicle", back_populates="brief")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "brand_archetype": self.brand_archetype,
            "target_persona": self.target_persona,
            "emotional_points": self.emotional_points,
            "tone_of_voice": self.tone_of_voice,
            "key_hooks": self.key_hooks,
            "balanced_copy": self.balanced_copy,
            "professional_copy": self.professional_copy,
            "engaging_copy": self.engaging_copy,
            "story_frames": self.story_frames,
            "hashtags": self.hashtags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class CustomerLead(Base):
    """
    Bilişsel AI Satış Danışmanı Müşteri Takip Tablosu
    """
    __tablename__ = "customer_leads"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    full_name = Column(String(200), nullable=True)
    phone = Column(String(50), nullable=True)
    phone_declined = Column(Boolean, default=False)
    honorific_preference = Column(String(20), nullable=True)  # "BEY", "HANIM", "SAYIN"

    # Active Preferences
    interested_brand = Column(String(100), nullable=True)
    interested_model = Column(String(100), nullable=True)
    interested_body_type = Column(String(50), nullable=True)
    budget_min = Column(Float, nullable=True)
    budget_max = Column(Float, nullable=True)
    focused_vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="SET NULL"), nullable=True)

    # Conversation State Persistence
    active_filters = Column(JSON, default=dict)
    conversation_state_json = Column(JSON, default=dict)
    chat_history = Column(JSON, default=list)
    conversation_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    test_drives = relationship("TestDrive", back_populates="customer_lead", cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "phone": self.phone,
            "phone_declined": bool(self.phone_declined),
            "honorific_preference": self.honorific_preference,
            "interested_brand": self.interested_brand,
            "interested_model": self.interested_model,
            "interested_body_type": self.interested_body_type,
            "budget_min": self.budget_min,
            "budget_max": self.budget_max,
            "focused_vehicle_id": self.focused_vehicle_id,
            "active_filters": self.active_filters or {},
            "conversation_state_json": self.conversation_state_json or {},
            "chat_history": self.chat_history or [],
            "conversation_summary": self.conversation_summary,
            "test_drives": [td.to_dict() for td in self.test_drives] if self.test_drives else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

class TestDrive(Base):
    """
    Arkas Spoticar 2. El Test Sürüşü & Showroom Randevu Tablosu
    """
    __tablename__ = "test_drives"

    id = Column(Integer, primary_key=True, index=True)
    customer_lead_id = Column(Integer, ForeignKey("customer_leads.id", ondelete="CASCADE"), nullable=False, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="SET NULL"), nullable=True, index=True)

    customer_name = Column(String(200), nullable=True)
    customer_phone = Column(String(50), nullable=True)

    appointment_date = Column(DateTime, nullable=True)
    appointment_time = Column(String(50), nullable=True)
    appointment_datetime_text = Column(String(150), nullable=False)
    showroom_location = Column(String(250), default="Arkas Spoticar Gaziemir Showroom (Akçay Cad. No: 284 Gaziemir / İZMİR)")

    status = Column(String(50), default="CONFIRMED")  # CONFIRMED, PENDING, COMPLETED, CANCELLED
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer_lead = relationship("CustomerLead", back_populates="test_drives")
    vehicle = relationship("Vehicle", backref="test_drives")

    def to_dict(self) -> Dict[str, Any]:
        vehicle_title = None
        if self.vehicle:
            vehicle_title = f"{self.vehicle.brand} {self.vehicle.model} {self.vehicle.package or ''} ({self.vehicle.year})".strip()

        return {
            "id": self.id,
            "customer_lead_id": self.customer_lead_id,
            "vehicle_id": self.vehicle_id,
            "vehicle_title": vehicle_title,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "appointment_date": self.appointment_date.isoformat() if self.appointment_date else None,
            "appointment_time": self.appointment_time,
            "appointment_datetime_text": self.appointment_datetime_text,
            "showroom_location": self.showroom_location,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

