import unittest
from backend.db.database import SessionLocal, init_db
from backend.db.models import Vehicle, CustomerLead
from backend.agent.chatbot_agent import ChatbotAgent
from backend.agent.chatbot import ConversationState, VehicleQueryCriteria, ActionOffer
from backend.web.server import chat_with_agent, reset_chat, ChatRequest, ResetChatRequest

class ChatResetRegressionTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def setUp(self):
        self.db = SessionLocal()
        self.db.query(CustomerLead).filter(CustomerLead.session_id.like("reset_test_%")).delete(synchronize_session=False)
        self.db.commit()
        self.agent = ChatbotAgent(self.db)

    def tearDown(self):
        self.db.close()

    # TEST 1: apply filter -> reset chat -> filters empty
    def test_01_apply_filter_then_reset_chat_clears_filters(self):
        sid = "reset_test_01"
        # Step 1: Apply filter
        r1 = self.agent.process_message("SUV araçları göster", session_id=sid)
        self.assertIsNotNone(r1["filter_action"])
        self.assertEqual(r1["filter_action"]["body_type"], "SUV")

        # Step 2: Reset chat
        r2 = self.agent.process_message("Yeni sohbet", session_id=sid)
        self.assertEqual(r2["action"]["type"], "RESET_VEHICLE_FILTERS")
        self.assertEqual(r2["filter_action"]["type"], "RESET_VEHICLE_FILTERS")
        self.assertEqual(r2["filter_action"]["body_type"], "all")
        self.assertIsNone(r2["filter_action"]["min_price"])
        self.assertIsNone(r2["filter_action"]["max_price"])
        self.assertEqual(r2["filter_action"]["features"], [])

        # Validate DB lead state
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertEqual(lead.active_filters, {})
        self.assertIsNone(lead.interested_body_type)

    # TEST 2: apply price filter -> reset -> full inventory
    def test_02_apply_price_filter_then_reset_returns_full_inventory(self):
        sid = "reset_test_02"
        # Step 1: Price filter
        r1 = self.agent.process_message("1.5 milyon altı araçlar", session_id=sid)
        self.assertIsNotNone(r1["filter_action"])
        self.assertEqual(r1["filter_action"]["max_price"], 1500000.0)

        # Step 2: Reset
        r2 = self.agent.process_message("Sohbeti sıfırla", session_id=sid)
        all_active_count = self.db.query(Vehicle).filter(Vehicle.is_active == True).count()
        self.assertEqual(len(r2["matched_vehicles"]), all_active_count)
        self.assertEqual(r2["action"]["type"], "RESET_VEHICLE_FILTERS")

    # TEST 3: apply brand/model filter -> reset -> full inventory
    def test_03_apply_brand_model_filter_then_reset(self):
        sid = "reset_test_03"
        # Step 1: Brand/model filter
        r1 = self.agent.process_message("Peugeot 408 göster", session_id=sid)
        self.assertIsNotNone(r1["filter_action"])
        self.assertEqual(r1["filter_action"]["brand"], "Peugeot")
        self.assertEqual(r1["filter_action"]["model"], "408")

        # Step 2: Reset
        r2 = self.agent.process_message("Baştan başla", session_id=sid)
        all_active_count = self.db.query(Vehicle).filter(Vehicle.is_active == True).count()
        self.assertEqual(len(r2["matched_vehicles"]), all_active_count)
        self.assertEqual(r2["filter_action"]["brand"], "all")
        self.assertIsNone(r2["filter_action"]["model"])

    # TEST 4: apply multiple filters -> reset -> all filters cleared
    def test_04_apply_multiple_filters_then_reset_all_cleared(self):
        sid = "reset_test_04"
        r1 = self.agent.process_message("1.5m ile 2m arası otomatik dizel SUV cam tavanlı", session_id=sid)
        self.assertIsNotNone(r1["filter_action"])

        r2 = self.agent.process_message("filtreleri temizle", session_id=sid)
        self.assertEqual(r2["action"]["type"], "RESET_VEHICLE_FILTERS")
        self.assertEqual(r2["filter_action"]["brand"], "all")
        self.assertIsNone(r2["filter_action"]["model"])
        self.assertEqual(r2["filter_action"]["body_type"], "all")
        self.assertIsNone(r2["filter_action"]["min_price"])
        self.assertIsNone(r2["filter_action"]["max_price"])
        self.assertIsNone(r2["filter_action"]["transmission"])
        self.assertIsNone(r2["filter_action"]["fuel_type"])
        self.assertEqual(r2["filter_action"]["features"], [])

    # TEST 5: active vehicle -> reset -> active_vehicle=null
    def test_05_active_vehicle_reset(self):
        sid = "reset_test_05"
        r1 = self.agent.process_message("Peugeot 408 hakkında bilgi ver", session_id=sid)
        lead1 = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertIsNotNone(lead1.focused_vehicle_id)

        r2 = self.agent.process_message("reset", session_id=sid)
        lead2 = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertIsNone(lead2.focused_vehicle_id)
        self.assertIsNone(r2["conversation_state"]["active_vehicle_id"])

    # TEST 6: pending action & clarification -> reset -> pending_action=null
    def test_06_pending_action_reset(self):
        sid = "reset_test_06"
        # Ask question that generates an ActionOffer (sunroof on Honda City)
        r1 = self.agent.process_message("Honda City'de cam tavan var mı?", session_id=sid)
        state1 = r1["conversation_state"]
        self.assertIsNotNone(state1.get("last_offer"))

        r2 = self.agent.process_message("Yeni sohbet", session_id=sid)
        state2 = r2["conversation_state"]
        self.assertIsNone(state2.get("last_offer"))
        self.assertIsNone(state2.get("pending_clarification"))

    # TEST 7: last search results -> reset -> last_search_results updated to full or cleared
    def test_07_last_search_results_reset(self):
        sid = "reset_test_07"
        r1 = self.agent.process_message("1.5 milyon ile 2 milyon arası SUV göster", session_id=sid)
        self.assertEqual(len(r1["matched_vehicles"]), 3)

        r2 = self.agent.process_message("Yeni sohbet", session_id=sid)
        all_active_count = self.db.query(Vehicle).filter(Vehicle.is_active == True).count()
        self.assertEqual(len(r2["matched_vehicles"]), all_active_count)
        self.assertEqual(r2["conversation_state"]["vehicle_query"]["brand"], None)
        self.assertIsNone(r2["conversation_state"]["vehicle_query"]["min_price"])
        self.assertIsNone(r2["conversation_state"]["vehicle_query"]["max_price"])

    # TEST 8: frontend reset integration via API endpoint /api/chat/reset
    def test_08_api_reset_endpoint(self):
        sid = "reset_test_08"
        # 1. Chat via route function
        req1 = ChatRequest(message="1.5m altı araçlar", session_id=sid)
        data1 = chat_with_agent(req1, db=self.db)
        self.assertEqual(data1["filter_action"]["max_price"], 1500000.0)

        # 2. Reset endpoint via route function
        req2 = ResetChatRequest(session_id=sid)
        data2 = reset_chat(req2, db=self.db)
        self.assertEqual(data2["action"]["type"], "RESET_VEHICLE_FILTERS")
        self.assertEqual(data2["filter_action"]["type"], "RESET_VEHICLE_FILTERS")
        self.assertIsNone(data2["filter_action"]["max_price"])
        self.assertEqual(len(data2["matched_vehicles"]), 5)

    # TEST 9: full E2E conversation reset & inventory query
    def test_09_full_e2e_journey_reset_and_inventory_query(self):
        sid = "reset_test_09"

        # STEP 1: Filter 1.5m - 2m SUV
        r1 = self.agent.process_message("1.5 milyon ile 2 milyon arası SUV göster", session_id=sid)
        self.assertEqual(len(r1["matched_vehicles"]), 3)
        self.assertEqual(r1["filter_action"]["min_price"], 1500000.0)
        self.assertEqual(r1["filter_action"]["max_price"], 2000000.0)
        self.assertEqual(r1["filter_action"]["body_type"], "SUV")

        # STEP 2: Yeni sohbet
        r2 = self.agent.process_message("Yeni sohbet", session_id=sid)
        self.assertEqual(r2["action"]["type"], "RESET_VEHICLE_FILTERS")
        self.assertEqual(len(r2["matched_vehicles"]), 5)
        self.assertIn("sıfırlandı", r2["reply"])

        # STEP 3: "Şu anda kaç araç var?"
        r3 = self.agent.process_message("Şu anda kaç araç var?", session_id=sid)
        self.assertEqual(r3["action"]["type"], "RESET_VEHICLE_FILTERS")
        self.assertEqual(len(r3["matched_vehicles"]), 5)
        self.assertIn("5 adet", r3["reply"])
        self.assertIn("Citroën C5 Aircross", r3["reply"])
        self.assertIn("Peugeot 408", r3["reply"])
        self.assertIn("Honda City", r3["reply"])
        self.assertIn("Fiat Egea Cross", r3["reply"])
        self.assertIn("Peugeot 3008", r3["reply"])

    # TEST 10: "şu anda 3 araç görüyorum? tüm araçlar bunlar mı" query
    def test_10_clarification_3_arac_goruyorum(self):
        sid = "reset_test_10"
        r1 = self.agent.process_message("şu anda 3 araç görüyorum? tüm araçlar bunlar mı", session_id=sid)
        self.assertEqual(r1["action"]["type"], "RESET_VEHICLE_FILTERS")
        self.assertEqual(len(r1["matched_vehicles"]), 5)
        self.assertIn("5 adet", r1["reply"])

if __name__ == "__main__":
    unittest.main()
