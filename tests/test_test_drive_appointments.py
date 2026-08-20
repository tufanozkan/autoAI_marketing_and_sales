import unittest
from backend.db.database import SessionLocal, init_db
from backend.db.models import Vehicle, CustomerLead, TestDrive
from backend.agent.chatbot_agent import ChatbotAgent
from fastapi.testclient import TestClient
from backend.web.server import app

class TestDriveAppointmentsTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = TestClient(app)

    def setUp(self):
        self.db = SessionLocal()
        self.db.query(TestDrive).delete()
        self.db.query(CustomerLead).filter(CustomerLead.session_id.like("test_td_%")).delete()
        self.db.commit()
        self.agent = ChatbotAgent(self.db)

    def tearDown(self):
        self.db.close()

    def test_01_end_to_end_test_drive_flow_with_phone_first(self):
        sid = "test_td_01"

        # Step 1: User identification with phone at the beginning
        r1 = self.agent.process_message("Merhaba ben Deniz Yılmaz, 05321234567", session_id=sid)
        self.assertIn("Deniz", r1["reply"])
        self.assertIn("05321234567", r1["reply"])

        # Step 2: User inquires about Peugeot 408
        r2 = self.agent.process_message("Peugeot 408 hakkında detaylı bilgi verir misin", session_id=sid)
        self.assertIn("Peugeot 408", r2["reply"])
        self.assertIn("Satış Fiyatı", r2["reply"])

        # Step 3: User requests test drive appointment
        r3 = self.agent.process_message("test randevusu hazırlayalım", session_id=sid)
        self.assertIn("Peugeot 408", r3["reply"])
        self.assertIn("gün ve saat", r3["reply"])

        # Step 4: User provides appointment date and time ("21.08.2026 - 14.00 saat olarak iyidir")
        r4 = self.agent.process_message("21.08.2026 - 14.00 saat olarak iyidir", session_id=sid)
        self.assertIn("Test sürüşü randevunuzu başarıyla oluşturdum", r4["reply"])
        self.assertIn("Peugeot 408", r4["reply"])
        self.assertIn("21 Ağustos 2026 - 14:00", r4["reply"])
        self.assertIn("Gaziemir Showroom", r4["reply"])
        self.assertIn("05321234567", r4["reply"])

        # Step 5: Verify database record in test_drives table
        td = self.db.query(TestDrive).first()
        self.assertIsNotNone(td)
        self.assertEqual(td.customer_phone, "05321234567")
        self.assertEqual(td.appointment_datetime_text, "21 Ağustos 2026 - 14:00")
        self.assertEqual(td.status, "CONFIRMED")
        self.assertIn("Gaziemir", td.showroom_location)
        self.assertEqual(td.vehicle.model, "408")

        # Step 6: Verify API endpoint GET /api/test-drives
        res = self.client.get(f"/api/test-drives?session_id={sid}")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["appointment_datetime_text"], "21 Ağustos 2026 - 14:00")
        self.assertIn("Peugeot 408", data[0]["vehicle_title"])

    def test_02_test_drive_flow_with_phone_mandatory_for_appointment(self):
        sid = "test_td_02"

        # Step 1: User asks for C5 Aircross without giving phone at the start
        r1 = self.agent.process_message("Merhaba ben Ceylan, C5 Aircross hakkında bilgi alabilir miyim", session_id=sid)
        self.assertIn("C5 Aircross", r1["reply"])

        # Step 2: User provides test drive date without phone -> Bot MUST ask for phone before confirming
        r2 = self.agent.process_message("Yarın saat 15:00 için test sürüşü randevusu alabilir miyim", session_id=sid)
        self.assertIn("C5 Aircross", r2["reply"])
        self.assertIn("15:00", r2["reply"])
        self.assertIn("telefon numaranızı", r2["reply"])

        # Verify DB record is NOT yet created (phone is mandatory!)
        td_count = self.db.query(TestDrive).count()
        self.assertEqual(td_count, 0)

        # Step 3: User provides phone number -> Bot confirms appointment and creates DB record
        r3 = self.agent.process_message("05559876543", session_id=sid)
        self.assertIn("05559876543", r3["reply"])
        self.assertIn("randevunuzu başarıyla oluşturdum", r3["reply"])
        self.assertIn("C5 Aircross", r3["reply"])

        # Verify DB record now created with status CONFIRMED
        td = self.db.query(TestDrive).first()
        self.assertIsNotNone(td)
        self.assertEqual(td.customer_phone, "05559876543")
        self.assertEqual(td.status, "CONFIRMED")
        self.assertEqual(td.vehicle.model, "C5 Aircross")

    def test_03_refusal_of_phone_cancels_test_drive_booking(self):
        sid = "test_td_03"

        # Step 1: User asks about Peugeot 3008 without giving phone
        r1 = self.agent.process_message("Merhaba ben Tugce, Peugeot 3008 hakkında bilgi almak istiyorum", session_id=sid)
        self.assertIn("Peugeot 3008", r1["reply"])

        # Step 2: User requests test drive
        r2 = self.agent.process_message("Yarın saat 14:00'e test sürüşü randevusu ayarlayalım", session_id=sid)
        self.assertIn("telefon numaranızı", r2["reply"])

        # Step 3: User explicitly refuses to give phone
        r3 = self.agent.process_message("Telefon numaramı vermek istemiyorum", session_id=sid)
        self.assertIn("iletişim numarası zorunludur", r3["reply"])
        self.assertIn("Gaziemir Showroom", r3["reply"])
        self.assertNotIn("Anlayışınız için teşekkür ederiz", r3["reply"])

        # Verify no test drive appointment was saved
        td_count = self.db.query(TestDrive).count()
        self.assertEqual(td_count, 0)

    def test_04_stats_and_leads_api(self):
        # Stats check
        res_stats = self.client.get("/api/stats")
        self.assertEqual(res_stats.status_code, 200)
        self.assertIn("total_test_drives", res_stats.json())

        # Leads check
        res_leads = self.client.get("/api/leads")
        self.assertEqual(res_leads.status_code, 200)
        self.assertIsInstance(res_leads.json(), list)

    def test_05_irem_exact_dialogue_flow_with_policy_explanation(self):
        sid = "test_td_irem_05"

        # Turn 1: User introduces name without phone and asks for test drive
        r1 = self.agent.process_message("Merhaba ben İrem, C5 Aircross için test sürüşü planlamak isterim", session_id=sid)
        self.assertIn("İrem", r1["reply"])
        self.assertIn("C5 Aircross", r1["reply"])
        self.assertIn("telefon numaranızı", r1["reply"])

        # Turn 2: User provides date & explicitly declines phone in the same turn
        r2 = self.agent.process_message("21 ağustos saat 15 olabilir, telefonumu paylaşmak istemiyorum", session_id=sid)
        self.assertIn("21 Ağustos", r2["reply"])
        self.assertIn("15:00", r2["reply"])
        self.assertIn("iletişim numarası zorunludur", r2["reply"])
        self.assertIn("Gaziemir Showroom", r2["reply"])
        self.assertNotIn("Anlayışınız için teşekkür ederiz", r2["reply"]) # No robotic cliché

        # Turn 3: User follows up asking why phone is needed / if they can visit showroom directly
        r3 = self.agent.process_message("illa telefon numaramı vermem mi lazım", session_id=sid)
        self.assertIn("telefon numarası zorunludur", r3["reply"])
        self.assertIn("Gaziemir Showroom", r3["reply"])
        self.assertNotIn("Merhaba İrem Hanım! Size nasıl yardımcı olabilirim", r3["reply"]) # No reset!

        # Turn 4: User asks alternative direct walk-in question
        r4 = self.agent.process_message("telefonumu vermeden direkt showrooma gelsem olur mu", session_id=sid)
        self.assertIn("Gaziemir Showroom", r4["reply"])
        self.assertIn("test sürüşü", r4["reply"])
        self.assertNotIn("Merhaba İrem Hanım! Size nasıl yardımcı olabilirim", r4["reply"])

        # Turn 5: User changes mind and gives phone
        r5 = self.agent.process_message("05339998877", session_id=sid)
        self.assertIn("05339998877", r5["reply"])

    def test_06_tufan_exact_dialogue_flow_with_agreement_and_booking(self):
        sid = "test_td_tufan_06"

        # Turn 1: User asks about sunroof on C5 Aircross
        r1 = self.agent.process_message("Merhaba ben Tufan, C5 Aircross'ta cam tavan var mı?", session_id=sid)
        self.assertIn("Tufan", r1["reply"])
        self.assertIn("Cam Tavan", r1["reply"])

        # Turn 2: User requests test drive
        r2 = self.agent.process_message("test sürüşü planlayabilir miyiz", session_id=sid)
        self.assertIn("C5 Aircross", r2["reply"])
        self.assertIn("gün ve saat", r2["reply"])

        # Turn 3: User provides date and declines phone initially
        r3 = self.agent.process_message("21.08.2026 saat 14.00, telefonumu paylaşmak istemiyorum", session_id=sid)
        self.assertIn("21 Ağustos 2026 - 14:00", r3["reply"])
        self.assertIn("iletişim numarası zorunludur", r3["reply"])
        self.assertIn("Gaziemir Showroom", r3["reply"])
        self.assertNotIn("Anlayışınız için teşekkür ederiz", r3["reply"])

        # Verify DB record is NOT yet created
        self.assertEqual(self.db.query(TestDrive).count(), 0)

        # Turn 4: User changes their mind and agrees to share phone
        r4 = self.agent.process_message("tamam paylaşayım o zaman telefon numaramı", session_id=sid)
        self.assertIn("C5 Aircross", r4["reply"])
        self.assertIn("21 Ağustos 2026 - 14:00", r4["reply"])
        self.assertIn("telefon numaranızı", r4["reply"])
        self.assertNotIn("Merhaba Tufan Bey! Size nasıl yardımcı olabilirim", r4["reply"]) # No reset!

        # Turn 5: User enters phone number
        r5 = self.agent.process_message("05321112233", session_id=sid)
        self.assertIn("test sürüşü randevunuzu başarıyla oluşturdum", r5["reply"])
        self.assertIn("C5 Aircross", r5["reply"])
        self.assertIn("21 Ağustos 2026 - 14:00", r5["reply"])
        self.assertIn("05321112233", r5["reply"])
        self.assertIn("Gaziemir Showroom", r5["reply"])

        # Verify DB record is now created with status CONFIRMED and correct vehicle & phone
        td = self.db.query(TestDrive).first()
        self.assertIsNotNone(td)
        self.assertEqual(td.customer_phone, "05321112233")
        self.assertEqual(td.appointment_datetime_text, "21 Ağustos 2026 - 14:00")
        self.assertEqual(td.status, "CONFIRMED")
        self.assertEqual(td.vehicle.model, "C5 Aircross")

    def test_07_saying_olur_after_vehicle_overview_triggers_test_drive_flow(self):
        sid = "test_td_olur_07"

        # Turn 1: User asks for comprehensive overview of Citroën C5 Aircross
        r1 = self.agent.process_message("Merhaba ben Tufan, C5 Aircross hakkında detaylı bilgi alabilir miyim", session_id=sid)
        self.assertIn("Tufan", r1["reply"])
        self.assertIn("Citroën C5 Aircross", r1["reply"])
        self.assertIn("test sürüşü randevusu", r1["reply"])

        # Turn 2: User responds simply with "olur"
        r2 = self.agent.process_message("olur", session_id=sid)
        self.assertIn("C5 Aircross", r2["reply"])
        self.assertIn("test sürüşü", r2["reply"])
        self.assertIn("gün ve saat", r2["reply"])
        self.assertNotIn("kriterlerinize en uygun güncel", r2["reply"]) # Did NOT fall back to catalog search!

        # Turn 3: User provides date and phone
        r3 = self.agent.process_message("21.08.2026 saat 14:00, 05321112233", session_id=sid)
        self.assertIn("Test sürüşü randevunuzu başarıyla oluşturdum", r3["reply"])
        self.assertIn("C5 Aircross", r3["reply"])
        self.assertIn("21 Ağustos 2026 - 14:00", r3["reply"])

        # Verify DB
        td = self.db.query(TestDrive).first()
        self.assertIsNotNone(td)
        self.assertEqual(td.customer_phone, "05321112233")
        self.assertEqual(td.vehicle.model, "C5 Aircross")

if __name__ == "__main__":
    unittest.main()
