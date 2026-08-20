import unittest
from backend.db.database import SessionLocal, init_db
from backend.db.models import CustomerLead
from backend.agent.chatbot_agent import ChatbotAgent

class TestGratitudeAndChatFlow(unittest.TestCase):
    def setUp(self):
        init_db()
        self.db = SessionLocal()
        self.db.query(CustomerLead).filter(CustomerLead.session_id == "test_user_scenario_tugce").delete()
        self.db.commit()
        self.agent = ChatbotAgent(self.db)

    def tearDown(self):
        self.db.close()

    def test_user_reported_flow(self):
        sid = "test_user_scenario_tugce"

        # Step 1: User introduces name and phone
        r1 = self.agent.process_message("Merhaba Tugce Hazir, 05678931456", session_id=sid)
        self.assertIn("Tugce Hanım", r1["reply"])
        self.assertIn("05678931456", r1["reply"])

        # Step 2: User asks for 1.5M TL altı araçlar
        r2 = self.agent.process_message("1.5M TL altı araçlar", session_id=sid)
        self.assertIn("Tugce Hanım", r2["reply"])
        self.assertIn("Fiat Egea", r2["reply"])
        self.assertIn("Honda City", r2["reply"])
        # Verify that "Sayfayı filtreledim" is NOT in the reply
        self.assertNotIn("Sayfayı filtreledim", r2["reply"])
        self.assertNotIn("sayfayı yeniledim", r2["reply"])
        self.assertNotIn("sayfayı filtreledim", r2["reply"])

        # Step 3: Question about seat heating
        r3 = self.agent.process_message("koltuk ısıtma var mı bu iki araçtada", session_id=sid)
        self.assertIn("Koltuk Isıtma", r3["reply"])
        self.assertIn("Fiat Egea", r3["reply"])

        # Step 4: User says "teşekkür ederim"
        r4 = self.agent.process_message("teşekkür ederim", session_id=sid)
        # Must acknowledge thanks and close politely
        self.assertIn("Rica ederim Tugce Hanım", r4["reply"])
        self.assertNotIn("Merhaba Tugce Hanım! Size nasıl yardımcı olabilirim", r4["reply"])

        # Step 5: User says "çok teşekkürler iyi günler"
        r5 = self.agent.process_message("çok teşekkürler iyi günler", session_id=sid)
        self.assertIn("Tugce Hanım", r5["reply"])
        self.assertIn("İyi günler", r5["reply"])

if __name__ == "__main__":
    unittest.main()
