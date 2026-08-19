import logging
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, not_
from backend.db.models import Vehicle
from .state import VehicleQueryCriteria
from .nlu import norm

logger = logging.getLogger(__name__)

class VehicleSearchEngine:
    @staticmethod
    def _vehicle_has_feature(vehicle: Vehicle, feature_key: str) -> bool:
        ad_feat = vehicle.ad_features or {}
        flat_feats = []
        for cat_items in ad_feat.values():
            if isinstance(cat_items, list):
                flat_feats.extend(cat_items)
            elif isinstance(cat_items, str):
                flat_feats.append(cat_items)
        
        flat_norm = [norm(f) for f in flat_feats]
        
        if feature_key == "sunroof":
            return any("cam tavan" in f or "sunroof" in f or "panoramik" in f for f in flat_norm)
        elif feature_key == "seat_heating":
            return any("isitma" in f or "ısıtma" in f for f in flat_norm)
        elif feature_key == "massage_seats":
            return any("masaj" in f for f in flat_norm)
        elif feature_key == "safety_assist":
            return any("serit" in f or "şerit" in f or "kor nokta" in f or "kör nokta" in f or "adaptif" in f for f in flat_norm)
        elif feature_key == "leather_seats":
            return any("deri" in f for f in flat_norm)
        return False

    @classmethod
    def search_inventory(cls, db: Session, criteria: VehicleQueryCriteria, limit: int = 10) -> List[Vehicle]:
        query = db.query(Vehicle).filter(Vehicle.is_active == True)

        # 1. New vs Used filter
        if criteria.is_new_vehicle_request:
            # 0 KM or brand new
            query = query.filter(Vehicle.km == 0)

        # 2. Brand
        if criteria.brand and criteria.brand.lower() != "all":
            query = query.filter(Vehicle.brand.ilike(f"%{criteria.brand}%"))

        # 3. Model
        if criteria.model:
            query = query.filter(Vehicle.model.ilike(f"%{criteria.model}%"))

        # 4. Body Type
        if criteria.body_type and criteria.body_type.lower() != "all":
            if criteria.body_type.upper() == "SUV":
                query = query.filter(or_(
                    Vehicle.body_type.ilike("%SUV%"),
                    Vehicle.body_type.ilike("%Crossover%"),
                    Vehicle.model.ilike("%Cross%"),
                    Vehicle.model.ilike("%3008%"),
                    Vehicle.model.ilike("%C5%"),
                    Vehicle.model.ilike("%408%")
                ))
            else:
                query = query.filter(Vehicle.body_type.ilike(f"%{criteria.body_type}%"))

        # 5. Price bounds
        if criteria.min_price is not None:
            query = query.filter(Vehicle.price >= criteria.min_price)
        if criteria.max_price is not None:
            query = query.filter(Vehicle.price <= criteria.max_price)

        # 6. KM bounds
        if criteria.min_km is not None:
            query = query.filter(Vehicle.km >= criteria.min_km)
        if criteria.max_km is not None:
            query = query.filter(Vehicle.km <= criteria.max_km)

        # 7. Fuel Type
        if criteria.fuel_type:
            if criteria.fuel_type.lower() == "dizel":
                query = query.filter(or_(
                    Vehicle.fuel_type.ilike("%Dizel%"),
                    Vehicle.package.ilike("%BlueHDi%"),
                    Vehicle.package.ilike("%Multijet%")
                ))
            elif criteria.fuel_type.lower() == "benzin":
                query = query.filter(or_(
                    Vehicle.fuel_type.ilike("%Benzin%"),
                    Vehicle.package.ilike("%PureTech%"),
                    Vehicle.package.ilike("%i-VTEC%"),
                    Vehicle.package.ilike("%TSI%")
                ))
            else:
                query = query.filter(Vehicle.fuel_type.ilike(f"%{criteria.fuel_type}%"))

        if criteria.fuel_type_excluded:
            query = query.filter(
                not_(Vehicle.fuel_type.ilike(f"%{criteria.fuel_type_excluded}%")),
                not_(Vehicle.package.ilike(f"%{criteria.fuel_type_excluded}%"))
            )

        # 8. Transmission
        if criteria.transmission:
            if criteria.transmission.lower() == "automatic":
                query = query.filter(or_(
                    Vehicle.transmission.ilike("%otomatik%"),
                    Vehicle.transmission.ilike("%eat8%"),
                    Vehicle.transmission.ilike("%cvt%"),
                    Vehicle.transmission.ilike("%dct%"),
                    Vehicle.transmission.ilike("%dsg%")
                ))
            elif criteria.transmission.lower() == "manual":
                query = query.filter(Vehicle.transmission.ilike("%manuel%"))

        if criteria.transmission_excluded:
            if criteria.transmission_excluded.lower() == "manual":
                query = query.filter(not_(Vehicle.transmission.ilike("%manuel%")))
            elif criteria.transmission_excluded.lower() == "automatic":
                query = query.filter(not_(or_(
                    Vehicle.transmission.ilike("%otomatik%"),
                    Vehicle.transmission.ilike("%eat8%"),
                    Vehicle.transmission.ilike("%cvt%"),
                    Vehicle.transmission.ilike("%dct%")
                )))

        # Ordering
        if criteria.sort_by == "price_asc":
            query = query.order_by(Vehicle.price.asc())
        elif criteria.sort_by == "km_asc":
            query = query.order_by(Vehicle.km.asc())
        else:
            query = query.order_by(Vehicle.price.desc())

        candidates = query.all()

        # In-Memory JSONB feature filtering
        filtered = []
        for v in candidates:
            # Check included features
            has_all_features = True
            for feat in criteria.features:
                if not cls._vehicle_has_feature(v, feat):
                    has_all_features = False
                    break
            if not has_all_features:
                continue

            # Check excluded features
            has_any_excluded = False
            for ex_feat in criteria.features_excluded:
                if cls._vehicle_has_feature(v, ex_feat):
                    has_any_excluded = True
                    break
            if has_any_excluded:
                continue

            filtered.append(v)

        return filtered[:limit]

    @classmethod
    def resolve_active_vehicle(cls, db: Session, criteria: VehicleQueryCriteria, current_vehicle_id: Optional[int] = None) -> Optional[Vehicle]:
        # 1. Exact model requested
        if criteria.model:
            v = db.query(Vehicle).filter(Vehicle.is_active == True, Vehicle.model.ilike(f"%{criteria.model}%")).first()
            if v:
                return v

        # 2. Brand requested
        if criteria.brand:
            v = db.query(Vehicle).filter(Vehicle.is_active == True, Vehicle.brand.ilike(f"%{criteria.brand}%")).first()
            if v:
                return v

        # 3. Maintain current active vehicle if exists
        if current_vehicle_id:
            v = db.query(Vehicle).filter(Vehicle.is_active == True, Vehicle.id == current_vehicle_id).first()
            if v:
                return v

        # 4. Default to first active vehicle
        return db.query(Vehicle).filter(Vehicle.is_active == True).order_by(Vehicle.price.desc()).first()

    @classmethod
    def find_cross_alternative_with_feature(cls, db: Session, current_vehicle_id: int, feature_key: str) -> Optional[Vehicle]:
        other_vehicles = db.query(Vehicle).filter(Vehicle.is_active == True, Vehicle.id != current_vehicle_id).all()
        for v in other_vehicles:
            if cls._vehicle_has_feature(v, feature_key):
                return v
        return None
