import unittest
from backend.db.database import SessionLocal, init_db
from backend.db.models import Vehicle, CustomerLead
from backend.agent.chatbot import ChatbotAgent, NLUParser, VehicleSearchEngine, ConversationState, VehicleQueryCriteria

class ProductionChatbotTestSuite(unittest.TestCase):
    def setUp(self):
        init_db()
        self.db = SessionLocal()
        self.db.query(CustomerLead).filter(CustomerLead.session_id.like("suite_s_%")).delete(synchronize_session=False)
        self.db.commit()
        self.agent = ChatbotAgent(self.db)

    def tearDown(self):
        self.db.close()

    # TEST 1: Ceren ben ama telefon numaramı vermiyorum
    def test_01_ceren_declined_phone(self):
        res = self.agent.process_message("Ceren ben ama telefon numaramı vermiyorum", session_id="suite_s_01")
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == "suite_s_01").first()
        self.assertEqual(lead.first_name, "Ceren")
        self.assertTrue(lead.phone_declined)
        self.assertIsNone(lead.phone)
        self.assertIn("Ceren Hanım", res["reply"])
        self.assertNotIn("Telefonumu", res["reply"])

    # TEST 2: telefonumu vermek istemiyorum
    def test_02_phone_declined_only_no_name(self):
        res = self.agent.process_message("telefonumu vermek istemiyorum", session_id="suite_s_02")
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == "suite_s_02").first()
        self.assertIsNone(lead.first_name)
        self.assertTrue(lead.phone_declined)
        self.assertNotIn("Telefonumu", res["reply"])
        self.assertNotIn("Bey", res["reply"])

    # TEST 3: Telefonumu Hanım (Unknown token validation)
    def test_03_safety_telefonumu_hanim(self):
        phone, pd, clean = NLUParser.extract_phone("Telefonumu Hanım")
        fn, ln, fl = NLUParser.extract_name(clean)
        self.assertIsNone(fn)
        hon, is_u = NLUParser.resolve_honorific(fn, "Telefonumu Hanım")
        self.assertIsNone(hon)

    # TEST 4: Telefonumu Bey (Unknown token validation)
    def test_04_safety_telefonumu_bey(self):
        phone, pd, clean = NLUParser.extract_phone("Telefonumu Bey")
        fn, ln, fl = NLUParser.extract_name(clean)
        self.assertIsNone(fn)
        hon, is_u = NLUParser.resolve_honorific(fn, "Telefonumu Bey")
        self.assertIsNone(hon)

    # TEST 5: Peugeot 408'in kilometresi kaç?
    def test_05_peugeot_408_aspect_mileage(self):
        crit = NLUParser.extract_vehicle_criteria("Peugeot 408'in kilometresi kaç?")
        aspects = NLUParser.extract_question_aspects("Peugeot 408'in kilometresi kaç?")
        self.assertEqual(crit.brand, "Peugeot")
        self.assertEqual(crit.model, "408")
        self.assertIn("mileage", aspects)

    # TEST 6: 408'in vitesi nedir? (Active vehicle context follow-up)
    def test_06_active_vehicle_context_followup(self):
        sid = "suite_s_06"
        r1 = self.agent.process_message("Peugeot 408 hakkında bilgi almak istiyorum", session_id=sid)
        lead1 = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertIsNotNone(lead1.focused_vehicle_id)

        r2 = self.agent.process_message("Vitesi nedir?", session_id=sid)
        self.assertIn("Otomatik", r2["reply"])
        self.assertIn("408", r2["reply"])

    # TEST 7: 1.5 milyon altı SUV
    def test_07_budget_max_suv(self):
        crit = NLUParser.extract_vehicle_criteria("1.5 milyon altı SUV")
        self.assertEqual(crit.max_price, 1500000.0)
        self.assertIsNone(crit.min_price)
        self.assertEqual(crit.body_type, "SUV")

    # TEST 8: 1.5m üstü SUV
    def test_08_budget_min_suv(self):
        crit = NLUParser.extract_vehicle_criteria("1.5m üstü SUV")
        self.assertEqual(crit.min_price, 1500000.0)
        self.assertIsNone(crit.max_price)
        self.assertEqual(crit.body_type, "SUV")

    # TEST 9: cam tavanlı araç göster
    def test_09_sunroof_feature(self):
        crit = NLUParser.extract_vehicle_criteria("cam tavanlı araç göster")
        self.assertIn("sunroof", crit.features)

    # TEST 10: öyle yapalım (Confirmation follow-up)
    def test_10_followup_confirmation_execution(self):
        sid = "suite_s_10"
        r1 = self.agent.process_message("Honda City'de cam tavan var mı?", session_id=sid)
        self.assertIn("bulunmamaktadır", r1["reply"].lower())

        r2 = self.agent.process_message("Öyle yapalım", session_id=sid)
        self.assertIn("C5 Aircross", r2["reply"])
        self.assertIsNotNone(r2["filter_action"])
        self.assertIn("sunroof", r2["filter_action"]["features"])

    # TEST 11: yeni araç istiyorum
    def test_11_new_vehicle_request(self):
        crit = NLUParser.extract_vehicle_criteria("yeni araç istiyorum")
        self.assertTrue(crit.is_new_vehicle_request)

    # TEST 12: sıfır araç göster
    def test_12_new_vehicle_query_handling(self):
        res = self.agent.process_message("sıfır araç göster", session_id="suite_s_12")
        self.assertIn("sıfır kilometre / yeni araç", res["reply"])

    # TEST 13: Peugeot 408 fiyatı kaç, kaç km ve vitesi ne?
    def test_13_multi_aspect_query(self):
        res = self.agent.process_message("Peugeot 408 fiyatı kaç, kaç km ve vitesi ne?", session_id="suite_s_13")
        self.assertIn("Fiyat", res["reply"])
        self.assertIn("Kilometre", res["reply"])
        self.assertIn("Şanzıman", res["reply"])

    # TEST 14: Ceren Ayruk - telefon numaramı vermek istemiyorum
    def test_14_name_surname_phone_declined(self):
        res = self.agent.process_message("Ceren Ayruk - telefon numaramı vermek istemiyorum", session_id="suite_s_14")
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == "suite_s_14").first()
        self.assertEqual(lead.first_name, "Ceren")
        self.assertEqual(lead.last_name, "Ayruk")
        self.assertTrue(lead.phone_declined)

    # TEST 15, 16, 17: UNISEX NAME FLOW (Deniz -> Unisex pending -> Bey -> Persistence)
    def test_15_16_17_unisex_honorific_flow(self):
        sid = "suite_s_unisex"
        r1 = self.agent.process_message("Merhaba ben Deniz", session_id=sid)
        self.assertIn("Deniz Bey", r1["reply"])
        self.assertIn("Deniz Hanım", r1["reply"])

        r2 = self.agent.process_message("Deniz Bey", session_id=sid)
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertEqual(lead.honorific_preference, "BEY")
        self.assertIn("Deniz Bey", r2["reply"])

        r3 = self.agent.process_message("408 kaç km?", session_id=sid)
        self.assertIn("Deniz Bey", r3["reply"])

    # TEST 18, 19, 20: TURKISH BUDGET FORMATS
    def test_18_19_20_budget_formats(self):
        _, max1, _ = NLUParser.extract_budget("1.500.000 TL bütçem var")
        self.assertEqual(max1, 1500000.0)

        _, max2, _ = NLUParser.extract_budget("1,5 milyon bütçe")
        self.assertEqual(max2, 1500000.0)

        _, max3, _ = NLUParser.extract_budget("1 milyon 500 bin TL")
        self.assertEqual(max3, 1500000.0)

    # TEST 21, 22, 23: NEGATIONS
    def test_21_sunroof_negation(self):
        crit = NLUParser.extract_vehicle_criteria("cam tavan istemiyorum")
        self.assertIn("sunroof", crit.features_excluded)

    def test_22_fuel_negation(self):
        crit = NLUParser.extract_vehicle_criteria("dizel olmasın")
        self.assertEqual(crit.fuel_type_excluded, "Dizel")

    def test_23_transmission_negation(self):
        crit = NLUParser.extract_vehicle_criteria("manuel istemiyorum")
        self.assertEqual(crit.transmission, "automatic")
        self.assertEqual(crit.transmission_excluded, "manual")

    # TEST 24: PHONE DETECTION
    def test_24_phone_detection(self):
        res = self.agent.process_message("telefon numaram 05321234567", session_id="suite_s_24")
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == "suite_s_24").first()
        self.assertEqual(lead.phone, "05321234567")

    # TEST 25 & 26: BRAND & MODEL RESOLUTION
    def test_25_brand_only(self):
        crit = NLUParser.extract_vehicle_criteria("Peugeot marka araç bakıyorum")
        self.assertEqual(crit.brand, "Peugeot")
        self.assertIsNone(crit.model)

    def test_26_model_resolution(self):
        crit = NLUParser.extract_vehicle_criteria("408 bakıyorum")
        self.assertEqual(crit.model, "408")
        self.assertEqual(crit.brand, "Peugeot")

    # TEST 27 & 28: SIMULTANEOUS FILTERS & BUDGET REFINEMENT
    def test_27_28_simultaneous_and_budget_refinement(self):
        sid = "suite_s_27_28"
        r1 = self.agent.process_message("1.5 milyon altı otomatik SUV ve cam tavanlı", session_id=sid)
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertEqual(lead.budget_max, 1500000.0)
        self.assertEqual(lead.interested_body_type, "SUV")

        r2 = self.agent.process_message("Bütçemi 2 milyona çıkarıyorum", session_id=sid)
        lead2 = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertEqual(lead2.budget_max, 2000000.0)
        self.assertIn("2.000.000 TL", r2["reply"])

    # TEST 29: BEN CEREN'İM + VEHICLE + PHONE DECLINED
    def test_29_all_in_one(self):
        res = self.agent.process_message("ben Ceren'im, SUV istiyorum, telefon vermeyeceğim", session_id="suite_s_29")
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == "suite_s_29").first()
        self.assertEqual(lead.first_name, "Ceren")
        self.assertTrue(lead.phone_declined)
        self.assertEqual(lead.interested_body_type, "SUV")

    # TEST 30, 31, 32: EXACT MODEL DISCOVERY
    def test_30_exact_c5(self):
        crit = NLUParser.extract_vehicle_criteria("c5 aircross göster")
        self.assertEqual(crit.model, "C5 Aircross")
        self.assertEqual(crit.brand, "Citroën")

    def test_31_exact_city(self):
        crit = NLUParser.extract_vehicle_criteria("city göster")
        self.assertEqual(crit.model, "City")
        self.assertEqual(crit.brand, "Honda")

    def test_32_exact_egea(self):
        crit = NLUParser.extract_vehicle_criteria("egea cross göster")
        self.assertEqual(crit.model, "Egea Cross")
        self.assertEqual(crit.brand, "Fiat")

    # =======================================================
    # NEW ROOT CAUSE REGRESSION TESTS (BUG #1 & BUG #2)
    # =======================================================

    # REGRESSION TEST 1: selam ceren ben, telefonumu vermek istemiyorum
    def test_regression_01_selam_ceren_ben_phone_declined(self):
        sid = "suite_s_reg_01"
        res = self.agent.process_message("selam ceren ben, telefonumu vermek istemiyorum", session_id=sid)
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertEqual(lead.first_name, "Ceren")
        self.assertIsNone(lead.last_name)
        self.assertIsNone(lead.phone)
        self.assertTrue(lead.phone_declined)
        self.assertEqual(lead.honorific_preference, "HANIM")
        self.assertIn("Ceren Hanım", res["reply"])
        self.assertNotIn("Telefonumu", res["reply"])
        self.assertNotIn("Bey", res["reply"])

    # REGRESSION TEST 2: telefonumu vermek istemiyorum (Phone decline variations)
    def test_regression_02_all_phone_decline_variations(self):
        variations = [
            "telefonumu vermek istemiyorum",
            "telefon numaramı vermek istemiyorum",
            "numaramı paylaşmak istemiyorum",
            "telefon vermeyeceğim",
            "numara vermicem",
            "telefon paylaşmak istemiyorum",
            "telefon yok",
            "numara vermek istemiyorum"
        ]
        for idx, text in enumerate(variations):
            sid = f"suite_s_decline_{idx}"
            res = self.agent.process_message(text, session_id=sid)
            lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
            self.assertIsNone(lead.first_name, f"Failed first_name None check for: {text}")
            self.assertTrue(lead.phone_declined, f"Failed phone_declined check for: {text}")
            self.assertNotIn("Telefonumu", res["reply"])
            self.assertNotIn("Bey", res["reply"])

    # REGRESSION TEST 3: Range "1.5m ile 2m arası bütçem var"
    def test_regression_03_range_1_5m_ile_2m_arasi(self):
        sid = "suite_s_reg_03"
        res = self.agent.process_message("1.5m ile 2m arası bütçem var", session_id=sid)
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertEqual(lead.budget_min, 1500000.0)
        self.assertEqual(lead.budget_max, 2000000.0)
        self.assertIsNotNone(res["filter_action"])
        self.assertEqual(res["filter_action"]["min_price"], 1500000.0)
        self.assertEqual(res["filter_action"]["max_price"], 2000000.0)
        self.assertEqual(len(res["matched_vehicles"]), 3)
        self.assertIn("1.500.000 - 2.000.000 TL", res["reply"])

    # REGRESSION TEST 4: Range format variations
    def test_regression_04_range_formats_parsing(self):
        ranges = [
            ("1.5m ile 2m arası", 1500000.0, 2000000.0),
            ("1.5 milyon ile 2 milyon arası", 1500000.0, 2000000.0),
            ("1.500.000 - 2.000.000", 1500000.0, 2000000.0),
            ("1.5M-2M", 1500000.0, 2000000.0),
            ("1,5 milyon - 2 milyon", 1500000.0, 2000000.0),
            ("1.5 ile 2 milyon", 1500000.0, 2000000.0),
            ("1 milyon 500 bin ile 2 milyon", 1500000.0, 2000000.0),
            ("1.5m - 2m bütçem var", 1500000.0, 2000000.0)
        ]
        for text, exp_min, exp_max in ranges:
            min_p, max_p, has_b = NLUParser.extract_budget(text)
            self.assertTrue(has_b, f"Failed has_budget for {text}")
            self.assertEqual(min_p, exp_min, f"Failed min_price for {text}")
            self.assertEqual(max_p, exp_max, f"Failed max_price for {text}")

    # REGRESSION TEST 5: Old max_price + New Range Override
    def test_regression_05_old_max_price_range_override(self):
        sid = "suite_s_reg_05"
        # Turn 1: 1.5m altı (max=1.5M)
        r1 = self.agent.process_message("1.5m altı araç bakıyorum", session_id=sid)
        lead1 = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertEqual(lead1.budget_max, 1500000.0)
        self.assertIsNone(lead1.budget_min)

        # Turn 2: 1.5m ile 2m arası (overrides old constraints to min=1.5M, max=2.0M)
        r2 = self.agent.process_message("1.5m ile 2m arası bütçem var", session_id=sid)
        lead2 = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertEqual(lead2.budget_min, 1500000.0)
        self.assertEqual(lead2.budget_max, 2000000.0)
        self.assertEqual(r2["filter_action"]["min_price"], 1500000.0)
        self.assertEqual(r2["filter_action"]["max_price"], 2000000.0)

    # REGRESSION TEST 6: Backend Search Range SQL
    def test_regression_06_backend_search_range_sql(self):
        c = VehicleQueryCriteria(min_price=1500000.0, max_price=2000000.0)
        results = VehicleSearchEngine.search_inventory(self.db, c)
        self.assertEqual(len(results), 3)
        for v in results:
            self.assertGreaterEqual(v.price, 1500000.0)
            self.assertLessEqual(v.price, 2000000.0)

    # COMPLETE MULTI-TURN CONVERSATION JOURNEY TEST
    def test_full_conversation_journey(self):
        sid = "suite_s_full_journey"

        # Turn 1: Introduction with phone decline
        r1 = self.agent.process_message("Selam, Ceren ben ama telefon numaramı vermicem.", session_id=sid)
        self.assertIn("Ceren Hanım", r1["reply"])
        lead1 = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertEqual(lead1.first_name, "Ceren")
        self.assertTrue(lead1.phone_declined)

        # Turn 2: Min price filter (1.5M üstü)
        r2 = self.agent.process_message("1.5 milyon üstü araç bakıyorum.", session_id=sid)
        self.assertIn("Ceren Hanım", r2["reply"])
        lead2 = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertEqual(lead2.budget_min, 1500000.0)

        # Turn 3: Body type refinement (SUV)
        r3 = self.agent.process_message("SUV olsun.", session_id=sid)
        lead3 = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertEqual(lead3.interested_body_type, "SUV")

        # Turn 4: Cam tavan
        r4 = self.agent.process_message("Cam tavan da olsun.", session_id=sid)
        self.assertIn("C5 Aircross", r4["reply"])

        # Turn 5: Model search Peugeot 408
        r5 = self.agent.process_message("Peugeot 408 var mı?", session_id=sid)
        self.assertIn("408", r5["reply"])

        # Turn 6: Specs follow up
        r6 = self.agent.process_message("Kaç km ve vitesi ne?", session_id=sid)
        self.assertIn("9.000 KM", r6["reply"])
        self.assertIn("Otomatik", r6["reply"])

        # Turn 7: New vehicle query
        r7 = self.agent.process_message("Yeni araçlardan da göster.", session_id=sid)
        self.assertIn("sıfır kilometre / yeni araç", r7["reply"])

        # Validate final state
        lead_final = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertEqual(lead_final.first_name, "Ceren")
        self.assertEqual(len(lead_final.chat_history), 14)  # 7 user + 7 assistant

    # TEST 33: Kasa Tipi Doğrudan Eşleşme (Sedan) & Çapraz Öneri Başlatmama Kuralı
    def test_33_sedan_direct_match_no_cross_recommendation(self):
        sid = "suite_s_33_sedan"
        r1 = self.agent.process_message("sedan araç yok mu?", session_id=sid)
        self.assertIn("Honda City", r1["reply"])
        self.assertIn("Sedan", r1["reply"])
        self.assertNotIn("incelediğimiz", r1["reply"].lower())
        self.assertNotIn("C5 Aircross", r1["reply"])
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertEqual(lead.interested_body_type, "Sedan")

    # TEST 34: Çok Turlu Bağlam Sıfırlama (SUV'dan Sedan'a Geçiş & Yoksa Şeffaf Çapraz Öneri)
    def test_34_multi_turn_body_type_reset_from_suv_to_sedan(self):
        sid = "suite_s_34_reset"
        # Turn 1: C5 Aircross detay sor
        r1 = self.agent.process_message("Citroën C5 Aircross hakkında bilgi verir misin?", session_id=sid)
        self.assertIn("C5 Aircross", r1["reply"])
        self.assertNotIn("incelediğimiz", r1["reply"].lower())

        # Turn 2: Yeni filtre (Sedan araç yok mu?) -> C5 odağı sıfırlanmalı, doğrudan Honda City sunulmalı
        r2 = self.agent.process_message("Sedan araç yok mu?", session_id=sid)
        self.assertIn("Honda City", r2["reply"])
        self.assertNotIn("C5 Aircross", r2["reply"])
        self.assertNotIn("incelediğimiz", r2["reply"].lower())

        # Turn 3: Stokta olmayan kasa tipi (Hatchback araç var mı?) -> Şeffaf çapraz öneri
        r3 = self.agent.process_message("Hatchback araç var mı?", session_id=sid)
        self.assertIn("stoklarımızda bulunmuyor", r3["reply"])
        self.assertIn("alternatif modellerimiz", r3["reply"])
        self.assertNotIn("incelediğimiz", r3["reply"].lower())

if __name__ == "__main__":
    unittest.main()

