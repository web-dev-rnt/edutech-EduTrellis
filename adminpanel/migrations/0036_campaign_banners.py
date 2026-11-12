"""Add the colourful campaign banners (free 3-month test series, board exams, competitive exams)
and put the free-offer banner first. Non-destructive: banners are matched by title, existing
ones are only re-ordered, and nothing is deleted."""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.db import migrations

BRAND_DIR = Path(settings.BASE_DIR) / "base" / "static" / "img" / "brand"

NEW_BANNERS = [
    ("Free Test Series for 3 Months", "Indore Tutorials - free test series for 3 months, all mock tests unlocked", 1, 5),
    ("Ace Your Board Exams", "Indore Tutorials - chapter-wise tests and board mocks for CBSE, ICSE, UP Board, NIOS and state boards", 3, 6),
    ("Crack Your Dream Exam", "Indore Tutorials - full mocks, PYQ papers and topic tests for 100+ competitive exams", 5, 7),
]
ORDER = {
    "Learn Smarter, Score Higher": 2,
    "Boost Your Score with Smart Tests": 4,
    "Knowledge That Costs Nothing": 6,
    "Learn Anytime, Anywhere": 7,
}


def add_banners(apps, schema_editor):
    Banner = apps.get_model("adminpanel", "Banner")
    for title, alt, order, n in NEW_BANNERS:
        if Banner.objects.filter(title=title).exists():
            continue
        desktop, mobile = BRAND_DIR / f"banner-{n}-desktop.webp", BRAND_DIR / f"banner-{n}-mobile.webp"
        if not desktop.exists():
            continue
        banner = Banner(title=title, alt_text=alt, order=order, is_active=True)
        with open(desktop, "rb") as fh:
            banner.image.save(desktop.name, File(fh), save=False)
        if mobile.exists():
            with open(mobile, "rb") as fh:
                banner.mobile_image.save(mobile.name, File(fh), save=False)
        banner.save()
    for title, order in ORDER.items():
        Banner.objects.filter(title=title).update(order=order)


def remove_banners(apps, schema_editor):
    Banner = apps.get_model("adminpanel", "Banner")
    Banner.objects.filter(title__in=[b[0] for b in NEW_BANNERS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("adminpanel", "0035_tutor_settings_and_queries"),
    ]

    operations = [
        migrations.RunPython(add_banners, remove_banners),
    ]
