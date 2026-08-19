from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class CustomerContext(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    phone_declined: bool = False
    honorific_preference: Optional[str] = None  # "BEY", "HANIM", "SAYIN"
    unisex_pending: bool = False

    def get_salutation(self) -> str:
        if not self.first_name:
            return "Değerli Müşterimiz"
        if self.honorific_preference == "BEY":
            return f"{self.first_name} Bey"
        elif self.honorific_preference == "HANIM":
            return f"{self.first_name} Hanım"
        elif self.honorific_preference == "SAYIN":
            return f"Sayın {self.first_name}"
        return f"{self.first_name}"

class VehicleQueryCriteria(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    body_type: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_km: Optional[int] = None
    max_km: Optional[int] = None
    fuel_type: Optional[str] = None
    fuel_type_excluded: Optional[str] = None
    transmission: Optional[str] = None
    transmission_excluded: Optional[str] = None
    features: List[str] = Field(default_factory=list)
    features_excluded: List[str] = Field(default_factory=list)
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    is_new_vehicle_request: bool = False
    sort_by: Optional[str] = None

    def is_empty(self) -> bool:
        return not (
            self.brand
            or self.model
            or self.body_type
            or self.min_price is not None
            or self.max_price is not None
            or self.min_km is not None
            or self.max_km is not None
            or self.fuel_type
            or self.fuel_type_excluded
            or self.transmission
            or self.transmission_excluded
            or bool(self.features)
            or bool(self.features_excluded)
            or self.is_new_vehicle_request
        )

class ActionOffer(BaseModel):
    action_type: str  # "FILTER_VEHICLES", "RESET_VEHICLE_FILTERS", "SEARCH_SUNROOF", "SEARCH_ALTERNATIVE"
    description: str
    criteria: Dict[str, Any] = Field(default_factory=dict)

class ConversationState(BaseModel):
    session_id: str
    customer: CustomerContext = Field(default_factory=CustomerContext)
    vehicle_query: VehicleQueryCriteria = Field(default_factory=VehicleQueryCriteria)
    active_vehicle_id: Optional[int] = None
    last_search_result_ids: List[int] = Field(default_factory=list)
    last_offer: Optional[ActionOffer] = None
    pending_clarification: Optional[str] = None
    conversation_stage: str = "DISCOVERY"
    question_aspects: List[str] = Field(default_factory=list)
    intents: List[str] = Field(default_factory=list)

    def reset_all(self):
        self.customer = CustomerContext()
        self.vehicle_query = VehicleQueryCriteria()
        self.active_vehicle_id = None
        self.last_search_result_ids = []
        self.last_offer = None
        self.pending_clarification = None
        self.conversation_stage = "DISCOVERY"
        self.question_aspects = []
        self.intents = ["CONVERSATION_RESET"]
