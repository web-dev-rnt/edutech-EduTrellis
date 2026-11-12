# adminpanel/management/commands/apply_brand_assets.py
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from adminpanel.models import (
    AboutUsSection,
    AuthPageSettings,
    Banner,
    CTASection,
    FooterSettings,
    NavbarSettings,
    ThemeSettings,
)

BRAND_DIR = Path(settings.BASE_DIR) / "base" / "static" / "img" / "brand"
BRAND_COLOR = "#2459E0"

# (title, alt text, display order, artwork number -> banner-<n>-desktop/mobile.webp)
BANNERS = [
    ("Free Test Series for 3 Months", "Infinite360 - free test series for 3 months, all mock tests unlocked", 1, 5),
    ("Learn Smarter, Score Higher", "Infinite360 - live classes, video courses and test series", 2, 1),
    ("Ace Your Board Exams", "Infinite360 - chapter-wise tests and board mocks for CBSE, ICSE, UP Board, NIOS and state boards", 3, 6),
    ("Boost Your Score with Smart Tests", "Infinite360 - mock tests, PYQs and all-India rank", 4, 2),
    ("Crack Your Dream Exam", "Infinite360 - full mocks, PYQ papers and topic tests for 100+ competitive exams", 5, 7),
    ("Knowledge That Costs Nothing", "Infinite360 - knowledge that costs nothing, empowers everything", 6, 3),
    ("Learn Anytime, Anywhere", "Infinite360 - video lectures, notes and e-books", 7, 4),
]


def attach(instance, field_name, filename):
    """Copy base/static/img/brand/<filename> into the field, unless an identical copy is already there."""
    field = getattr(instance, field_name)
    source = (BRAND_DIR / filename).read_bytes()
    if field and Path(field.name).name == filename:
        try:
            with field.storage.open(field.name, "rb") as current:
                if current.read() == source:
                    return False
        except FileNotFoundError:
            pass
        # Re-rendered artwork: replace the stored file under the same name.
        field.storage.delete(field.name)
    with open(BRAND_DIR / filename, "rb") as fh:
        field.save(filename, File(fh), save=False)
    return True


class Command(BaseCommand):
    help = (
        "Apply the Infinite360 brand artwork (logo, favicon, banners, login/signup images) "
        "and brand color to the site settings. Run design/brand_assets/export.py first if you "
        "re-rendered the artwork. Safe to run more than once."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--keep-old-banners",
            action="store_true",
            help="Leave existing banners active instead of deactivating them.",
        )

    def handle(self, *args, **options):
        theme = ThemeSettings.get_solo()
        theme.primary_color = BRAND_COLOR
        theme.save()

        navbar = NavbarSettings.objects.first() or NavbarSettings()
        attach(navbar, "logo", "logo-inline.png")
        attach(navbar, "favicon", "favicon.png")
        navbar.save()

        footer = FooterSettings.objects.first() or FooterSettings()
        attach(footer, "logo", "logo-horizontal-light.png")
        footer.save()

        about = AboutUsSection.objects.first()
        if about:
            attach(about, "logo", "logo-badge.png")
            about.save()

        cta = CTASection.objects.first()
        if cta:
            cta.button_color = BRAND_COLOR
            cta.save()

        auth = AuthPageSettings.get_solo()
        attach(auth, "login_image", "auth-login.webp")
        attach(auth, "signup_image", "auth-signup.webp")
        attach(auth, "login_image_mobile", "auth-login-mobile.webp")
        attach(auth, "signup_image_mobile", "auth-signup-mobile.webp")
        auth.save()

        brand_ids = []
        for title, alt, order, i in BANNERS:
            banner = Banner.objects.filter(title=title).first() or Banner(title=title)
            banner.alt_text = alt
            banner.order = order
            banner.is_active = True
            attach(banner, "image", f"banner-{i}-desktop.webp")
            attach(banner, "mobile_image", f"banner-{i}-mobile.webp")
            banner.save()
            brand_ids.append(banner.pk)

        if not options["keep_old_banners"]:
            retired = Banner.objects.filter(is_active=True).exclude(pk__in=brand_ids).update(is_active=False)
            if retired:
                self.stdout.write(f"Deactivated {retired} older banner(s); re-enable them from the admin panel if needed.")

        self.stdout.write(self.style.SUCCESS("Brand assets applied."))
