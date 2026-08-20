import unittest
from fastapi.testclient import TestClient
from backend.web.server import app
from backend.db.database import SessionLocal, init_db

class TestWebServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = TestClient(app)

    def test_root_serves_nextjs_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers.get("content-type", ""))

    def test_api_stats(self):
        response = self.client.get("/api/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total_vehicles", data)
        self.assertIn("total_briefs", data)
        self.assertIn("total_images", data)
        self.assertGreaterEqual(data["total_vehicles"], 5)

    def test_api_vehicles(self):
        response = self.client.get("/api/vehicles")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 5)
        
        first = data[0]
        self.assertIn("external_id", first)
        self.assertIn("brand", first)
        self.assertIn("primary_image_url", first)
        if first["primary_image_url"]:
            self.assertTrue(first["primary_image_url"].startswith("/vehicle_images/"))

    def test_api_brands(self):
        response = self.client.get("/api/brands")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertIn("Citroën", data)

    def test_vehicle_image_static_mount(self):
        # Verify that vehicle images are mounted and served at /vehicle_images
        response = self.client.get("/vehicle_images/SHBDN-1328660469/image_0.jpg")
        self.assertEqual(response.status_code, 200)
        self.assertIn("image/", response.headers.get("content-type", ""))

    def test_chat_endpoint(self):
        response = self.client.post("/api/chat", json={
            "message": "Merhaba, bütçem 2 milyon TL, SUV arıyorum",
            "session_id": "test_server_chat"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("reply", data)

    def test_chat_reset_endpoint(self):
        response = self.client.post("/api/chat/reset", json={
            "session_id": "test_server_chat"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("reply", data)

if __name__ == "__main__":
    unittest.main()
