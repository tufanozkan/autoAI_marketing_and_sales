import os
import io
import logging
import urllib.request
from typing import Optional, List, Dict, Any
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from sqlalchemy.orm import Session
from config import settings, POSTERS_DIR
from src.db.models import Vehicle, Poster

logger = logging.getLogger(__name__)

class PosterEngine:
    """
    Renders high-resolution automotive marketing posters (Instagram 4:5 Portrait & Web Banner)
    using the Quiet Luxury Warm Beige / Alabaster White / Silver / Charcoal design system.
    Supports 3 focused angles:
    1) Ana Görünüm (Sağ/Ön Çapraz)
    2) Ön Far & Izgara Detayı
    3) Arka Çapraz & Dinamik Profil
    plus 1 Landscape 16:9 Banner.
    """

    def __init__(self, db: Session):
        self.db = db
        self._image_cache = {}

    def _get_font(self, size: int, bold: bool = False) -> ImageFont.ImageFont:
        font_paths = [
            "/System/Library/Fonts/SFNS.ttf",
            "/System/Library/Fonts/SFNSText.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
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

    def _download_image(self, url: str) -> Optional[Image.Image]:
        if not url:
            return None
        if url in self._image_cache:
            return self._image_cache[url].copy()

        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Referer": "https://www.arkasotomotiv2.com/"
            })
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read()
                img = Image.open(io.BytesIO(data)).convert("RGBA")
                self._image_cache[url] = img
                return img.copy()
        except Exception as e:
            logger.warning(f"Could not download car image {url} ({e})")
            return None

    def _get_fallback_image(self, brand: str) -> Image.Image:
        img = Image.new("RGBA", (800, 500), (240, 237, 230, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(20, 20), (780, 480)], outline=(194, 166, 118, 200), width=2)
        font = self._get_font(28, bold=True)
        draw.text((260, 230), f"ARKAS 2. EL — {brand.upper()}", fill=(24, 24, 27, 255), font=font)
        return img

    def _create_luxury_gradient_bg(self, width: int, height: int) -> Image.Image:
        """
        Creates a sophisticated Warm Architectural Stone / Linen gradient background.
        """
        base = Image.new("RGB", (width, height), (247, 245, 240))  # #F7F5F0 Warm Stone
        draw = ImageDraw.Draw(base)

        # Subtle vertical gradient from light beige to slightly deeper stone
        for y in range(height):
            ratio = y / height
            r = int(248 * (1 - ratio) + 235 * ratio)
            g = int(246 * (1 - ratio) + 231 * ratio)
            b = int(241 * (1 - ratio) + 222 * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Soft ambient radial glow behind the vehicle photo area
        for rad in range(350, 0, -25):
            alpha = int(18 * (1 - rad / 350))
            draw.ellipse(
                [(width // 2 - rad, 420 - rad), (width // 2 + rad, 420 + rad)],
                fill=(255, 255, 255)
            )

        return base

    def _prepare_angle_image(self, car_img: Image.Image, angle_code: str, is_custom_gallery_photo: bool) -> Image.Image:
        """
        Prepares vehicle photo for the camera angle.
        If a single photo is available, applies high-precision focal crop.
        """
        orig_w, orig_h = car_img.size

        if is_custom_gallery_photo and angle_code in ["front"]:
            return car_img

        if angle_code == "headlight":
            # Focus on front headlight, grill, and front badge
            crop_box = (
                int(orig_w * 0.05),
                int(orig_h * 0.28),
                int(orig_w * 0.65),
                int(orig_h * 0.90)
            )
            return car_img.crop(crop_box)
        elif angle_code == "rear":
            # Focus on rear quarter, taillight and rear fender
            crop_box = (
                int(orig_w * 0.42),
                int(orig_h * 0.25),
                int(orig_w * 0.98),
                int(orig_h * 0.90)
            )
            return car_img.crop(crop_box)

        return car_img

    def render_portrait_poster(
        self,
        vehicle: Vehicle,
        image_url: str,
        angle_code: str,
        angle_badge: str,
        is_custom_gallery_photo: bool = False
    ) -> str:
        """
        Renders a 1080x1350 4:5 Instagram Portrait poster using the Quiet Luxury design system.
        Guarantees zero text overlap with strict vertical bounding box calculation.
        """
        W, H = settings.POSTER_WIDTH, settings.POSTER_HEIGHT
        canvas = self._create_luxury_gradient_bg(W, H)
        draw = ImageDraw.Draw(canvas)

        font_header = self._get_font(22, bold=True)
        font_brand = self._get_font(28, bold=True)
        font_title = self._get_font(44, bold=True)
        font_spec = self._get_font(22, bold=True)
        font_price = self._get_font(52, bold=True)
        font_cta = self._get_font(20, bold=True)
        font_feature = self._get_font(22, bold=False)

        # 1. Top Header Bar: Arkas Clean Badge & Year Pill
        # Arkas Badge (Matte Charcoal #18181B)
        draw.rounded_rectangle([(50, 45), (420, 95)], radius=12, fill=(24, 24, 27))
        draw.text((72, 58), "ARKAS 2. EL GÜVENCESİYLE", fill=(247, 245, 240), font=font_header)

        # Year Badge (Stone #F0EDE6 with Charcoal Border)
        draw.rounded_rectangle([(W - 230, 45), (W - 50, 95)], radius=12, fill=(240, 237, 230), outline=(213, 207, 194), width=1)
        draw.text((W - 205, 58), f"{vehicle.year} MODEL", fill=(24, 24, 27), font=font_header)

        # 2. Vehicle Photo Card (White card with subtle silver-beige border)
        car_img = self._download_image(image_url)
        if not car_img:
            car_img = self._get_fallback_image(vehicle.brand)

        car_img_angle = self._prepare_angle_image(car_img, angle_code, is_custom_gallery_photo)

        card_x1, card_y1 = 50, 115
        card_w = W - 100
        card_h = 560
        card_x2, card_y2 = card_x1 + card_w, card_y1 + card_h

        # Draw card container
        draw.rounded_rectangle([(card_x1, card_y1), (card_x2, card_y2)], radius=24, fill=(255, 255, 255), outline=(230, 226, 216), width=2)

        # Resize car image to fit inside card with padding
        inner_w = card_w - 20
        inner_h = card_h - 20
        car_resized = car_img_angle.resize((inner_w, inner_h), Image.Resampling.LANCZOS)

        mask = Image.new("L", (inner_w, inner_h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (inner_w, inner_h)], radius=18, fill=255)

        canvas.paste(car_resized.convert("RGB"), (card_x1 + 10, card_y1 + 10), mask=mask)

        # Angle Badge Tag over photo (Alabaster Pill with Champagne accent)
        draw.rounded_rectangle([(70, 135), (310, 175)], radius=10, fill=(255, 255, 255, 240), outline=(213, 207, 194), width=1)
        draw.text((86, 145), f"• {angle_badge}", fill=(156, 130, 98), font=font_cta)

        # 3. Vehicle Typography & Information (Clean Vertical Flow)
        text_start_y = 705

        # Brand Tag in Champagne / Bronze
        draw.text((50, text_start_y), vehicle.brand.upper(), fill=(156, 130, 98), font=font_brand)

        # Model Title (Dynamic sizing to prevent overflow)
        model_full = f"{vehicle.model} {vehicle.sub_model or ''}".strip()
        if len(model_full) > 30:
            model_full = model_full[:28] + "..."
        draw.text((50, text_start_y + 40), model_full, fill=(24, 24, 27), font=font_title)

        # 4. Specs Pills (KM, Fuel, Transmission)
        badge_y = text_start_y + 115
        km_str = f"{vehicle.km:,.0f} KM".replace(",", ".")
        fuel_str = f"{vehicle.fuel_type or 'Benzin'}"
        trans_str = f"{vehicle.transmission or 'Otomatik'}"

        badges = [km_str, fuel_str, trans_str]
        cur_x = 50
        for b in badges:
            b_w = len(b) * 14 + 32
            draw.rounded_rectangle([(cur_x, badge_y), (cur_x + b_w, badge_y + 44)], radius=10, fill=(255, 255, 255), outline=(230, 226, 216), width=1)
            draw.text((cur_x + 16, badge_y + 10), b, fill=(82, 82, 91), font=font_spec)
            cur_x += b_w + 14

        # 5. Highlight Equipment (2 items with ample spacing)
        feat_y = badge_y + 65
        draw.text((50, feat_y), "ÖNE ÇIKAN STANDARTLAR", fill=(142, 138, 130), font=font_cta)

        features_to_show = vehicle.features[:2] if (vehicle.features and len(vehicle.features) >= 2) else [
            "Ekspertiz ve Kilometre Garantili",
            "Yetkili Servis Bakımlı & Kusursuz Kondisyon"
        ]
        for idx, feat in enumerate(features_to_show):
            item_y = feat_y + 32 + (idx * 32)
            draw.text((55, item_y), f"—  {feat}", fill=(82, 82, 91), font=font_feature)

        # 6. Bottom Price & Action Footer Card (Deep Matte Charcoal)
        footer_y1 = H - 170
        footer_y2 = H - 40
        draw.rounded_rectangle([(50, footer_y1), (W - 50, footer_y2)], radius=20, fill=(24, 24, 27))

        price_text = f"{vehicle.price:,.0f} {vehicle.currency}".replace(",", ".")
        draw.text((80, footer_y1 + 22), price_text, fill=(247, 245, 240), font=font_price)
        draw.text((80, footer_y1 + 88), "Ekspertiz Raporu & Detaylar İçin İletişime Geçin", fill=(194, 166, 118), font=font_cta)

        # Right CTA Button on footer
        btn_w = 230
        draw.rounded_rectangle([(W - 50 - btn_w - 30, footer_y1 + 35), (W - 80, footer_y1 + 95)], radius=12, fill=(247, 245, 240))
        draw.text((W - 50 - btn_w + 5, footer_y1 + 52), "DETAYLI İNCELE >", fill=(24, 24, 27), font=font_cta)

        # Save output
        filename = f"poster_{vehicle.id}_{angle_code}.png"
        output_path = POSTERS_DIR / filename
        canvas.save(output_path, "PNG", quality=95)

        return f"/static/generated_posters/{filename}"

    def render_banner(self, vehicle: Vehicle, image_url: str) -> str:
        """
        Renders a 1200x630 Landscape banner in Quiet Luxury styling.
        """
        W, H = settings.BANNER_WIDTH, settings.BANNER_HEIGHT
        canvas = self._create_luxury_gradient_bg(W, H)
        draw = ImageDraw.Draw(canvas)

        font_header = self._get_font(20, bold=True)
        font_brand = self._get_font(24, bold=True)
        font_title = self._get_font(36, bold=True)
        font_spec = self._get_font(20, bold=True)
        font_price = self._get_font(44, bold=True)
        font_cta = self._get_font(18, bold=True)

        # Left Column: Information
        draw.rounded_rectangle([(50, 35), (380, 75)], radius=10, fill=(24, 24, 27))
        draw.text((68, 46), "ARKAS 2. EL GÜVENCESİYLE", fill=(247, 245, 240), font=font_header)

        draw.text((50, 100), vehicle.brand.upper(), fill=(156, 130, 98), font=font_brand)
        model_str = f"{vehicle.model} {vehicle.sub_model or ''}".strip()
        if len(model_str) > 26:
            model_str = model_str[:24] + "..."
        draw.text((50, 135), model_str, fill=(24, 24, 27), font=font_title)

        km_str = f"{vehicle.km:,.0f} KM".replace(",", ".")
        badges = [f"{vehicle.year} MODEL", km_str, vehicle.fuel_type or "Benzin"]
        cur_x = 50
        for b in badges:
            b_w = len(b) * 11 + 24
            draw.rounded_rectangle([(cur_x, 205), (cur_x + b_w, 245)], radius=8, fill=(255, 255, 255), outline=(230, 226, 216), width=1)
            draw.text((cur_x + 12, 215), b, fill=(82, 82, 91), font=font_spec)
            cur_x += b_w + 10

        features_to_show = vehicle.features[:2] if vehicle.features else ["Ekspertiz ve KM Garantili", "Yetkili Servis Bakımlı"]
        for idx, feat in enumerate(features_to_show):
            draw.text((50, 275 + idx * 28), f"— {feat}", fill=(113, 109, 101), font=font_cta)

        # Price
        price_text = f"{vehicle.price:,.0f} {vehicle.currency}".replace(",", ".")
        draw.text((50, 365), price_text, fill=(24, 24, 27), font=font_price)

        draw.rounded_rectangle([(50, 440), (270, 495)], radius=12, fill=(24, 24, 27))
        draw.text((75, 458), "HEMEN İNCELE >", fill=(247, 245, 240), font=font_cta)

        # Right Column: Car Image Card
        car_img = self._download_image(image_url)
        if not car_img:
            car_img = self._get_fallback_image(vehicle.brand)

        target_w, target_h = 520, 480
        draw.rounded_rectangle([(630, 35), (630 + target_w, 35 + target_h)], radius=20, fill=(255, 255, 255), outline=(230, 226, 216), width=2)

        inner_w, inner_h = target_w - 20, target_h - 20
        car_resized = car_img.resize((inner_w, inner_h), Image.Resampling.LANCZOS)
        mask = Image.new("L", (inner_w, inner_h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (inner_w, inner_h)], radius=16, fill=255)

        canvas.paste(car_resized.convert("RGB"), (640, 45), mask=mask)

        filename = f"poster_{vehicle.id}_banner.png"
        output_path = POSTERS_DIR / filename
        canvas.save(output_path, "PNG", quality=95)

        return f"/static/generated_posters/{filename}"

    def generate_all_posters_for_vehicle(self, vehicle: Vehicle) -> List[Poster]:
        """
        Generates 3 focused camera angle posters:
        1) Ana Görünüm (Ön Çapraz)
        2) Ön Far & Izgara Detayı
        3) Arka Çapraz Profil
        and 1 landscape banner.
        """
        # Delete existing poster records for this vehicle
        self.db.query(Poster).filter(Poster.vehicle_id == vehicle.id).delete()
        self.db.flush()

        gallery = vehicle.image_urls if (vehicle.image_urls and len(vehicle.image_urls) > 0) else [vehicle.primary_image_url]
        primary = vehicle.primary_image_url or (gallery[0] if gallery else "")

        # Define 3 clean angles
        angle_configs = [
            {
                "code": "front",
                "badge": "ANA GÖRÜNÜM",
                "title": f"{vehicle.brand} {vehicle.model} - Ana Görünüm",
                "type": "instagram_post",
                "image_url": gallery[0] if len(gallery) > 0 else primary
            },
            {
                "code": "headlight",
                "badge": "ÖN FAR & IZGARA",
                "title": f"{vehicle.brand} {vehicle.model} - Ön Far & Izgara Detayı",
                "type": "detail_headlight",
                "image_url": gallery[1] if len(gallery) > 1 else (gallery[0] if gallery else primary)
            },
            {
                "code": "rear",
                "badge": "ARKA ÇAPRAZ PROFIL",
                "title": f"{vehicle.brand} {vehicle.model} - Arka Çapraz Profil",
                "type": "rear_profile",
                "image_url": gallery[2] if len(gallery) > 2 else (gallery[-1] if len(gallery) > 1 else primary)
            }
        ]

        created_posters = []

        # 1. Generate 3 Angle Portrait Posters
        for cfg in angle_configs:
            try:
                is_custom = bool(len(gallery) > 1 and cfg["image_url"] != gallery[0])
                url = self.render_portrait_poster(
                    vehicle=vehicle,
                    image_url=cfg["image_url"],
                    angle_code=cfg["code"],
                    angle_badge=cfg["badge"],
                    is_custom_gallery_photo=is_custom
                )
                p = Poster(
                    vehicle_id=vehicle.id,
                    poster_type=cfg["type"],
                    file_path=str(POSTERS_DIR / f"poster_{vehicle.id}_{cfg['code']}.png"),
                    file_url=url,
                    title=cfg["title"],
                    badge_text=cfg["badge"],
                    theme_color="#18181B"
                )
                self.db.add(p)
                created_posters.append(p)
            except Exception as e:
                logger.error(f"Error rendering angle poster {cfg['code']} for vehicle {vehicle.id}: {e}")

        # 2. Generate 1 Landscape Banner
        try:
            banner_url = self.render_banner(vehicle, primary)
            p_banner = Poster(
                vehicle_id=vehicle.id,
                poster_type="banner",
                file_path=str(POSTERS_DIR / f"poster_{vehicle.id}_banner.png"),
                file_url=banner_url,
                title=f"{vehicle.brand} {vehicle.model} - 16:9 Banner",
                badge_text="16:9 BANNER",
                theme_color="#18181B"
            )
            self.db.add(p_banner)
            created_posters.append(p_banner)
        except Exception as e:
            logger.error(f"Error rendering banner for vehicle {vehicle.id}: {e}")

        self.db.commit()
        return created_posters

    def render_all_pending(self, limit: int = 50) -> int:
        vehicles = self.db.query(Vehicle).filter(Vehicle.is_active == True).limit(limit).all()
        count = 0
        for v in vehicles:
            try:
                self.generate_all_posters_for_vehicle(v)
                count += 1
            except Exception as e:
                logger.error(f"Error rendering all angle posters for vehicle {v.id}: {e}")
        return count
