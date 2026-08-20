import unittest
from backend.db.database import SessionLocal, init_db
from backend.db.models import CustomerLead
from backend.agent.chatbot_agent import ChatbotAgent

class TestVehicleOverviewConsultantFlow(unittest.TestCase):
    def setUp(self):
        init_db()
        self.db = SessionLocal()
        self.db.query(CustomerLead).filter(CustomerLead.session_id == "test_user_ceylan_flow").delete()
        self.db.commit()
        self.agent = ChatbotAgent(self.db)

    def tearDown(self):
        self.db.close()

    def test_ceylan_exact_conversation_flow(self):
        sid = "test_user_ceylan_flow"

        # Step 1: User introduces name
        r1 = self.agent.process_message("Merhaba ben Ceylan Kaya", session_id=sid)
        self.assertIn("Ceylan Hanım", r1["reply"])

        # Step 2: User asks for SUV
        r2 = self.agent.process_message("suv araç bakıyorum", session_id=sid)
        self.assertIn("Ceylan Hanım", r2["reply"])
        self.assertIn("Peugeot 3008", r2["reply"])
        self.assertIn("Citroën C5 Aircross", r2["reply"])

        # Step 3: User asks for information about Peugeot 3008
        r3 = self.agent.process_message("peugot 3008 hakkında bilgi alabilir miyim", session_id=sid)
        self.assertIn("Ceylan Hanım", r3["reply"])
        self.assertIn("Peugeot 3008", r3["reply"])
        # Should provide full details (not just a bullet search repeat)
        self.assertIn("Satış Fiyatı", r3["reply"])
        self.assertIn("Kilometre", r3["reply"])
        self.assertIn("Ekspertiz", r3["reply"])
        self.assertIn("Öne Çıkan Donanımlar", r3["reply"])
        self.assertIn("test sürüşü", r3["reply"])

        # Step 4: User asks for detailed explanation ("bilgi almak istiyorum işte detaylı anlatır mısın bana")
        r4 = self.agent.process_message("bilgi almak istiyorum işte detaylı anlatır mısın bana", session_id=sid)
        self.assertIn("Ceylan Hanım", r4["reply"])
        self.assertIn("Peugeot 3008", r4["reply"])
        self.assertIn("Satış Fiyatı", r4["reply"])
        # Must NOT be a generic greeting reset
        self.assertNotIn("Size nasıl yardımcı olabilirim? Arkas Spoticar portföyümüzdeki araçlarımızın donanım", r4["reply"])

        # Step 5: User asks about another vehicle ("Citroen C5 Aircross'u anlatır mısın")
        r5 = self.agent.process_message("Citroen C5 Aircross'u anlatır mısın", session_id=sid)
        self.assertIn("Ceylan Hanım", r5["reply"])
        self.assertIn("C5 Aircross", r5["reply"])
        self.assertIn("Satış Fiyatı", r5["reply"])

        # Step 6: User says "teşekkür ederim"
        r6 = self.agent.process_message("teşekkür ederim", session_id=sid)
        self.assertIn("Rica ederim Ceylan Hanım", r6["reply"])
        self.assertNotIn("Merhaba Ceylan Hanım! Size nasıl yardımcı olabilirim", r6["reply"])

if __name__ == "__main__":
    unittest.main()
