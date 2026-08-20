import unittest
from pathlib import Path
from config import BASE_DIR, FRONTEND_DIR, FRONTEND_PUBLIC_DIR, VEHICLE_IMAGES_DIR
from backend.scraper.sahibinden_scraper import SahibindenScraper

class TestArchitectureAndAssets(unittest.TestCase):
    def test_no_legacy_static_directory(self):
        """Root directory should not contain legacy static/ directory."""
        legacy_static = BASE_DIR / "static"
        self.assertFalse(legacy_static.exists(), "Legacy static/ folder should not exist in root.")

    def test_frontend_public_structure(self):
        """Frontend public directory should exist with vehicle_images and placeholder."""
        self.assertTrue(FRONTEND_PUBLIC_DIR.exists(), "frontend/public should exist.")
        self.assertTrue(VEHICLE_IMAGES_DIR.exists(), "frontend/public/vehicle_images should exist.")
        placeholder = FRONTEND_PUBLIC_DIR / "placeholder.svg"
        self.assertTrue(placeholder.exists(), "frontend/public/placeholder.svg should exist.")

    def test_scraper_image_urls_prefix(self):
        """Scraper should generate image paths starting with /vehicle_images/."""
        scraper = SahibindenScraper()
        self.assertEqual(scraper.images_dir, VEHICLE_IMAGES_DIR)
        
        # Test download & sync method URL generation logic with local cached image
        test_dir = VEHICLE_IMAGES_DIR / "SHBDN-TEST-1"
        test_dir.mkdir(parents=True, exist_ok=True)
        (test_dir / "image_0.jpg").write_bytes(b"dummy image content" * 100)

        dummy_urls = ["https://s3.eu-central-1.amazonaws.com/test.jpg"]
        local_urls = scraper._download_and_sync_images("SHBDN-TEST-1", dummy_urls)
        self.assertTrue(len(local_urls) > 0)
        self.assertTrue(local_urls[0].startswith("/vehicle_images/SHBDN-TEST-1/"))

        # Clean up test dir
        test_dir = VEHICLE_IMAGES_DIR / "SHBDN-TEST-1"
        if test_dir.exists():
            import shutil
            shutil.rmtree(test_dir)

if __name__ == "__main__":
    unittest.main()
