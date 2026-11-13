"""Render the Edutrellis brand assets to PNG with headless Chromium.

Usage:
    python design/brand_assets/render.py            # render everything into out/
    python design/brand_assets/render.py banner_1   # render assets whose name contains "banner_1"

Assets are declared in scenes.js (ASSETS); brand.js and people.js hold shared parts.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
FONTS = (HERE.parent.parent / "base" / "static" / "fonts").as_uri()
OUT = HERE / "out"

PAGE = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Plus Jakarta Sans"; src: url("{FONTS}/plus-jakarta-sans-variable.woff2") format("woff2"); font-weight: 200 800; }}
html, body {{ margin: 0; padding: 0; background: transparent; }}
svg {{ display: block; }}
</style></head><body><div id="stage"></div>
<script src="brand.js"></script><script src="people.js"></script><script src="scenes.js"></script>
</body></html>"""


def trim(path, pad=8):
    """Crop a transparent PNG to its visible content plus a small margin."""
    from PIL import Image

    im = Image.open(path)
    left, top, right, bottom = im.getchannel("A").getbbox()
    im.crop((max(left - pad, 0), max(top - pad, 0), min(right + pad, im.width), min(bottom + pad, im.height))).save(path)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    OUT.mkdir(exist_ok=True)
    page_file = HERE / "_stage.html"
    page_file.write_text(PAGE, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=1)
        page.goto(page_file.as_uri())
        page.evaluate("document.fonts.load('700 20px \"Plus Jakarta Sans\"')")
        page.wait_for_function("document.fonts.status === 'loaded'")
        names = page.evaluate("Object.keys(ASSETS)")
        for name in names:
            if only and only not in name:
                continue
            w, h = page.evaluate(
                """(n) => {
                    const a = ASSETS[n], k = a.scale || 1;
                    document.getElementById('stage').innerHTML =
                        `<svg xmlns="http://www.w3.org/2000/svg" width="${a.w * k}" height="${a.h * k}" viewBox="0 0 ${a.w} ${a.h}">${defs()}${a.draw()}</svg>`;
                    return [a.w * k, a.h * k];
                }""",
                name,
            )
            page.set_viewport_size({"width": w, "height": h})
            page.wait_for_timeout(50)
            target = OUT / f"{name}.png"
            page.locator("svg").screenshot(path=str(target), omit_background=True)
            if page.evaluate("(n) => !!ASSETS[n].trim", name):
                trim(target)
            print(f"rendered {target.name} ({w}x{h})")
        browser.close()
    page_file.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
