import logging
import datetime
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
from backend.db.models import Vehicle, CustomerLead, TestDrive
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
            if not new_crit.model and not new_crit.brand:
                state.vehicle_query.model = None
                lead.interested_model = None
                state.active_vehicle_id = None
                lead.focused_vehicle_id = None
                state.last_offer = None
                state.pending_clarification = None

        if new_crit.brand:
            state.vehicle_query.brand = new_crit.brand
            lead.interested_brand = new_crit.brand
            if not new_crit.model:
                state.vehicle_query.model = None
                lead.interested_model = None
                state.active_vehicle_id = None
                lead.focused_vehicle_id = None
                state.last_offer = None
                state.pending_clarification = None

        if new_crit.model:
            state.vehicle_query.model = new_crit.model
            lead.interested_model = new_crit.model
            # If explicit new model is asked, clear previous search features if they don't apply
            state.vehicle_query.features = [f for f in state.vehicle_query.features if f in new_crit.features]

        if new_crit.body_type:
            state.vehicle_query.body_type = new_crit.body_type
            lead.interested_body_type = new_crit.body_type
            if not new_crit.model:
                state.vehicle_query.model = None
                lead.interested_model = None
            if not new_crit.brand:
                state.vehicle_query.brand = None
                lead.interested_brand = None
            state.active_vehicle_id = None
            lead.focused_vehicle_id = None
            state.last_offer = None
            state.pending_clarification = None

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
            if not lead.interested_brand:
                lead.interested_brand = focused_v.brand
            if not lead.interested_model:
                lead.interested_model = focused_v.model
            if not lead.interested_body_type:
                lead.interested_body_type = focused_v.body_type
        else:
            state.active_vehicle_id = None
            lead.focused_vehicle_id = None

        reply_text = ""
        filter_action = None
        action = None
        matched_vehicles_data = []

        # Check follow-up confirmation ("Öyle yapalım", "Olur", "Evet", "İsterim", "Tamamdır")
        is_confirmation = "CONFIRMATION" in intents or (
            any(w in q_norm for w in ["olur", "evet", "isterim", "istiyorum", "tabi", "tabii", "tabiki", "tamamdir", "tamamdır", "tamam", "yapalim", "yapalım", "ayarlayalim", "ayarlayalım", "olusturalim", "oluşturalım", "harika olur", "super olur", "süper olur"])
            and len(msg_clean.split()) <= 4
            and not any(w in q_norm for w in ["nedir", "kac", "kaç", "fiyat", "km", "suv", "sedan", "benzin", "dizel", "nerede"])
        )
        if is_confirmation and state.last_offer:
            if state.last_offer.action_type == "FILTER_VEHICLES" and state.last_offer.criteria:
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
        
        # If user asks for a body_type or brand without asking a specific aspect, it is always a catalog search
        if (new_crit.body_type or new_crit.brand) and not new_crit.model and not concrete_aspects and "VEHICLE_OVERVIEW" not in intents:
            is_asking_info = False

        is_explicit_search = (
            not is_asking_info
            and (
                has_new_budget
                or new_crit.body_type is not None
                or new_crit.brand is not None
                or (
                    any(w in q_norm for w in ["goster", "göster", "listele", "filtrele", "bakiyorum", "bakıyorum", "istiyorum", "oner", "öner", "var mi", "var mı", "yok mu"])
                    and not any(w in q_norm for w in ["ne yakar", "beygir", "bagaj", "hasar", "tramer", "vitesi", "kilometresi", "bilgi", "hakkinda", "hakkında", "anlat", "tanit", "ozellik", "özellik"])
                )
                or (len(new_crit.features) > 0 and (new_crit.body_type or new_crit.transmission or new_crit.fuel_type or new_crit.min_price or new_crit.max_price))
            )
        )

        # Check if confirmation is accepting a test drive offer
        is_filter_offer = state.last_offer is not None and state.last_offer.action_type == "FILTER_VEHICLES"
        is_test_drive_confirmed = (
            is_confirmation
            and not is_filter_offer
            and not new_crit.is_new_vehicle_request
            and not is_explicit_search
            and (
                (state.last_offer and state.last_offer.action_type == "SCHEDULE_TEST_DRIVE")
                or state.pending_clarification == "TEST_DRIVE_OFFER"
            )
        )

        # Check datetime expressions & appointment requests
        dt_expr = NLUParser.extract_datetime_expression(msg_clean)
        is_appointment_datetime = "APPOINTMENT_DATETIME_PROVIDED" in intents or (state.appointment_pending and bool(dt_expr))
        is_appointment_request = (
            "APPOINTMENT_REQUEST" in intents
            or is_test_drive_confirmed
            or ("APPOINTMENT" in intents and not dt_expr and not ("VEHICLE_SEARCH" in intents and (new_crit.brand or new_crit.model)))
        )
        is_phone_declined_in_appointment = (state.appointment_pending or is_appointment_request or is_appointment_datetime) and ("PHONE_DECLINED" in intents or any(w in q_norm for w in ["vermek istemiyorum", "paylasamam", "paylaşamam", "vermeyegim", "vermicem", "vermiyorum", "numara yok", "telefon yok", "gizli", "veremem"]))

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
        elif state.customer.unisex_pending and len(lead.chat_history or []) <= 4 and not ("VEHICLE_DETAIL" in intents or "VEHICLE_SEARCH" in intents or is_appointment_datetime or is_appointment_request):
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

        # 2.3. Phone Policy Explanation / Direct Walk-in Showroom Visit without Phone
        elif "PHONE_POLICY_EXPLANATION" in intents:
            target_vehicle = focused_v
            if not target_vehicle and state.active_vehicle_id:
                target_vehicle = db.query(Vehicle).filter(Vehicle.id == state.active_vehicle_id).first()
            v_context = f"**{target_vehicle.brand} {target_vehicle.model}** veya " if target_vehicle else ""

            reply_text = (
                f"{salutation}, sistem üzerinden belirli bir gün ve saat için adınıza özel araç rezerve edebilmemiz, geçici kasko/sigorta hazırlıkları ve danışmanımızın randevu saatinde aracı sadece size hazır tutabilmesi adına resmi kayıtlarda telefon numarası zorunludur.\n\n"
                f"**Ancak telefon numaranızı paylaşmadan da test sürüşü yapabilirsiniz!** Bunun için önceden randevu oluşturmadan doğrudan **Arkas Spoticar Gaziemir Showroomumuzu (Akçay Cad. No: 284 Gaziemir / İZMİR)** ziyaret edebilirsiniz. Showroom satış danışmanlarımız {v_context}o sırada müsait olan araçlarımızla sizi kahvemiz eşliğinde ağırlamaktan ve test sürüşü imkanı sunmaktan memnuniyet duyacaktır. 😊🚗\n\n"
                f"Showroom ziyareti öncesinde araçlarımızın donanım, ekspertiz veya fiyat detaylarıyla ilgili merak ettiğiniz tüm soruları doğrudan bana sormaya devam edebilirsiniz!"
            )

        # 2.4. Phone Declined specifically during Test Drive Appointment Flow
        elif is_phone_declined_in_appointment:
            state.appointment_pending = True
            if dt_expr:
                state.appointment_datetime_text = dt_expr["formatted_text"]
            date_note = f"tercih ettiğiniz tarihi (**{dt_expr['formatted_text']}**) memnuniyetle not aldım. Ancak " if dt_expr else ""
            reply_text = (
                f"{salutation}, {date_note}Arkas Spoticar güvencesiyle adınıza özel test aracı rezerve edebilmemiz, plaka/kasko hazırlıkları ve satış danışmanımızın randevu teyidi sağlayabilmesi için iletişim numarası zorunludur.\n\n"
                f"Telefon numaranızı paylaşmak istememenizi gayet iyi anlıyorum. Dilerseniz önceden telefonla randevu kaydı oluşturmadan da doğrudan **Gaziemir Showroomumuzu (Akçay Cad. No: 284 Gaziemir / İZMİR)** ziyaret edebilirsiniz! Danışmanlarımız o an müsait olan araçlarımızla size test sürüşü yaptırmaktan memnuniyet duyacaktır. 🚗✨\n\n"
                f"Bu esnada araçlarımızın donanım, ekspertiz durumu veya fiyat koşullarıyla ilgili merak ettiğiniz soruları buradan yanıtlamaya devam edebilirim."
            )

        # 2.45. User Agrees / Decides to Share Phone Number
        elif "PHONE_AGREEMENT" in intents:
            state.appointment_pending = True
            state.customer.phone_declined = False
            target_vehicle = focused_v
            if not target_vehicle and state.active_vehicle_id:
                target_vehicle = db.query(Vehicle).filter(Vehicle.id == state.active_vehicle_id).first()
            if not target_vehicle and state.last_search_result_ids:
                target_vehicle = db.query(Vehicle).filter(Vehicle.id == state.last_search_result_ids[0]).first()

            v_title = f"**{target_vehicle.brand} {target_vehicle.model} {target_vehicle.package or ''}**" if target_vehicle else "Arkas Spoticar aracımız"
            dt_title = f" (**{state.appointment_datetime_text}**)" if state.appointment_datetime_text else ""

            reply_text = (
                f"Harika {salutation}! {v_title} için test sürüşü randevunuzu{dt_title} tamamlamak üzere **telefon numaranızı rica edebilir miyim?** 📱\n\n"
                f"Numaranızı ilettiğiniz anda randevunuzu showroom sistemimizde onaylayıp satış danışmanımıza ileteceğim."
            )

        # 2.5. Test Drive Appointment Scheduled (Date & Time Provided)
        elif is_appointment_datetime:
            parsed_date = dt_expr["date_obj"] if dt_expr else None
            time_str = dt_expr["time_str"] if dt_expr else "14:00"
            formatted_dt = dt_expr["formatted_text"] if dt_expr else msg_clean

            target_vehicle = focused_v
            if not target_vehicle and state.active_vehicle_id:
                target_vehicle = db.query(Vehicle).filter(Vehicle.id == state.active_vehicle_id).first()
            if not target_vehicle and state.last_search_result_ids:
                target_vehicle = db.query(Vehicle).filter(Vehicle.id == state.last_search_result_ids[0]).first()
            if not target_vehicle:
                target_vehicle = db.query(Vehicle).filter(Vehicle.is_active == True).first()

            v_title = f"{target_vehicle.brand} {target_vehicle.model} {target_vehicle.package or ''} ({target_vehicle.year})".strip() if target_vehicle else "Arkas Spoticar Showroom Aracı"
            cust_name = state.customer.full_name or (f"{state.customer.first_name} {state.customer.last_name}" if state.customer.last_name else state.customer.first_name) or "Değerli Müşterimiz"

            if target_vehicle:
                state.active_vehicle_id = target_vehicle.id
                lead.focused_vehicle_id = target_vehicle.id
                lead.interested_brand = target_vehicle.brand
                lead.interested_model = target_vehicle.model
                lead.interested_body_type = target_vehicle.body_type

            if state.customer.phone:
                test_drive = TestDrive(
                    customer_lead_id=lead.id,
                    vehicle_id=target_vehicle.id if target_vehicle else None,
                    customer_name=cust_name,
                    customer_phone=state.customer.phone,
                    appointment_date=parsed_date,
                    appointment_time=time_str,
                    appointment_datetime_text=formatted_dt,
                    showroom_location="Arkas Spoticar Gaziemir Showroom (Akçay Cad. No: 284 Gaziemir / İZMİR)",
                    status="CONFIRMED",
                    notes=f"AI Danışman üzerinden randevu oluşturuldu. İlgilenilen Araç: {v_title}"
                )
                db.add(test_drive)
                db.commit()
                db.refresh(test_drive)

                state.appointment_pending = False
                state.last_appointment_id = test_drive.id
                state.appointment_datetime_text = formatted_dt
                lead.conversation_summary = f"{lead.conversation_summary} | Randevu: {formatted_dt} ({v_title})"

                reply_text = (
                    f"Harika {salutation}! Test sürüşü randevunuzu başarıyla oluşturdum. 📅✨\n\n"
                    f"📋 **Randevu Detayları:**\n"
                    f"• 🚘 **Araç:** **{v_title}**\n"
                    f"• 🕒 **Tarih & Saat:** **{formatted_dt}**\n"
                    f"• 📍 **Lokasyon:** Arkas Spoticar Gaziemir Showroom (Akçay Cad. No: 284 Gaziemir / İZMİR)\n"
                    f"• 📱 **İletişim:** {state.customer.phone}\n\n"
                    f"Satış danışmanımız randevu saatinizde aracınızı test sürüşüne hazır tutacaktır. İletişim numaranıza bilgilendirme kaydı iletilmiştir.\n\n"
                    f"Showroom ziyareti öncesinde araç veya ekspertiz durumuyla ilgili sormak istediğiniz başka bir detay var mı?"
                )
            else:
                state.appointment_pending = True
                state.appointment_datetime_text = formatted_dt
                reply_text = (
                    f"Memnuniyetle {salutation}! **{v_title}** için **{formatted_dt}** test sürüşü talebinizi aldım. 📅✨\n\n"
                    f"Showroomumuzda aracı adınıza rezerve edebilmemiz, plaka/sigorta hazırlıklarını yapabilmemiz ve satış danışmanımızın randevu teyidini gerçekleştirebilmesi için **telefon numaranızı paylaşabilir misiniz?** 📱"
                )

        # 2.6. Test Drive Appointment Requested (Awaiting Date/Time)
        elif is_appointment_request:
            state.appointment_pending = True
            target_vehicle = focused_v
            if not target_vehicle and state.active_vehicle_id:
                target_vehicle = db.query(Vehicle).filter(Vehicle.id == state.active_vehicle_id).first()
            if not target_vehicle and state.last_search_result_ids:
                target_vehicle = db.query(Vehicle).filter(Vehicle.id == state.last_search_result_ids[0]).first()

            if target_vehicle:
                state.active_vehicle_id = target_vehicle.id
                lead.focused_vehicle_id = target_vehicle.id
                lead.interested_brand = target_vehicle.brand
                lead.interested_model = target_vehicle.model
                lead.interested_body_type = target_vehicle.body_type

            v_title = f"**{target_vehicle.brand} {target_vehicle.model} {target_vehicle.package or ''}**" if target_vehicle else "Arkas Spoticar portföyümüzdeki araçlarımız"
            
            if state.customer.phone:
                reply_text = (
                    f"Memnuniyetle {salutation}! {v_title} için test sürüşü ve danışman randevunuzu hemen planlayalım. 🚗✨\n\n"
                    f"📅 Size en uygun **gün ve saat aralığını** iletebilir misiniz? (Örn: *Yarın saat 14:00* veya *21.08.2026 - 14:00*)\n\n"
                    f"Gaziemir showroomumuzda satış danışmanımız aracınızı hazır ederek sizi kahvemiz eşliğinde ağırlayacaktır."
                )
            else:
                reply_text = (
                    f"Memnuniyetle {salutation}! {v_title} için test sürüşü ve danışman randevunuzu hemen planlayalım. 🚗✨\n\n"
                    f"📅 Size en uygun **gün ve saat aralığını** ve danışmanımızın aracı adınıza rezerve edip teyit sağlayabilmesi için **telefon numaranızı** iletebilir misiniz? 📱\n\n"
                    f"Gaziemir showroomumuzda satış danışmanımız aracınızı hazır ederek sizi kahvemiz eşliğinde ağırlayacaktır."
                )

        # 3. Dedicated Phone Submission Acknowledgment
        elif "PHONE_PROVIDED" in intents and not aspects and not ("VEHICLE_SEARCH" in intents and (new_crit.brand or new_crit.model or new_crit.body_type)):
            # If appointment was pending with a saved datetime, complete booking now!
            if state.appointment_pending and state.appointment_datetime_text:
                target_vehicle = focused_v
                if not target_vehicle and state.active_vehicle_id:
                    target_vehicle = db.query(Vehicle).filter(Vehicle.id == state.active_vehicle_id).first()
                if not target_vehicle and state.last_search_result_ids:
                    target_vehicle = db.query(Vehicle).filter(Vehicle.id == state.last_search_result_ids[0]).first()
                if not target_vehicle:
                    target_vehicle = db.query(Vehicle).filter(Vehicle.is_active == True).first()

                if target_vehicle:
                    state.active_vehicle_id = target_vehicle.id
                    lead.focused_vehicle_id = target_vehicle.id
                    lead.interested_brand = target_vehicle.brand
                    lead.interested_model = target_vehicle.model
                    lead.interested_body_type = target_vehicle.body_type

                v_title = f"{target_vehicle.brand} {target_vehicle.model} {target_vehicle.package or ''} ({target_vehicle.year})".strip() if target_vehicle else "Arkas Spoticar Showroom Aracı"
                cust_name = state.customer.full_name or (f"{state.customer.first_name} {state.customer.last_name}" if state.customer.last_name else state.customer.first_name) or "Değerli Müşterimiz"

                test_drive = TestDrive(
                    customer_lead_id=lead.id,
                    vehicle_id=target_vehicle.id if target_vehicle else None,
                    customer_name=cust_name,
                    customer_phone=state.customer.phone,
                    appointment_date=None,
                    appointment_time=None,
                    appointment_datetime_text=state.appointment_datetime_text,
                    showroom_location="Arkas Spoticar Gaziemir Showroom (Akçay Cad. No: 284 Gaziemir / İZMİR)",
                    status="CONFIRMED",
                    notes=f"AI Danışman üzerinden randevu oluşturuldu. İlgilenilen Araç: {v_title}"
                )
                db.add(test_drive)
                db.commit()
                db.refresh(test_drive)

                state.appointment_pending = False
                state.last_appointment_id = test_drive.id
                formatted_dt = state.appointment_datetime_text
                lead.conversation_summary = f"{lead.conversation_summary} | Randevu: {formatted_dt} ({v_title})"

                reply_text = (
                    f"Harika {salutation}! İletişim numaranızı ({state.customer.phone}) kaydettim ve test sürüşü randevunuzu başarıyla oluşturdum. 📅✨\n\n"
                    f"📋 **Randevu Detayları:**\n"
                    f"• 🚘 **Araç:** **{v_title}**\n"
                    f"• 🕒 **Tarih & Saat:** **{formatted_dt}**\n"
                    f"• 📍 **Lokasyon:** Arkas Spoticar Gaziemir Showroom (Akçay Cad. No: 284 Gaziemir / İZMİR)\n"
                    f"• 📱 **İletişim:** {state.customer.phone}\n\n"
                    f"Satış danışmanımız randevu saatinizde aracınızı test sürüşüne hazır tutacaktır. İletişim numaranıza bilgilendirme kaydı iletilmiştir.\n\n"
                    f"Showroom ziyareti öncesinde araç veya ekspertiz durumuyla ilgili sormak istediğiniz başka bir detay var mı?"
                )
            elif state.appointment_pending:
                reply_text = (
                    f"İletişim numaranızı ({state.customer.phone}) kaydettim {salutation}! 📱\n\n"
                    f"Test sürüşü için size en uygun **gün ve saat aralığını** iletebilir misiniz? (Örn: *Yarın saat 14:00* veya *21.08.2026 - 14:00*)\n\n"
                    f"Gaziemir showroomumuzda satış danışmanımız aracınızı hazır ederek sizi kahvemiz eşliğinde ağırlayacaktır."
                )
            elif state.last_appointment_id:
                td = db.query(TestDrive).filter(TestDrive.id == state.last_appointment_id).first()
                if td and not td.customer_phone:
                    td.customer_phone = state.customer.phone
                    db.commit()
                reply_text = (
                    f"İletişim numaranızı ({state.customer.phone}) test sürüşü randevunuza başarıyla ekledim {salutation}! 📱\n\n"
                    f"Satış danışmanımız randevu öncesinde sizinle iletişime geçerek hazırlıkları tamamlayacaktır.\n\n"
                    f"Bu esnada araçlarımızla ilgili merak ettiğiniz başka bir detay veya donanım sorusu var mı?"
                )
            else:
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
            else:
                # Overview or general vehicle enquiry concluded with test drive CTA
                state.last_offer = ActionOffer(
                    action_type="SCHEDULE_TEST_DRIVE",
                    description=f"{focused_v.brand} {focused_v.model} test sürüşü randevusu",
                    criteria={}
                )
                state.pending_clarification = "TEST_DRIVE_OFFER"

        # 6. General FAQ
        elif any(it in intents for it in ["TRADE_IN", "FINANCE", "LOCATION", "WARRANTY", "APPOINTMENT"]):
            reply_text = ChatbotTools.answer_general_faq(msg_clean, salutation)

        # 7. Vehicle Search / Recommendation / Refinement / Budget
        elif ("VEHICLE_SEARCH" in intents or "VEHICLE_RECOMMENDATION" in intents or "BUDGET_UPDATE" in intents or (is_confirmation and state.last_offer and state.last_offer.action_type == "FILTER_VEHICLES")):
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
                if state.vehicle_query.body_type and state.vehicle_query.body_type.lower() != "all":
                    alt_vehicles = db.query(Vehicle).filter(Vehicle.is_active == True).order_by(Vehicle.price.desc()).all()
                    if alt_vehicles:
                        alt_desc_list = [f"**{v.brand} {v.model}** ({v.body_type})" for v in alt_vehicles[:3]]
                        alt_str = ", ".join(alt_desc_list)
                        reply_text = (
                            f"{salutation}, istediğiniz kriterde **{state.vehicle_query.body_type}** araç şu anda stoklarımızda bulunmuyor. "
                            f"Ancak filtreleri esnetirseniz portföyümüzdeki alternatif modellerimiz ({alt_str}) mevcuttur.\n\n"
                            f"Dilerseniz bu alternatif modellerimizi inceleyebilir veya arama kriterlerinizi güncelleyebilirsiniz!"
                        )
                    else:
                        reply_text = (
                            f"{salutation}, istediğiniz kriterde **{state.vehicle_query.body_type}** araç şu anda stoklarımızda bulunmuyor.\n\n"
                            f"Filtreleri esneterek alternatif modellerimizi incelemek ister misiniz?"
                        )
                elif "sunroof" in state.vehicle_query.features:
                    alt_sunroof = VehicleSearchEngine.find_cross_alternative_with_feature(db, 0, "sunroof")
                    alt_txt = f"Panoramik Açılabilir Cam Tavan donanımına sahip **{alt_sunroof.brand} {alt_sunroof.model} {alt_sunroof.package or ''}** ({alt_sunroof.year})" if alt_sunroof else "farklı donanım paketlerimiz"
                    reply_text = (
                        f"{salutation}, aradığınız kriterlerde cam tavanlı araç bulunamadı. "
                        f"Ancak filtreleri esnetirseniz {alt_txt} modelimiz mevcuttur.\n\n"
                        f"Dilerseniz bu alternatif modelimizi detaylandırabilirim!"
                    )
                elif state.vehicle_query.max_price:
                    min_v = db.query(Vehicle).filter(Vehicle.is_active == True).order_by(Vehicle.price.asc()).first()
                    min_txt = f"portföyümüzdeki en uygun fiyatlı aracımız **{min_v.brand} {min_v.model}** ({min_v.price:,.0f} {min_v.currency}) modelidir.".replace(",", ".") if min_v else ""
                    reply_text = (
                        f"{salutation}, belirttiğiniz bütçede ({state.vehicle_query.max_price:,.0f} TL altı) bir araç şu anda stoklarımızda bulunmuyor. "
                        f"Ancak {min_txt}\n\n"
                        f"Bütçenizi esneterek bu aracımızı veya avantajlı taşıt kredisi seçeneklerimizi değerlendirmek ister misiniz?"
                    ).replace(",", ".")
                else:
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
