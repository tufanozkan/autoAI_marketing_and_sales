import os
import io
import logging
import requests
from typing import Optional, List, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from sqlalchemy.orm import Session
from config import settings, POSTERS_DIR
from src.db.models import Vehicle, Poster
from .brand_rules import BrandRules

logger = logging.getLogger(__name__)

class PosterEngine:
    """
    Renders high-quality automotive marketing posters (Instagram 4:5 & Web Banners)
    using Pillow with modern typography, gradients, badges, and brand palettes.
    """

    def __init__(self, db: Session):
        self.db = db

    def _get_font(self, size: int, bold: bool = False) -> ImageFont.ImageFont:
        """Loads available system fonts with safe fallbacks."""
        font_paths = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/SFNSText.ttf",
            "/Library/Fonts/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ]
        for p in font_paths:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size=size)
                except Exception:
                    continue
        try:
            return ImageFont.load_default()
        except Exception:
            return None

    def _download_or_load_image(self, url: str) -> Optional[Image.Image]:
        """Downloads remote car image or creates an elegant placeholder."""
        if url and url.startswith("http"):
            try:
                resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                if resp.status_code == 200:
                    img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
                    return img
            except Exception as e:
                logger.warning(f"Could not download car image ({e}), using synthetic studio visual.")
        
        # Fallback synthetic clean gradient car canvas
        img = Image.new("RGBA", (800, 500), (20, 30, 45, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(20, 20), (780, 480)], outline=(227, 6, 19, 150), width=3)
        draw.text((250, 230), "ARKAS 2. EL GÖRSELİ", fill=(255, 255, 255, 200))
        return img

    def _create_gradient_bg(self, width: int, height: int, primary_hex: str = "#E30613") -> Image.Image:
        """Creates a modern luxury dark gradient background."""
        base = Image.new("RGB", (width, height), (15, 23, 42))  # Slate 900
        draw = ImageDraw.Draw(base)
        
        # Draw radial ambient light at top-right
        for r in range(400, 0, -20):
            alpha = int(35 * (1 - r / 400))
            draw.ellipse(
                [(width - 150 - r, 100 - r), (width - 150 + r, 100 + r)],
                fill=(30 + alpha, 41 + alpha, 59 + alpha)
            )
            
        # Draw bottom subtle glow
        draw.rectangle([(0, height - 260), (width, height)], fill=(11, 15, 26))
        return base

    def generate_instagram_poster(self, vehicle: Vehicle) -> str:
        """Generates 1080x1350 4:5 Instagram Portrait Poster."""
        W, H = settings.POSTER_WIDTH, settings.POSTER_HEIGHT
        brand_cfg = BrandRules.get_brand_config(vehicle.brand)
        
        canvas = self._create_gradient_bg(W, H, brand_cfg.get("accent_color", "#E30613"))
        draw = ImageDraw.Draw(canvas)

        font_header_tag = self._get_font(28, bold=True)
        font_brand = self._get_font(36, bold=True)
        font_title = self._get_font(52, bold=True)
        font_sub = self._get_font(30, bold=False)
        font_spec = self._get_font(26, bold=True)
        font_price = self._get_font(58, bold=True)
        font_cta = self._get_font(24, bold=True)
        font_feature = self._get_font(24, bold=False)

        # 1. Top Bar: Arkas 2. El Brand Pill
        pill_x1, pill_y1, pill_x2, pill_y2 = 50, 50, 480, 110
        draw.rounded_rectangle([(pill_x1, pill_y1), (pill_x2, pill_y2)], radius=25, fill=(227, 6, 19)) # Arkas Red
        draw.text((pill_x1 + 30, pill_y1 + 17), "ARKAS 2. EL GUVENCESİYLE", fill=(255, 255, 255), font=font_header_tag)

        # Year badge
        draw.rounded_rectangle([(W - 250, 50), (W - 50, 110)], radius=25, fill=(30, 41, 59), outline=(227, 6, 19), width=2)
        draw.text((W - 220, 67), f"{vehicle.year} MODEL", fill=(255, 255, 255), font=font_header_tag)

        # 2. Main Car Image Box
        car_img = self._download_or_load_image(vehicle.primary_image_url)
        target_img_w = W - 100
        target_img_h = 580
        car_img_resized = car_img.resize((target_img_w, target_img_h), Image.Resampling.LANCZOS)
        
        # Rounded mask for car image
        mask = Image.new("L", (target_img_w, target_img_h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (target_img_w, target_img_h)], radius=30, fill=255)
        
        # Border card behind image
        draw.rounded_rectangle([(46, 136), (W - 46, 144 + target_img_h)], radius=32, fill=(255, 255, 255, 20), outline=(227, 6, 19, 100), width=3)
        canvas.paste(car_img_resized.convert("RGB"), (50, 140), mask=mask)

        # Segment tag over image
        draw.rounded_rectangle([(70, 160), (320, 205)], radius=15, fill=(15, 23, 42, 220))
        draw.text((85, 172), f"• {vehicle.body_type or 'Otomobil'}", fill=(255, 255, 255), font=font_cta)

        # 3. Vehicle Typography Details
        content_top = 750
        draw.text((50, content_top), vehicle.brand.upper(), fill=(227, 6, 19), font=font_brand)
        
        model_full = f"{vehicle.model} {vehicle.sub_model or ''}"
        if len(model_full) > 28:
            model_full = model_full[:26] + "..."
        draw.text((50, content_top + 45), model_full, fill=(255, 255, 255), font=font_title)

        # Specs Badges (KM, Fuel, Transmission)
        badge_y = content_top + 120
        km_str = f"{vehicle.km:,.0f} KM".replace(",", ".")
        fuel_str = f"{vehicle.fuel_type or 'Benzin'}"
        trans_str = f"{vehicle.transmission or 'Otomatik'}"

        badges = [km_str, fuel_str, trans_str]
        cur_x = 50
        for b in badges:
            b_len = len(b) * 15 + 34
            draw.rounded_rectangle([(cur_x, badge_y), (cur_x + b_len, badge_y + 45)], radius=12, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
            draw.text((cur_x + 16, badge_y + 10), b, fill=(241, 245, 249), font=font_spec)
            cur_x += b_len + 15

        # 4. Feature Highlights (Top 3 features)
        feat_y = badge_y + 65
        draw.text((50, feat_y), "ONE CIKAN DONANIMLAR", fill=(148, 163, 184), font=font_cta)
        
        features_to_show = vehicle.features[:3] if vehicle.features else ["Ekspertiz Garantili", "Yetkili Servis Bakimli", "Geri Gorus Kamerasi"]
        for idx, feat in enumerate(features_to_show):
            item_y = feat_y + 35 + (idx * 35)
            draw.text((60, item_y), f"•  {feat}", fill=(226, 232, 240), font=font_feature)

        # 5. Bottom Price & CTA Footer Card
        footer_y1 = H - 180
        draw.rounded_rectangle([(50, footer_y1), (W - 50, H - 40)], radius=24, fill=(227, 6, 19)) # Arkas Red
        
        price_text = f"{vehicle.price:,.0f} {vehicle.currency}".replace(",", ".")
        draw.text((80, footer_y1 + 25), price_text, fill=(255, 255, 255), font=font_price)
        draw.text((80, footer_y1 + 95), "Detaylar & Randevu Icin Hemen Iletisime Gecin", fill=(255, 230, 230), font=font_cta)

        # Right CTA Button on footer
        btn_w = 240
        draw.rounded_rectangle([(W - 50 - btn_w - 30, footer_y1 + 35), (W - 80, footer_y1 + 105)], radius=15, fill=(255, 255, 255))
        draw.text((W - 50 - btn_w + 10, footer_y1 + 55), "INCELE & AL >", fill=(227, 6, 19), font=font_cta)

        # Save output
        filename = f"poster_{vehicle.id}_post.png"
        output_path = POSTERS_DIR / filename
        canvas.save(output_path, "PNG", quality=95)
        
        file_url = f"/static/generated_posters/{filename}"
        return file_url

    def generate_banner(self, vehicle: Vehicle) -> str:
        """Generates 1200x630 Web/Social Landscape Banner."""
        W, H = settings.BANNER_WIDTH, settings.BANNER_HEIGHT
        brand_cfg = BrandRules.get_brand_config(vehicle.brand)
        
        canvas = self._create_gradient_bg(W, H, brand_cfg.get("accent_color", "#E30613"))
        draw = ImageDraw.Draw(canvas)

        font_header_tag = self._get_font(24, bold=True)
        font_brand = self._get_font(30, bold=True)
        font_title = self._get_font(42, bold=True)
        font_spec = self._get_font(22, bold=True)
        font_price = self._get_font(46, bold=True)
        font_cta = self._get_font(20, bold=True)

        # Left Column: Information (Width: 620px)
        # 1. Header Pill
        draw.rounded_rectangle([(50, 40), (420, 85)], radius=20, fill=(227, 6, 19))
        draw.text((70, 52), "ARKAS 2. EL GUVENCESİYLE", fill=(255, 255, 255), font=font_header_tag)

        # 2. Titles
        draw.text((50, 110), vehicle.brand.upper(), fill=(227, 6, 19), font=font_brand)
        model_str = f"{vehicle.model} {vehicle.sub_model or ''}"
        if len(model_str) > 24:
            model_str = model_str[:22] + "..."
        draw.text((50, 150), model_str, fill=(255, 255, 255), font=font_title)

        # 3. Badges
        km_str = f"{vehicle.km:,.0f} KM".replace(",", ".")
        badges = [f"{vehicle.year} MODEL", km_str, vehicle.fuel_type or "Benzin"]
        cur_x = 50
        for b in badges:
            b_len = len(b) * 12 + 25
            draw.rounded_rectangle([(cur_x, 220), (cur_x + b_len, 260)], radius=10, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
            draw.text((cur_x + 12, 230), b, fill=(241, 245, 249), font=font_spec)
            cur_x += b_len + 12

        # 4. Features
        features_to_show = vehicle.features[:2] if vehicle.features else ["Ekspertiz Garantili", "Kusursuz Bakimli"]
        for idx, feat in enumerate(features_to_show):
            draw.text((50, 285 + idx * 30), f"• {feat}", fill=(203, 213, 225), font=font_cta)

        # 5. Price & CTA
        price_text = f"{vehicle.price:,.0f} {vehicle.currency}".replace(",", ".")
        draw.text((50, 370), price_text, fill=(255, 255, 255), font=font_price)
        
        draw.rounded_rectangle([(50, 440), (280, 500)], radius=15, fill=(227, 6, 19))
        draw.text((75, 460), "HEMEN INCELE >", fill=(255, 255, 255), font=font_cta)

        # Right Column: Car Image (Width: 480px, Height: 480px)
        car_img = self._download_or_load_image(vehicle.primary_image_url)
        target_w, target_h = 500, 460
        car_img_resized = car_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        mask = Image.new("L", (target_w, target_h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (target_w, target_h)], radius=25, fill=255)
        
        draw.rounded_rectangle([(650, 40), (650 + target_w, 40 + target_h)], radius=27, fill=(255, 255, 255, 20), outline=(227, 6, 19, 100), width=2)
        canvas.paste(car_img_resized.convert("RGB"), (650, 40), mask=mask)

        # Save output
        filename = f"poster_{vehicle.id}_banner.png"
        output_path = POSTERS_DIR / filename
        canvas.save(output_path, "PNG", quality=95)
        
        file_url = f"/static/generated_posters/{filename}"
        return file_url

    def generate_all_posters_for_vehicle(self, vehicle: Vehicle) -> List[Poster]:
        """Generates both Instagram Post & Banner posters and saves into database."""
        # Clean existing posters
        self.db.query(Poster).filter(Poster.vehicle_id == vehicle.id).delete()
        self.db.flush()

        post_url = self.generate_instagram_poster(vehicle)
        banner_url = self.generate_banner(vehicle)

        p1 = Poster(
            vehicle_id=vehicle.id,
            poster_type="instagram_post",
            file_path=str(POSTERS_DIR / f"poster_{vehicle.id}_post.png"),
            file_url=post_url,
            title=f"{vehicle.brand} {vehicle.model} - Instagram Afişi",
            badge_text="ARKAS 2. EL",
            theme_color="#E30613"
        )
        p2 = Poster(
            vehicle_id=vehicle.id,
            poster_type="banner",
            file_path=str(POSTERS_DIR / f"poster_{vehicle.id}_banner.png"),
            file_url=banner_url,
            title=f"{vehicle.brand} {vehicle.model} - Web Banner",
            badge_text="ARKAS 2. EL",
            theme_color="#E30613"
        )
        self.db.add(p1)
        self.db.add(p2)
        self.db.commit()

        return [p1, p2]

    def render_all_pending(self, limit: int = 50) -> int:
        """Renders posters for all active vehicles."""
        vehicles = self.db.query(Vehicle).filter(Vehicle.is_active == True).limit(limit).all()
        count = 0
        for v in vehicles:
            try:
                self.generate_all_posters_for_vehicle(v)
                count += 1
            except Exception as e:
                logger.error(f"Error rendering poster for vehicle {v.id}: {e}")
        return count
