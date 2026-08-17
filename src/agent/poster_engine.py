import os
import io
import logging
import urllib.request
from typing import Optional, List, Dict, Any
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from sqlalchemy.orm import Session
from config import settings, POSTERS_DIR
from src.db.models import Vehicle, Poster
from .brand_rules import BrandRules

logger = logging.getLogger(__name__)

class PosterEngine:
    """
    Renders high-resolution automotive marketing posters (Instagram 4:5 Portrait & Web Banner)
    featuring multiple camera angles (Front, Headlight detail, Rear fender, Interior cockpit).
    """

    def __init__(self, db: Session):
        self.db = db
        self._image_cache = {}

    def _get_font(self, size: int, bold: bool = False) -> ImageFont.ImageFont:
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
        img = Image.new("RGBA", (800, 500), (20, 30, 45, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(20, 20), (780, 480)], outline=(227, 6, 19, 150), width=3)
        draw.text((260, 230), f"ARKAS 2. EL - {brand.upper()}", fill=(255, 255, 255, 200))
        return img

    def _create_gradient_bg(self, width: int, height: int) -> Image.Image:
        base = Image.new("RGB", (width, height), (15, 23, 42))  # Slate 900
        draw = ImageDraw.Draw(base)
        
        # Radial ambient light top right
        for r in range(400, 0, -20):
            alpha = int(30 * (1 - r / 400))
            draw.ellipse(
                [(width - 150 - r, 100 - r), (width - 150 + r, 100 + r)],
                fill=(30 + alpha, 41 + alpha, 59 + alpha)
            )
            
        # Bottom dark container
        draw.rectangle([(0, height - 260), (width, height)], fill=(11, 15, 26))
        return base

    def _prepare_angle_image(self, car_img: Image.Image, angle_code: str, is_custom_gallery_photo: bool) -> Image.Image:
        """
        Prepares and enhances the vehicle image for the specific camera angle.
        If a single photo is provided or macro detail is requested, performs intelligent focal cropping.
        """
        orig_w, orig_h = car_img.size

        # If it is an explicit separate gallery photo and not requiring focal macro zoom
        if is_custom_gallery_photo and angle_code in ["interior", "front"]:
            return car_img

        if angle_code == "headlight":
            # Macro focus on front headlight and front grill (left-to-center focal area)
            crop_box = (
                int(orig_w * 0.08),
                int(orig_h * 0.32),
                int(orig_w * 0.68),
                int(orig_h * 0.88)
            )
            return car_img.crop(crop_box)
        elif angle_code == "rear":
            # Macro focus on rear quarter, taillight and rear fender (center-to-right area)
            crop_box = (
                int(orig_w * 0.40),
                int(orig_h * 0.28),
                int(orig_w * 0.96),
                int(orig_h * 0.88)
            )
            return car_img.crop(crop_box)
        elif angle_code == "interior" and not is_custom_gallery_photo:
            # Cockpit / cabin roofline focal crop
            crop_box = (
                int(orig_w * 0.25),
                int(orig_h * 0.18),
                int(orig_w * 0.78),
                int(orig_h * 0.72)
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
        Renders a 1080x1350 4:5 Instagram Portrait poster for a specific vehicle camera angle.
        """
        W, H = settings.POSTER_WIDTH, settings.POSTER_HEIGHT
        canvas = self._create_gradient_bg(W, H)
        draw = ImageDraw.Draw(canvas)

        font_header_tag = self._get_font(28, bold=True)
        font_brand = self._get_font(36, bold=True)
        font_title = self._get_font(50, bold=True)
        font_spec = self._get_font(26, bold=True)
        font_price = self._get_font(58, bold=True)
        font_cta = self._get_font(24, bold=True)
        font_feature = self._get_font(24, bold=False)

        # 1. Top Header: Arkas Red Pill
        pill_x1, pill_y1, pill_x2, pill_y2 = 50, 50, 480, 110
        draw.rounded_rectangle([(pill_x1, pill_y1), (pill_x2, pill_y2)], radius=25, fill=(227, 6, 19))
        draw.text((pill_x1 + 30, pill_y1 + 17), "ARKAS 2. EL GUVENCESİYLE", fill=(255, 255, 255), font=font_header_tag)

        # Year badge
        draw.rounded_rectangle([(W - 250, 50), (W - 50, 110)], radius=25, fill=(30, 41, 59), outline=(227, 6, 19), width=2)
        draw.text((W - 220, 67), f"{vehicle.year} MODEL", fill=(255, 255, 255), font=font_header_tag)

        # 2. Vehicle Angle Photo Card
        car_img = self._download_image(image_url)
        if not car_img:
            car_img = self._get_fallback_image(vehicle.brand)

        # Apply intelligent angle focal crop if needed
        car_img_angle = self._prepare_angle_image(car_img, angle_code, is_custom_gallery_photo)

        target_img_w = W - 100
        target_img_h = 580
        car_img_resized = car_img_angle.resize((target_img_w, target_img_h), Image.Resampling.LANCZOS)

        mask = Image.new("L", (target_img_w, target_img_h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (target_img_w, target_img_h)], radius=30, fill=255)

        # Outer border
        draw.rounded_rectangle([(46, 136), (W - 46, 144 + target_img_h)], radius=32, fill=(255, 255, 255, 20), outline=(227, 6, 19, 100), width=3)
        canvas.paste(car_img_resized.convert("RGB"), (50, 140), mask=mask)

        # Angle Badge Tag over photo
        badge_w = len(angle_badge) * 16 + 40
        draw.rounded_rectangle([(70, 160), (70 + badge_w, 208)], radius=14, fill=(15, 23, 42, 230), outline=(227, 6, 19), width=1)
        draw.text((85, 172), angle_badge, fill=(255, 255, 255), font=font_cta)

        # 3. Vehicle Typography
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

        # 4. Feature Highlights
        feat_y = badge_y + 65
        draw.text((50, feat_y), "ONE CIKAN DONANIMLAR", fill=(148, 163, 184), font=font_cta)

        features_to_show = vehicle.features[:3] if vehicle.features else ["Ekspertiz ve Kilometre Garantili", "Yetkili Servis Bakimli", "Kusursuz Kondisyon"]
        for idx, feat in enumerate(features_to_show):
            item_y = feat_y + 35 + (idx * 35)
            draw.text((60, item_y), f"•  {feat}", fill=(226, 232, 240), font=font_feature)

        # 5. Bottom Price & CTA Footer Card
        footer_y1 = H - 180
        draw.rounded_rectangle([(50, footer_y1), (W - 50, H - 40)], radius=24, fill=(227, 6, 19))
        price_text = f"{vehicle.price:,.0f} {vehicle.currency}".replace(",", ".")
        draw.text((80, footer_y1 + 25), price_text, fill=(255, 255, 255), font=font_price)
        draw.text((80, footer_y1 + 95), "Detaylar & Randevu Icin Hemen Iletisime Gecin", fill=(255, 230, 230), font=font_cta)

        # Right CTA Button on footer
        btn_w = 240
        draw.rounded_rectangle([(W - 50 - btn_w - 30, footer_y1 + 35), (W - 80, footer_y1 + 105)], radius=15, fill=(255, 255, 255))
        draw.text((W - 50 - btn_w + 10, footer_y1 + 55), "INCELE & AL >", fill=(227, 6, 19), font=font_cta)

        # Save output
        filename = f"poster_{vehicle.id}_{angle_code}.png"
        output_path = POSTERS_DIR / filename
        canvas.save(output_path, "PNG", quality=95)

        return f"/static/generated_posters/{filename}"

    def render_banner(self, vehicle: Vehicle, image_url: str) -> str:
        """
        Renders a 1200x630 Web/Landscape banner.
        """
        W, H = settings.BANNER_WIDTH, settings.BANNER_HEIGHT
        canvas = self._create_gradient_bg(W, H)
        draw = ImageDraw.Draw(canvas)

        font_header_tag = self._get_font(24, bold=True)
        font_brand = self._get_font(30, bold=True)
        font_title = self._get_font(40, bold=True)
        font_spec = self._get_font(22, bold=True)
        font_price = self._get_font(46, bold=True)
        font_cta = self._get_font(20, bold=True)

        # Left Column: Information
        draw.rounded_rectangle([(50, 40), (420, 85)], radius=20, fill=(227, 6, 19))
        draw.text((70, 52), "ARKAS 2. EL GUVENCESİYLE", fill=(255, 255, 255), font=font_header_tag)

        draw.text((50, 110), vehicle.brand.upper(), fill=(227, 6, 19), font=font_brand)
        model_str = f"{vehicle.model} {vehicle.sub_model or ''}"
        if len(model_str) > 24:
            model_str = model_str[:22] + "..."
        draw.text((50, 150), model_str, fill=(255, 255, 255), font=font_title)

        km_str = f"{vehicle.km:,.0f} KM".replace(",", ".")
        badges = [f"{vehicle.year} MODEL", km_str, vehicle.fuel_type or "Benzin"]
        cur_x = 50
        for b in badges:
            b_len = len(b) * 12 + 25
            draw.rounded_rectangle([(cur_x, 220), (cur_x + b_len, 260)], radius=10, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
            draw.text((cur_x + 12, 230), b, fill=(241, 245, 249), font=font_spec)
            cur_x += b_len + 12

        features_to_show = vehicle.features[:2] if vehicle.features else ["Ekspertiz Garantili", "Yetkili Servis Bakimli"]
        for idx, feat in enumerate(features_to_show):
            draw.text((50, 285 + idx * 30), f"• {feat}", fill=(203, 213, 225), font=font_cta)

        price_text = f"{vehicle.price:,.0f} {vehicle.currency}".replace(",", ".")
        draw.text((50, 370), price_text, fill=(255, 255, 255), font=font_price)

        draw.rounded_rectangle([(50, 440), (280, 500)], radius=15, fill=(227, 6, 19))
        draw.text((75, 460), "HEMEN INCELE >", fill=(255, 255, 255), font=font_cta)

        # Right Column: Car Image
        car_img = self._download_image(image_url)
        if not car_img:
            car_img = self._get_fallback_image(vehicle.brand)

        target_w, target_h = 500, 460
        car_img_resized = car_img.resize((target_w, target_h), Image.Resampling.LANCZOS)

        mask = Image.new("L", (target_w, target_h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (target_w, target_h)], radius=25, fill=255)

        draw.rounded_rectangle([(650, 40), (650 + target_w, 40 + target_h)], radius=27, fill=(255, 255, 255, 20), outline=(227, 6, 19, 100), width=2)
        canvas.paste(car_img_resized.convert("RGB"), (650, 40), mask=mask)

        filename = f"poster_{vehicle.id}_banner.png"
        output_path = POSTERS_DIR / filename
        canvas.save(output_path, "PNG", quality=95)

        return f"/static/generated_posters/{filename}"

    def generate_all_posters_for_vehicle(self, vehicle: Vehicle) -> List[Poster]:
        """
        Generates 4 distinct camera angle posters (Front, Headlight/Grill, Rear profile, Interior)
        and 1 landscape banner using the vehicle's real photo gallery.
        """
        # Delete existing poster records for this vehicle
        self.db.query(Poster).filter(Poster.vehicle_id == vehicle.id).delete()
        self.db.flush()

        gallery = vehicle.image_urls if (vehicle.image_urls and len(vehicle.image_urls) > 0) else [vehicle.primary_image_url]
        primary = vehicle.primary_image_url or (gallery[0] if gallery else "")

        # Define 4 angles with appropriate gallery indices
        angle_configs = [
            {
                "code": "front",
                "badge": "ANA DIS GORUNUM",
                "title": f"{vehicle.brand} {vehicle.model} - Ana Dis Görünüm",
                "type": "instagram_post",
                "image_url": gallery[0] if len(gallery) > 0 else primary
            },
            {
                "code": "headlight",
                "badge": "ON FAR & DETAY",
                "title": f"{vehicle.brand} {vehicle.model} - Ön Far & Izgara Detayı",
                "type": "detail_headlight",
                "image_url": gallery[1] if len(gallery) > 1 else (gallery[0] if gallery else primary)
            },
            {
                "code": "rear",
                "badge": "ARKA & DINAMIK PROFIL",
                "title": f"{vehicle.brand} {vehicle.model} - Arka Çamurluk & Dinamik Profil",
                "type": "rear_profile",
                "image_url": gallery[2] if len(gallery) > 2 else (gallery[-1] if len(gallery) > 1 else primary)
            },
            {
                "code": "interior",
                "badge": "IC MEKAN & KOKPIT",
                "title": f"{vehicle.brand} {vehicle.model} - İç Mekan & Kokpit",
                "type": "interior_cockpit",
                "image_url": gallery[4] if len(gallery) > 4 else (gallery[2] if len(gallery) > 2 else primary)
            }
        ]

        created_posters = []

        # 1. Generate 4 Angle Portrait Posters
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
                    theme_color="#E30613"
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
                title=f"{vehicle.brand} {vehicle.model} - Web & Sosyal Medya Bannerı",
                badge_text="16:9 BANNER",
                theme_color="#E30613"
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
