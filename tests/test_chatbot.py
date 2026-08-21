import unittest
from backend.db.database import SessionLocal, init_db
from backend.db.models import Vehicle, CustomerLead
from backend.agent.chatbot_agent import ChatbotAgent

class ComprehensiveTestChatbotAgent(unittest.TestCase):
    def setUp(self):
        init_db()
        self.db = SessionLocal()
        self.db.query(CustomerLead).filter(CustomerLead.session_id.like("test_s_%")).delete(synchronize_session=False)
        self.db.commit()
        self.agent = ChatbotAgent(self.db)

    def tearDown(self):
        self.db.close()

    def test_male_ner_honorific(self):
        res = self.agent.process_message("Merhaba ben Ahmet Yılmaz, araç bakıyorum", session_id="test_s_male")
        self.assertIn("Ahmet Bey", res["reply"])
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == "test_s_male").first()
        self.assertEqual(lead.first_name, "Ahmet")
        self.assertEqual(lead.last_name, "Yılmaz")

    def test_female_ner_honorific(self):
        res = self.agent.process_message("İsmim Zeynep Demir, otomatik SUV arıyorum", session_id="test_s_female")
        self.assertIn("Zeynep Hanım", res["reply"])
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == "test_s_female").first()
        self.assertEqual(lead.first_name, "Zeynep")

    def test_declined_phone_intent(self):
        res = self.agent.process_message("Telefon numaramı vermek istemiyorum", session_id="test_s_declined")
        self.assertNotIn("Hata", res["reply"])
        self.assertTrue("telefon paylaşımı tercih edilmedi" in res["reply"].lower() or "portföyümüzde" in res["reply"].lower())

    def test_ceren_ben_declined_phone(self):
        res = self.agent.process_message("Merhaba Ceren ben telefon numaramı vermek istemiyorum", session_id="test_s_ceren_ben")
        self.assertIn("Ceren Hanım", res["reply"])
        self.assertIn("Telefon paylaşımı tercih edilmedi", res["reply"])
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == "test_s_ceren_ben").first()
        self.assertEqual(lead.first_name, "Ceren")

    def test_unisex_flow_deniz(self):
        # Step 1: Unisex name greeting asks for Bey vs Hanım
        r1 = self.agent.process_message("Merhaba Deniz ben telefonumu vermek istemiyorum", session_id="test_s_deniz_unisex")
        self.assertIn("Deniz", r1["reply"])
        self.assertIn("Deniz Bey", r1["reply"])
        self.assertIn("Deniz Hanım", r1["reply"])
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == "test_s_deniz_unisex").first()
        self.assertEqual(lead.first_name, "Deniz")

        # Step 2: User specifies honorific
        r2 = self.agent.process_message("Deniz Bey diyebilirsiniz", session_id="test_s_deniz_unisex")
        self.assertIn("Deniz Bey", r2["reply"])

        # Step 3: Follow up uses established honorific
        r3 = self.agent.process_message("408 kaç km?", session_id="test_s_deniz_unisex")
        self.assertIn("Deniz Bey", r3["reply"])
        self.assertIn("9.000 KM", r3["reply"])

    def test_phone_number_extraction(self):
        res = self.agent.process_message("İletişim için numaram +90 542 888 99 00", session_id="test_s_phone_extract")
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == "test_s_phone_extract").first()
        self.assertEqual(lead.phone, "05428889900")

    def test_various_budget_formats(self):
        test_cases = [
            ("1.500.000 TL bütçem var", 1500000.0),
            ("1,8 milyon tl bütçe", 1800000.0),
            ("2m bütçem bulunuyor", 2000000.0),
            ("1350000 TL", 1350000.0),
            ("900 bin tl", 900000.0),
        ]
        for idx, (text, expected_val) in enumerate(test_cases):
            sid = f"test_s_budget_fmt_{idx}"
            self.agent.process_message(text, session_id=sid)
            lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
            self.assertEqual(lead.budget_max, expected_val, f"Failed for {text}")

    def test_budget_expansion_command(self):
        res = self.agent.process_message("Fiyat aralığını 5m kadar çıkart", session_id="test_s_exp_5m")
        self.assertIn("5.000.000 TL", res["reply"])
        self.assertIsNotNone(res["filter_action"])
        self.assertEqual(res["filter_action"]["max_price"], 5000000.0)

    def test_peugeot_408_specs_and_km(self):
        res = self.agent.process_message("Peugeot 408 kilometresi ve yakıtı nedir?", session_id="test_s_408")
        self.assertIn("408", res["reply"])
        self.assertIn("9.000 KM", res["reply"])
        self.assertIn("6.0 lt", res["reply"])

    def test_c5_aircross_sunroof_and_comfort(self):
        res = self.agent.process_message("C5 Aircross cam tavan ve süspansiyon özellikleri neler?", session_id="test_s_c5")
        self.assertIn("C5 Aircross", res["reply"])
        self.assertIn("Cam Tavan", res["reply"])

    def test_honda_city_price_and_specs(self):
        res = self.agent.process_message("Honda City fiyatı ve beygir gücü nedir?", session_id="test_s_city")
        self.assertIn("City", res["reply"])
        self.assertIn("1.365.000", res["reply"])
        self.assertIn("121 HP", res["reply"])

    def test_egea_cross_fuel_and_expertise(self):
        res = self.agent.process_message("Fiat Egea Cross ekspertiz ve hasar durumu nedir?", session_id="test_s_egea")
        self.assertIn("Egea Cross", res["reply"])
        self.assertIn("Boyalı Parça", res["reply"])
        self.assertIn("Tramer", res["reply"])

    def test_peugeot_3008_bagaj_and_vites(self):
        res = self.agent.process_message("3008 modelinizin bagaj hacmi kaç litre?", session_id="test_s_3008")
        self.assertIn("3008", res["reply"])
        self.assertIn("520 lt", res["reply"])

    def test_cross_recommendation_sunroof_for_non_sunroof_car(self):
        # Honda City doesn't have sunroof in DB, C5 Aircross does
        res = self.agent.process_message("Honda City'de cam tavan var mı?", session_id="test_s_city_sunroof")
        self.assertIn("bulunmamaktadır", res["reply"].lower())
        self.assertIn("C5 Aircross", res["reply"])

    def test_trade_in_intent(self):
        res = self.agent.process_message("2018 model Megane aracım var, takas yapıyor musunuz?", session_id="test_s_trade")
        self.assertTrue(any(w in res["reply"].lower() for w in ["takas", "ekspertiz", "değerlendirme"]))

    def test_financing_and_credit_intent(self):
        res = self.agent.process_message("Taşıt kredisi veya taksit imkanlarınız neler?", session_id="test_s_credit")
        self.assertTrue(any(w in res["reply"].lower() for w in ["kredi", "finansman", "taksit"]))

    def test_showroom_location_and_hours(self):
        res = self.agent.process_message("Showroomunuz nerede ve saat kaça kadar açık?", session_id="test_s_loc")
        self.assertTrue(any(w in res["reply"].lower() for w in ["showroom", "plaza", "merkez", "adres"]))

    def test_warranty_and_inspection(self):
        res = self.agent.process_message("Araçlarınızda garanti var mı, kaç nokta kontrol yapılıyor?", session_id="test_s_warranty")
        self.assertTrue(any(w in res["reply"].lower() for w in ["100+", "garanti", "ekspertiz"]))

    def test_multi_turn_session_flow(self):
        sid = "test_s_multi_turn_flow"
        # Turn 1: Introduction
        r1 = self.agent.process_message("Merhaba adım Burak Öz, 1.5M bütçem var", session_id=sid)
        self.assertIn("Burak Bey", r1["reply"])
        
        # Turn 2: Follow up question without repeating name
        r2 = self.agent.process_message("408 modelinin vitesi nasıl?", session_id=sid)
        self.assertIn("Burak Bey", r2["reply"])
        self.assertIn("Otomatik", r2["reply"])

        # Turn 3: Phone number provision
        r3 = self.agent.process_message("0533 111 22 33 numaramdan ulaşabilirsiniz", session_id=sid)
        lead = self.db.query(CustomerLead).filter(CustomerLead.session_id == sid).first()
        self.assertEqual(lead.phone, "05331112233")
        self.assertEqual(lead.first_name, "Burak")
        self.assertEqual(lead.last_name, "Öz")
        self.assertEqual(len(lead.chat_history), 6)  # 3 user + 3 assistant

if __name__ == "__main__":
    unittest.main()
