import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(100), unique=True, index=True, nullable=False)
    source = Column(String(100), default="Arkas 2. El")
    url = Column(String(500), nullable=True)
    
    brand = Column(String(100), index=True, nullable=False)
    model = Column(String(100), index=True, nullable=False)
    sub_model = Column(String(150), nullable=True)
    year = Column(Integer, nullable=False)
    km = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(10), default="TL")
    
    fuel_type = Column(String(50), nullable=True)
    transmission = Column(String(50), nullable=True)
    body_type = Column(String(50), nullable=True)
    color = Column(String(50), nullable=True)
    
    features = Column(JSON, default=list)
    expertise_note = Column(Text, nullable=True)
    image_urls = Column(JSON, default=list)
    primary_image_url = Column(String(1000), nullable=True)
    
    content_hash = Column(String(64), index=True, nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    briefs = relationship("CreativeBrief", back_populates="vehicle", cascade="all, delete-orphan")
    copies = relationship("MarketingCopy", back_populates="vehicle", cascade="all, delete-orphan")
    posters = relationship("Poster", back_populates="vehicle", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "external_id": self.external_id,
            "source": self.source,
            "url": self.url,
            "brand": self.brand,
            "model": self.model,
            "sub_model": self.sub_model,
            "year": self.year,
            "km": self.km,
            "price": self.price,
            "currency": self.currency,
            "fuel_type": self.fuel_type,
            "transmission": self.transmission,
            "body_type": self.body_type,
            "color": self.color,
            "features": self.features or [],
            "expertise_note": self.expertise_note,
            "image_urls": self.image_urls or [],
            "primary_image_url": self.primary_image_url,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "posters": [p.to_dict() for p in self.posters] if self.posters else [],
            "copies": [c.to_dict() for c in self.copies] if self.copies else []
        }


class CreativeBrief(Base):
    __tablename__ = "creative_briefs"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    
    brand_archetype = Column(String(100), nullable=False)
    target_persona = Column(String(255), nullable=False)
    emotional_points = Column(JSON, default=list)
    tone_of_voice = Column(String(100), nullable=False)
    key_hooks = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    vehicle = relationship("Vehicle", back_populates="briefs")

    def to_dict(self):
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "brand_archetype": self.brand_archetype,
            "target_persona": self.target_persona,
            "emotional_points": self.emotional_points,
            "tone_of_voice": self.tone_of_voice,
            "key_hooks": self.key_hooks,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class MarketingCopy(Base):
    __tablename__ = "marketing_copies"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    
    variant = Column(String(20), default="safe")  # "safe" or "bold"
    headline = Column(String(255), nullable=False)
    hook = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    cta = Column(String(150), nullable=False)
    story_frames = Column(JSON, default=list)
    hashtags = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    vehicle = relationship("Vehicle", back_populates="copies")

    def to_dict(self):
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "variant": self.variant,
            "headline": self.headline,
            "hook": self.hook,
            "body": self.body,
            "cta": self.cta,
            "story_frames": self.story_frames,
            "hashtags": self.hashtags,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Poster(Base):
    __tablename__ = "posters"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    
    poster_type = Column(String(50), default="instagram_post")  # "instagram_post", "story", "banner"
    file_path = Column(String(500), nullable=False)
    file_url = Column(String(500), nullable=False)
    title = Column(String(255), nullable=False)
    badge_text = Column(String(100), nullable=True)
    theme_color = Column(String(50), default="#E30613")
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    vehicle = relationship("Vehicle", back_populates="posters")

    def to_dict(self):
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "poster_type": self.poster_type,
            "file_url": self.file_url,
            "title": self.title,
            "badge_text": self.badge_text,
            "theme_color": self.theme_color,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
