import logging
import datetime
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
from backend.db.models import Vehicle, CustomerLead
from .state import ConversationState, CustomerContext, VehicleQueryCriteria, ActionOffer
from .nlu import NLUParser, norm
from .search_engine import VehicleSearchEngine
from .tools import ChatbotTools

logger = logging.getLogger(__name__)

class ResponsePlanner:
    @staticmethod
    def load_or_create_state(db: Session, customer_id: Optional[int] = None, session_id: Optional[str] = None) -> Tuple[CustomerLead, ConversationState]:
        lead = None
        if customer_id:
            lead = db.query(CustomerLead).filter(CustomerLead.id == customer_id).first()
        if not lead and session_id:
            lead = db.query(CustomerLead).filter(CustomerLead.session_id == session_id).first()

        if not lead:
            sid = session_id or f"session_{datetime.datetime.now(datetime.timezone.utc).timestamp()}"
            lead = CustomerLead(
                session_id=sid,
                chat_history=[],
                conversation_summary="Yeni müşteri sohbeti başladı.",
                conversation_state_json={},
                active_filters={}
            )
            db.add(lead)
            db.commit()
            db.refresh(lead)

        # Restore state from JSON if available
        state_dict = lead.conversation_state_json or {}
        if state_dict:
            try:
                state = ConversationState(**state_dict)
            except Exception:
                state = ConversationState(session_id=lead.session_id)
        else:
            state = ConversationState(session_id=lead.session_id)

        # Sync persistent fields from lead
        if lead.first_name: state.customer.first_name = lead.first_name
        if lead.last_name: state.customer.last_name = lead.last_name
        if lead.full_name: state.customer.full_name = lead.full_name
        if lead.phone: state.customer.phone = lead.phone
        if lead.phone_declined: state.customer.phone_declined = lead.phone_declined
        if lead.honorific_preference: state.customer.honorific_preference = lead.honorific_preference
        if lead.budget_min: state.vehicle_query.min_price = lead.budget_min
        if lead.budget_max: state.vehicle_query.max_price = lead.budget_max
        if lead.interested_brand: state.vehicle_query.brand = lead.interested_brand
        if lead.interested_body_type: state.vehicle_query.body_type = lead.interested_body_type
        return lead, state

    @staticmethod
    def reset_session(db: Session, customer_id: Optional[int] = None, session_id: Optional[str] = None) -> Dict[str, Any]:
        lead = None
        if customer_id:
            lead = db.query(CustomerLead).filter(CustomerLead.id == customer_id).first()
        if not lead and session_id:
            lead = db.query(CustomerLead).filter(CustomerLead.session_id == session_id).first()

        sid = session_id or (lead.session_id if lead else f"session_{datetime.datetime.now(datetime.timezone.utc).timestamp()}")
        state = ConversationState(session_id=sid)
        state.reset_all()

        if lead:
            lead.first_name = None
            lead.last_name = None
            lead.full_name = None
            lead.phone = None
            lead.phone_declined = False
            lead.honorific_preference = None
            lead.interested_brand = None
            lead.interested_model = None
            lead.interested_body_type = None
            lead.budget_min = None
            lead.budget_max = None
            lead.focused_vehicle_id = None
            lead.active_filters = {}
            lead.conversation_summary = "Sohbet ve tüm araç filtreleri sıfırlandı."
            lead.conversation_state_json = state.model_dump()
            lead.chat_history = []
            db.commit()
            db.refresh(lead)

        all_v = db.query(Vehicle).filter(Vehicle.is_active == True).order_by(Vehicle.price.desc()).all()
        reset_action = {
            "type": "RESET_VEHICLE_FILTERS",
            "brand": "all",
            "model": None,
            "body_type": "all",
            "min_price": None,
            "max_price": None,
            "min_km": None,
            "max_km": None,
            "fuel_type": None,
            "transmission": None,
            "features": [],
            "is_new": None,
            "search": "",
            "reset": True,
        }

        return {
            "reply": "Sohbet ve tüm araç filtreleri sıfırlandı. Merhaba! Size nasıl hitap etmemizi istersiniz? Adınızı, soyadınızı ve ilgilendiğiniz araç kriterlerini iletebilirsiniz.",
            "customer_id": lead.id if lead else 0,
            "customer_name": "",
            "action": {
                "type": "RESET_VEHICLE_FILTERS",
                "filters": {},
            },
            "filter_action": reset_action,
            "matched_vehicles": [v.to_dict() for v in all_v],
            "conversation_state": state.model_dump(),
        }

    @staticmethod
    def plan_and_execute(db: Session, message: str, customer_id: Optional[int] = None, session_id: Optional[str] = None) -> Dict[str, Any]:
        lead, state = ResponsePlanner.load_or_create_state(db, customer_id, session_id)
        msg_clean = message.strip()
        q_norm = norm(msg_clean)

        # 1. NLU Extraction
        phone, phone_declined, clean_text = NLUParser.extract_phone(msg_clean)
        first_name, last_name, full_name = NLUParser.extract_name(clean_text, has_existing_name=bool(state.customer.first_name))

        # Extract aspects & new criteria
        new_crit = NLUParser.extract_vehicle_criteria(msg_clean)
        aspects = NLUParser.extract_question_aspects(msg_clean)
        intents = NLUParser.extract_intents(
            msg_clean,
            has_customer_name=bool(first_name),
            has_phone=bool(phone),
            phone_declined=phone_declined,
            criteria=new_crit,
            aspects=aspects
        )
        state.intents = intents
        state.question_aspects = aspects

        # --- 0. CONVERSATION & FILTER RESET BRANCH ---
        if "CONVERSATION_RESET" in intents:
            state.reset_all()
            lead.first_name = None
            lead.last_name = None
            lead.full_name = None
            lead.phone = None
            lead.phone_declined = False
            lead.honorific_preference = None
            lead.interested_brand = None
            lead.interested_model = None
            lead.interested_body_type = None
            lead.budget_min = None
            lead.budget_max = None
            lead.focused_vehicle_id = None
            lead.active_filters = {}
            lead.conversation_summary = "Sohbet ve tüm araç filtreleri sıfırlandı."

            all_v = db.query(Vehicle).filter(Vehicle.is_active == True).order_by(Vehicle.price.desc()).all()
            matched_vehicles_data = [v.to_dict() for v in all_v]
            state.last_search_result_ids = [v.id for v in all_v]

            reply_text = (
                "Sohbet ve tüm araç filtreleri sıfırlandı. 🔄✨\n\n"
                "Merhaba! Arkas Spoticar Showroomuna hoş geldiniz. Tüm güncel araçlarımız yeniden listelendi.\n\n"
                "Size nasıl hitap etmemizi istersiniz? Aklınızdaki model (Peugeot 408, Citroën C5 Aircross, Honda City, Fiat Egea vb.), kasa tipi veya bütçenizi iletebilirsiniz."
            )
            reset_action = {
                "type": "RESET_VEHICLE_FILTERS",
                "brand": "all",
                "model": None,
                "body_type": "all",
                "min_price": None,
                "max_price": None,
                "min_km": None,
                "max_km": None,
                "fuel_type": None,
                "transmission": None,
                "features": [],
                "is_new": None,
                "search": "",
                "reset": True,
            }
            action = {"type": "RESET_VEHICLE_FILTERS", "filters": {}}

            now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
            lead.chat_history = [
                {"role": "user", "content": msg_clean, "timestamp": now_str},
                {"role": "assistant", "content": reply_text, "timestamp": now_str}
            ]
            lead.conversation_state_json = state.model_dump()
            db.commit()
            db.refresh(lead)

            return {
                "reply": reply_text,
                "customer_id": lead.id,
                "customer_name": "",
                "action": action,
                "filter_action": reset_action,
                "matched_vehicles": matched_vehicles_data,
                "conversation_state": state.model_dump()
            }

        # Contact state update
        if phone:
            state.customer.phone = phone
            lead.phone = phone
        if phone_declined:
            state.customer.phone_declined = True
            lead.phone_declined = True
        if first_name:
            state.customer.first_name = first_name
            state.customer.last_name = last_name
            state.customer.full_name = full_name
            lead.first_name = first_name
            lead.last_name = last_name
            lead.full_name = full_name

        # Honorific resolution
        honorific_choice, is_unisex = NLUParser.resolve_honorific(
            state.customer.first_name,
            msg_clean,
            past_preference=state.customer.honorific_preference
        )
        if honorific_choice:
            state.customer.honorific_preference = honorific_choice
            lead.honorific_preference = honorific_choice
            state.customer.unisex_pending = False
        elif is_unisex and not state.customer.honorific_preference:
            state.customer.unisex_pending = True

        salutation = state.customer.get_salutation()

        # Overwrite budget constraints if user provided new budget information
        has_new_budget = (new_crit.min_price is not None or new_crit.max_price is not None)
        if has_new_budget:
            state.vehicle_query.min_price = new_crit.min_price
            state.vehicle_query.max_price = new_crit.max_price
            lead.budget_min = new_crit.min_price
            lead.budget_max = new_crit.max_price

        if new_crit.brand:
            state.vehicle_query.brand = new_crit.brand
            lead.interested_brand = new_crit.brand
        if new_crit.model:
            state.vehicle_query.model = new_crit.model
            lead.interested_model = new_crit.model
            # If explicit new model is asked, clear previous search features if they don't apply
            state.vehicle_query.features = [f for f in state.vehicle_query.features if f in new_crit.features]

        if new_crit.body_type:
            state.vehicle_query.body_type = new_crit.body_type
            lead.interested_body_type = new_crit.body_type
        if new_crit.transmission:
            state.vehicle_query.transmission = new_crit.transmission
        if new_crit.transmission_excluded:
            state.vehicle_query.transmission_excluded = new_crit.transmission_excluded
        if new_crit.fuel_type:
            state.vehicle_query.fuel_type = new_crit.fuel_type
        if new_crit.fuel_type_excluded:
            state.vehicle_query.fuel_type_excluded = new_crit.fuel_type_excluded

        for feat in new_crit.features:
            if feat not in state.vehicle_query.features:
                state.vehicle_query.features.append(feat)
        for ex_feat in new_crit.features_excluded:
            if ex_feat not in state.vehicle_query.features_excluded:
                state.vehicle_query.features_excluded.append(ex_feat)
            if ex_feat in state.vehicle_query.features:
                state.vehicle_query.features.remove(ex_feat)

        if new_crit.is_new_vehicle_request:
            state.vehicle_query.is_new_vehicle_request = True

        # Resolve active vehicle
        focused_v = VehicleSearchEngine.resolve_active_vehicle(db, state.vehicle_query, state.active_vehicle_id)
        if focused_v:
            state.active_vehicle_id = focused_v.id
            lead.focused_vehicle_id = focused_v.id

        reply_text = ""
        filter_action = None
        action = None
        matched_vehicles_data = []

        # Check follow-up confirmation ("Öyle yapalım")
        is_confirmation = "CONFIRMATION" in intents
        if is_confirmation and state.last_offer:
            if state.last_offer.criteria:
                for k, v in state.last_offer.criteria.items():
                    if k == "features" and isinstance(v, list):
                        for f in v:
                            if f not in state.vehicle_query.features:
                                state.vehicle_query.features.append(f)
                    elif k == "min_price":
                        state.vehicle_query.min_price = v
                    elif k == "max_price":
                        state.vehicle_query.max_price = v
                    elif k == "body_type":
                        state.vehicle_query.body_type = v
                    elif k == "brand":
                        state.vehicle_query.brand = v
                    elif k == "model":
                        state.vehicle_query.model = v

        # Check if query is asking for information/aspects/overview vs an explicit catalog search
        concrete_aspects = [a for a in (aspects or []) if a != "overview"]
        is_asking_info = (
            "VEHICLE_OVERVIEW" in intents
            or bool(concrete_aspects)
            or any(w in q_norm for w in ["bilgi alabilir miyim", "bilgi almak istiyorum", "detayli anlat", "detaylı anlat", "anlatir misin", "anlatır mısın", "tanitir misin", "tanıtır mısın", "hakkinda bilgi", "hakkında bilgi", "araci anlat", "aracı anlat", "hakkinda", "hakkında", "detayli bilgi", "detaylı bilgi"])
        )
        is_explicit_search = (
            not is_asking_info
            and (
                has_new_budget
                or (new_crit.body_type is not None and not any(w in q_norm for w in ["nedir", "kac", "kaç", "neler", "nasil", "nasıl", "var mi", "var mı", "hakkinda", "hakkında", "bilgi", "anlat", "tanit"]))
                or (
                    any(w in q_norm for w in ["goster", "göster", "listele", "filtrele", "bakiyorum", "bakıyorum", "istiyorum", "oner", "öner"])
                    and not any(w in q_norm for w in ["nedir", "kac", "kaç", "neler", "nasil", "nasıl", "var mi", "var mı", "ne yakar", "beygir", "bagaj", "hasar", "tramer", "vitesi", "kilometresi", "bilgi", "hakkinda", "hakkında", "anlat", "tanit", "ozellik", "özellik"])
                )
                or (len(new_crit.features) > 0 and (new_crit.body_type or new_crit.transmission or new_crit.fuel_type or new_crit.min_price or new_crit.max_price))
            )
        )

        # --- RESPONSE BRANCHING ---

        # 0.5. Full Inventory Status / Query ("kaç araç var", "tüm araçlar bunlar mı")
        if "INVENTORY_QUERY" in intents:
            all_v = db.query(Vehicle).filter(Vehicle.is_active == True).order_by(Vehicle.price.desc()).all()
            total_count = len(all_v)
            matched_vehicles_data = [v.to_dict() for v in all_v]
            state.last_search_result_ids = [v.id for v in all_v]

            # Clear old restrictive criteria
            state.vehicle_query = VehicleQueryCriteria()
            state.active_vehicle_id = None
            lead.budget_min = None
            lead.budget_max = None
            lead.interested_brand = None
            lead.interested_model = None
            lead.interested_body_type = None
            lead.focused_vehicle_id = None
            lead.active_filters = {}

            lines = []
            for v in all_v:
                km_fmt = f"{v.km:,.0f} KM".replace(",", ".")
                price_fmt = f"{v.price:,.0f} {v.currency}".replace(",", ".")
                lines.append(f"• **{v.brand} {v.model} {v.package or ''}** ({v.year} | {km_fmt}) ➔ **{price_fmt}**")

            vehicles_text = "\n".join(lines)
            reply_text = (
                f"{salutation}, Arkas Spoticar showroomumuzda şu anda toplam **{total_count} adet** sertifikalı ve 100+ nokta kontrolünden geçmiş 2. el aracımız bulunmaktadır:\n\n"
                f"{vehicles_text}\n\n"
                f"Aklınızdaki kasa tipi (SUV, Sedan), donanım veya bütçe aralığına göre istediğiniz aracı doğrudan bana sorabilirsiniz!"
            )
            action = {"type": "RESET_VEHICLE_FILTERS", "filters": {}}
            filter_action = {
                "type": "RESET_VEHICLE_FILTERS",
                "brand": "all",
                "model": None,
                "body_type": "all",
                "min_price": None,
                "max_price": None,
                "min_km": None,
                "max_km": None,
                "fuel_type": None,
                "transmission": None,
                "features": [],
                "is_new": None,
                "search": "",
                "reset": True,
            }

        # 1. Unisex Clarification
        elif state.customer.unisex_pending and len(lead.chat_history or []) <= 4 and not ("VEHICLE_DETAIL" in intents or "VEHICLE_SEARCH" in intents):
            phone_note = f" (İletişim Numaranız: {state.customer.phone})" if state.customer.phone else (" (Telefon paylaşımı tercih edilmedi)" if state.customer.phone_declined else "")
            reply_text = (
                f"Çok memnun oldum {state.customer.first_name}{phone_note}! Bilgilerinizi Arkas güvencesiyle kaydettim.\n\n"
                f"Size nasıl hitap etmemi arzu edersiniz; **{state.customer.first_name} Bey** mi yoksa **{state.customer.first_name} Hanım** mı? 😊\n\n"
                f"Arkas Spoticar portföyümüzde sizin için nasıl bir araç bakalım? Aklınızda belirli bir model (Peugeot 408, Citroën C5 Aircross, Honda City vb.), "
                f"kasa tipi (SUV, Sedan) ya da belirlediğiniz bir bütçe aralığı var mı?"
            )

        # 2. Honorific Answer
        elif "HONORIFIC_PROVIDED" in intents and len(msg_clean.split()) <= 4:
            reply_text = (
                f"Memnuniyetle {salutation}! Tercihinizi not aldım. ✨\n\n"
                f"Arkas Spoticar portföyümüzde sizin için nasıl bir araç bakalım? Aklınızda belirli bir model (Peugeot 408, Citroën C5 Aircross, Honda City vb.), "
                f"kasa tipi (SUV, Sedan) ya da belirlediğiniz bir bütçe aralığı var mı?"
            )

        # 3. Dedicated Phone Submission Acknowledgment
        elif "PHONE_PROVIDED" in intents and not aspects and not ("VEHICLE_SEARCH" in intents and (new_crit.brand or new_crit.model or new_crit.body_type)):
            reply_text = (
                f"İletişim numaranızı ({state.customer.phone}) başarıyla kaydettim {salutation}! 📱\n\n"
                f"Arkas Spoticar satış danışmanımız en kısa sürede sizinle iletişime geçerek test sürüşü ve özel tekliflerimizi aktaracaktır.\n\n"
                f"Bu esnada araçlarımızla ilgili merak ettiğiniz başka bir detay veya donanım sorusu var mı?"
            )

        # 4. New Vehicle Request Handling
        elif state.vehicle_query.is_new_vehicle_request:
            new_results = VehicleSearchEngine.search_inventory(db, state.vehicle_query)
            if new_results:
                matched_vehicles_data = [v.to_dict() for v in new_results]
                lines = [f"• **{v.brand} {v.model} {v.package or ''}** ({v.year} | Sıfır KM) ➔ **{v.price:,.0f} {v.currency}**".replace(",", ".") for v in new_results]
                reply_text = f"{salutation}, stoklarımızdaki sıfır kilometre araçlar:\n\n" + "\n".join(lines)
            else:
                reply_text = (
                    f"{salutation}, şu anda stok veritabanımızda **sıfır kilometre / yeni araç** bulunmamaktadır.\n\n"
                    f"Portföyümüzdeki düşük kilometreli, detaylı ekspertizden geçmiş ve 12 ay Arkas Spoticar garantili 2. el araçlarımızı incelemek ister misiniz?"
                )

        # 5. Vehicle Specific Q&A and Comprehensive Overview Presentation
        elif (aspects or "VEHICLE_OVERVIEW" in intents or "VEHICLE_DETAIL" in intents or is_asking_info) and focused_v and not is_explicit_search:
            reply_text = ChatbotTools.answer_vehicle_aspects(focused_v, aspects, salutation, db)
            
            # If user asked about sunroof and car doesn't have it, prepare action offer
            if "sunroof" in aspects and not VehicleSearchEngine._vehicle_has_feature(focused_v, "sunroof"):
                state.last_offer = ActionOffer(
                    action_type="FILTER_VEHICLES",
                    description="Cam tavanlı araçları listele",
                    criteria={"features": ["sunroof"], "model": None, "brand": None}
                )

        # 6. General FAQ
        elif any(it in intents for it in ["TRADE_IN", "FINANCE", "LOCATION", "WARRANTY", "APPOINTMENT"]):
            reply_text = ChatbotTools.answer_general_faq(msg_clean, salutation)

        # 7. Vehicle Search / Recommendation / Refinement / Budget
        elif ("VEHICLE_SEARCH" in intents or "VEHICLE_RECOMMENDATION" in intents or "BUDGET_UPDATE" in intents or is_confirmation):
            search_results = VehicleSearchEngine.search_inventory(db, state.vehicle_query)
            if search_results:
                matched_vehicles_data = [v.to_dict() for v in search_results]
                state.last_search_result_ids = [v.id for v in search_results]
                flagship = search_results[0]
                state.active_vehicle_id = flagship.id
                lead.focused_vehicle_id = flagship.id

                filter_action = {
                    "type": "FILTER_VEHICLES",
                    "brand": state.vehicle_query.brand or "all",
                    "model": state.vehicle_query.model,
                    "body_type": state.vehicle_query.body_type or "all",
                    "min_price": state.vehicle_query.min_price,
                    "max_price": state.vehicle_query.max_price,
                    "transmission": state.vehicle_query.transmission,
                    "fuel_type": state.vehicle_query.fuel_type,
                    "features": state.vehicle_query.features,
                    "is_new": state.vehicle_query.is_new_vehicle_request,
                    "search": "",
                    "reset": False,
                }
                action = {"type": "FILTER_VEHICLES", "filters": filter_action}

                lines = []
                for v in search_results:
                    km_fmt = f"{v.km:,.0f} KM".replace(",", ".")
                    price_fmt = f"{v.price:,.0f} {v.currency}".replace(",", ".")
                    lines.append(f"• **{v.brand} {v.model} {v.package or ''}** ({v.year} | {km_fmt}) ➔ **{price_fmt}**")

                vehicles_text = "\n".join(lines)
                
                # Context message
                criteria_notes = []
                if state.vehicle_query.min_price and state.vehicle_query.max_price:
                    criteria_notes.append(f"{state.vehicle_query.min_price:,.0f} - {state.vehicle_query.max_price:,.0f} TL".replace(",", "."))
                elif state.vehicle_query.min_price:
                    criteria_notes.append(f"{state.vehicle_query.min_price:,.0f} TL üstü".replace(",", "."))
                elif state.vehicle_query.max_price:
                    criteria_notes.append(f"{state.vehicle_query.max_price:,.0f} TL altı".replace(",", "."))
                if state.vehicle_query.body_type:
                    criteria_notes.append(state.vehicle_query.body_type)
                if state.vehicle_query.transmission:
                    criteria_notes.append(state.vehicle_query.transmission)
                if "sunroof" in state.vehicle_query.features:
                    criteria_notes.append("Cam Tavanlı")

                crit_str = f" ({', '.join(criteria_notes)})" if criteria_notes else ""

                if "BUDGET_UPDATE" in intents:
                    if state.vehicle_query.min_price and state.vehicle_query.max_price:
                        target_budget_fmt = f"{state.vehicle_query.min_price:,.0f} - {state.vehicle_query.max_price:,.0f} TL".replace(",", ".")
                    elif state.vehicle_query.min_price:
                        target_budget_fmt = f"{state.vehicle_query.min_price:,.0f} TL üstü".replace(",", ".")
                    elif state.vehicle_query.max_price:
                        target_budget_fmt = f"{state.vehicle_query.max_price:,.0f} TL".replace(",", ".")
                    else:
                        target_budget_fmt = ""
                    reply_text = (
                        f"{salutation}, belirttiğiniz bütçeye (**{target_budget_fmt}**) en uygun güncel Arkas Spoticar araçlarımız:\n\n"
                        f"{vehicles_text}\n\n"
                        f"İncelemek istediğiniz modelin donanım veya ekspertiz durumunu detaylandırabilirim!"
                    )
                else:
                    reply_text = (
                        f"{salutation}, kriterlerinize{crit_str} en uygun güncel Arkas Spoticar araçlarımız:\n\n"
                        f"{vehicles_text}\n\n"
                        f"Araçların vitesini, kilometresini, ekspertiz durumunu veya donanım detaylarını doğrudan bana sorabilirsiniz!"
                    )
            else:
                filter_action = {
                    "type": "FILTER_VEHICLES",
                    "brand": state.vehicle_query.brand or "all",
                    "model": state.vehicle_query.model,
                    "body_type": state.vehicle_query.body_type or "all",
                    "min_price": state.vehicle_query.min_price,
                    "max_price": state.vehicle_query.max_price,
                    "transmission": state.vehicle_query.transmission,
                    "fuel_type": state.vehicle_query.fuel_type,
                    "features": state.vehicle_query.features,
                    "is_new": state.vehicle_query.is_new_vehicle_request,
                    "search": "",
                    "reset": False,
                }
                action = {"type": "FILTER_VEHICLES", "filters": filter_action}
                reply_text = (
                    f"{salutation}, aradığınız kriterlere uygun güncel bir araç şu an stoklarımızda bulunmuyor.\n\n"
                    f"Filtreleri esneterek alternatif modellerimizi incelemek ister misiniz?"
                )

        # 8. Introduction Only
        elif ("CUSTOMER_IDENTIFICATION" in intents or "PHONE_DECLINED" in intents) and len(lead.chat_history or []) <= 4:
            phone_note = f" (İletişim Numaranız: {state.customer.phone})" if state.customer.phone else (" (Telefon paylaşımı tercih edilmedi)" if state.customer.phone_declined else "")
            reply_text = (
                f"Çok memnun oldum {salutation}{phone_note}! Bilgilerinizi Arkas güvencesiyle kaydettim.\n\n"
                f"Arkas Spoticar portföyümüzde sizin için nasıl bir araç bakalım? Aklınızda belirli bir model (Peugeot 408, Citroën C5 Aircross, Honda City vb.), "
                f"kasa tipi (SUV, Sedan) ya da belirlediğiniz bir bütçe aralığı var mı?"
            )

        # 8.5. Gratitude & Conversation Closing ("teşekkür ederim", "sağolun", "iyi günler")
        elif "GRATITUDE" in intents and not aspects and not (new_crit.brand or new_crit.model or new_crit.body_type or new_crit.min_price or new_crit.max_price):
            if any(w in q_norm for w in ["iyi gunler", "iyi günler", "iyi aksamlar", "iyi akşamlar", "iyi geceler", "hosca kal", "hoşça kal", "hoscakal", "hoşçakal", "gorusmek uzere", "görüşmek üzere"]):
                reply_text = (
                    f"İyi günler dilerim {salutation}! 😊\n\n"
                    f"Aklınıza takılan başka bir soru veya incelemek istediğiniz bir araç olursa ben her zaman buradayım. Arkas Spoticar olarak keyifli ve güvenli sürüşler dileriz! 🚗✨"
                )
            else:
                reply_text = (
                    f"Rica ederim {salutation}! Yardımcı olabildiysem ne mutlu bana. 😊\n\n"
                    f"Arkas Spoticar araçlarımız, ekspertiz güvencemiz veya kredi koşullarımızla ilgili aklınıza takılan bir konu olursa dilediğiniz zaman sorabilirsiniz. Keyifli ve güvenli sürüşler dilerim! 🚗✨"
                )

        # 9. Fallback Greeting
        else:
            if not state.customer.first_name:
                reply_text = (
                    "Merhaba! Arkas Spoticar Yapay Zeka Satış Danışmanına hoş geldiniz. 🚗✨\n\n"
                    "Size en doğru araçları önerebilmem ve nasıl hitap edeceğimi bilmem için adınızı paylaşabilir misiniz?\n"
                    "Ayrıca aradığınız kriterlerde yeni bir araç stoğumuza girdiğinde ilk sizin haberiniz olması için telefon numaranızı da yazabilirsiniz."
                )
            else:
                reply_text = (
                    f"Merhaba {salutation}! Size nasıl yardımcı olabilirim? "
                    f"Arkas Spoticar portföyümüzdeki araçlarımızın donanım, ekspertiz, takas ve kredi koşullarını sorabilirsiniz."
                )

        # Append chat history
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        history = list(lead.chat_history or [])
        history.append({"role": "user", "content": msg_clean, "timestamp": now_str})
        history.append({"role": "assistant", "content": reply_text, "timestamp": now_str})
        lead.chat_history = history

        # Update CRM summary
        summary_parts = []
        if state.customer.full_name: summary_parts.append(f"Müşteri: {state.customer.full_name}")
        if state.customer.phone: summary_parts.append(f"Tel: {state.customer.phone}")
        if state.customer.phone_declined: summary_parts.append("Tel: Reddedildi")
        if state.vehicle_query.brand: summary_parts.append(f"Marka: {state.vehicle_query.brand}")
        if state.vehicle_query.min_price: summary_parts.append(f"Min: {state.vehicle_query.min_price:,.0f} TL".replace(",", "."))
        if state.vehicle_query.max_price: summary_parts.append(f"Max: {state.vehicle_query.max_price:,.0f} TL".replace(",", "."))
        if focused_v: summary_parts.append(f"İncelenen: {focused_v.brand} {focused_v.model}")

        lead.conversation_summary = " | ".join(summary_parts) if summary_parts else "Müşteri genel Spoticar araması yapıyor."
        lead.conversation_state_json = state.model_dump()
        if filter_action:
            lead.active_filters = filter_action

        db.commit()
        db.refresh(lead)

        return {
            "reply": reply_text,
            "customer_id": lead.id,
            "customer_name": state.customer.first_name or "",
            "action": action,
            "filter_action": filter_action,
            "matched_vehicles": matched_vehicles_data,
            "conversation_state": state.model_dump()
        }
