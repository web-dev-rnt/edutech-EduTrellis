"""Convert the renders in out/ into the web files the site serves.

Run after render.py:
    python design/brand_assets/export.py

Writes base/static/img/brand/* (used by `manage.py apply_brand_assets`) and refreshes
the legacy static fallbacks (mainlogo.png, footerlogo.png, icon-*.png, ...).
"""
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
IMG = HERE.parent.parent / "base" / "static" / "img"
BRAND = IMG / "brand"


def load(name):
    return Image.open(OUT / f"{name}.png")


def webp(name, dest):
    load(name).convert("RGB").save(dest, "WEBP", quality=90, method=6)


def jpg(name, dest):
    load(name).convert("RGB").save(dest, "JPEG", quality=88, optimize=True, progressive=True)


def png(im, dest, size=None):
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(dest, "PNG", optimize=True)


def main():
    BRAND.mkdir(parents=True, exist_ok=True)

    for i in range(1, 8):
        webp(f"banner_{i}_desktop", BRAND / f"banner-{i}-desktop.webp")
        webp(f"banner_{i}_mobile", BRAND / f"banner-{i}-mobile.webp")
    for page in ("login", "signup"):
        webp(f"auth_{page}_desktop", BRAND / f"auth-{page}.webp")
        webp(f"auth_{page}_mobile", BRAND / f"auth-{page}-mobile.webp")

    png(load("logo_inline"), BRAND / "logo-inline.png")
    png(load("logo_compact"), BRAND / "logo-compact.png")
    png(load("logo_compact_light"), BRAND / "logo-compact-light.png")
    png(load("logo_horizontal"), BRAND / "logo-horizontal.png")
    png(load("logo_horizontal_light"), BRAND / "logo-horizontal-light.png")
    png(load("logo_stacked"), BRAND / "logo-stacked.png")
    png(load("logo_stacked_light"), BRAND / "logo-stacked-light.png")
    png(load("logo_badge"), BRAND / "logo-badge.png", (256, 256))

    icon, maskable = load("icon_512"), load("icon_maskable_512")
    png(icon, BRAND / "favicon.png", (192, 192))
    png(icon, BRAND / "favicon-32.png", (32, 32))
    png(maskable, BRAND / "apple-touch-icon.png", (180, 180))
    icon.save(BRAND / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    # Legacy fallbacks referenced directly by templates and the PWA manifest.
    png(load("logo_inline"), IMG / "mainlogo.png")
    png(load("logo_horizontal_light"), IMG / "footerlogo.png")
    png(maskable, IMG / "icon-192.png", (192, 192))
    png(maskable, IMG / "icon-512.png")
    jpg("auth_login_desktop", IMG / "loginformimg.jpg")
    jpg("default_thumb", IMG / "default-thumb.jpg")

    for f in sorted(BRAND.iterdir()):
        print(f"{f.relative_to(IMG)}  {f.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
