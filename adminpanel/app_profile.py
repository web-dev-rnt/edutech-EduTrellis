"""The installable app (PWA) and link-sharing preview: admin values with brand defaults.

Edited in the admin panel under Website > App & Sharing (AppSettings). Every field may be left blank:
app_profile() fills it from the brand name and the default artwork in base/static/img.
"""
from io import BytesIO

from django.core.files.base import ContentFile
from django.templatetags.static import static

from .branding import brand

DEFAULT_SHARE_IMAGE = "img/brand/og-share.jpg"  # 1200 x 630, see design/brand_assets (og_share)
SHARE_IMAGE_SIZE = (1200, 630)


def default_texts(site_brand=None):
    site_brand = site_brand or brand()
    name, full_name = site_brand["name"], site_brand["full_name"]
    return {
        "app_name": full_name if "test series" in full_name.lower() else f"{full_name} – Online Test Series",
        "short_name": name,
        "description": (f"{name}: India's best platform for online test series. Exam-pattern mock tests, previous "
                        f"year papers with solutions, instant results and all-India rank."),
        "share_title": f"{name} – India's Best Platform for Online Test Series",
        "share_description": (f"Crack your exam with {name}: exam-pattern mock tests, previous year papers with "
                              f"solutions, instant results and all-India rank for SSC, Banking, Railways, JEE, NEET "
                              f"and board exams. 10,000+ students trained."),
    }


def app_profile():
    """Resolved app and sharing values (URLs are relative; make them absolute where needed)."""
    from django.db import DatabaseError

    from .models import AppSettings, ThemeSettings

    try:
        settings_obj = AppSettings.get_solo()
    except DatabaseError:  # table not migrated yet (e.g. mid-deploy or mid-restore): use the defaults
        settings_obj = AppSettings()
    defaults = default_texts()

    def url(field, fallback):
        try:
            return field.url if field else static(fallback)
        except Exception:  # storage unreachable: never break a page over an icon
            return static(fallback)

    custom_icons = bool(settings_obj.icon_512)
    return {
        "app_name": settings_obj.app_name or defaults["app_name"],
        "short_name": settings_obj.short_name or defaults["short_name"],
        "description": settings_obj.description or defaults["description"],
        "theme_color": settings_obj.theme_color or ThemeSettings.get_solo().primary_color or "#D7263D",
        "background_color": settings_obj.background_color or "#ffffff",
        "icon_192": url(settings_obj.icon_192, "img/icon-192.png"),
        "icon_512": url(settings_obj.icon_512, "img/icon-512.png"),
        "icon_maskable": url(settings_obj.icon_maskable, "img/icon-512.png"),
        "icon_apple": url(settings_obj.icon_apple, "img/brand/apple-touch-icon.png"),
        "custom_icons": custom_icons,
        "share_title": settings_obj.share_title or defaults["share_title"],
        "share_description": settings_obj.share_description or defaults["share_description"],
        "share_image": url(settings_obj.share_image, DEFAULT_SHARE_IMAGE),
        "version": settings_obj.version,
        "defaults": defaults,
    }


# ── image processing ────────────────────────────────────────────────────────────────────────────────
def _open_rgba(source):
    from PIL import Image, ImageOps

    source.seek(0)
    image = Image.open(source)
    image = ImageOps.exif_transpose(image)
    return image.convert("RGBA")


def _square(image, size, background=None, scale=1.0):
    """The image fitted (not cropped) into a size x size square, optionally on a solid background."""
    from PIL import Image

    canvas = Image.new("RGBA", (size, size), background or (0, 0, 0, 0))
    inner = max(1, int(size * scale))
    fitted = image.copy()
    fitted.thumbnail((inner, inner), Image.LANCZOS)
    if fitted.width < inner and fitted.height < inner:  # small source: scale up to fill
        ratio = inner / max(fitted.width, fitted.height)
        fitted = image.resize((max(1, int(image.width * ratio)), max(1, int(image.height * ratio))), Image.LANCZOS)
    canvas.alpha_composite(fitted, ((size - fitted.width) // 2, (size - fitted.height) // 2))
    return canvas


def _png(image):
    out = BytesIO()
    image.save(out, "PNG", optimize=True)
    return ContentFile(out.getvalue())


def _hex_to_rgba(value):
    value = (value or "#ffffff").lstrip("#")
    try:
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
    except ValueError:
        return (255, 255, 255, 255)


def check_icon(upload):
    """Raise ValueError unless the upload is a usable app icon."""
    try:
        image = _open_rgba(upload)
    except Exception:
        raise ValueError("This file is not an image Pillow can read. Upload a PNG or JPG.")
    if min(image.size) < 192:
        raise ValueError(f"The icon is {image.width} × {image.height} px; it needs to be at least 192 × 192 (512 × 512 is best).")


def build_icons(settings_obj, source):
    """Make the 192, 512, maskable (safe-zone padded) and Apple touch icons from `source`."""
    image = _open_rgba(source)
    background = _hex_to_rgba(settings_obj.background_color)
    stamp = settings_obj.updated_at.strftime("%Y%m%d%H%M%S") if settings_obj.updated_at else "new"
    variants = {
        "icon_192": _square(image, 192),
        "icon_512": _square(image, 512),
        # Android crops maskable icons to a circle/squircle: keep the artwork inside the central 80%.
        "icon_maskable": _square(image, 512, background, scale=0.8),
        # iOS fills transparency with black: give the Apple icon a solid background.
        "icon_apple": _square(image, 180, background, scale=0.86),
    }
    for field, picture in variants.items():
        old = getattr(settings_obj, field)
        if old:
            try:
                old.delete(save=False)
            except Exception:
                pass
        getattr(settings_obj, field).save(f"{field.replace('_', '-')}-{stamp}.png", _png(picture), save=False)


def build_share_image(upload):
    """Crop/resize any picture to a 1200 x 630 JPEG (small enough for WhatsApp's preview limit)."""
    from PIL import Image, ImageOps

    upload.seek(0)
    image = ImageOps.exif_transpose(Image.open(upload)).convert("RGB")
    image = ImageOps.fit(image, SHARE_IMAGE_SIZE, Image.LANCZOS)
    out = BytesIO()
    image.save(out, "JPEG", quality=85, optimize=True, progressive=True)
    return ContentFile(out.getvalue())
