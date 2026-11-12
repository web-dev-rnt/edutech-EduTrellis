# adminpanel/context_processors.py
from .models import NavbarSettings, FooterSettings, FooterLink, FooterLegalLink
from video_courses.models import Category
from django.conf import settings
from django.core.cache import cache
from django.templatetags.static import static

# ── Site-wide contact constants ──────────────────────────────────────────────
SITE_EMAIL = "businessconsulting@gmail.com"
SITE_PHONE = "8296893895"
SITE_PHONE_DISPLAY = "+91 82968 93895"
SITE_WHATSAPP_NUMBER = "918296893895"  # country code + number, no +
SITE_WHATSAPP_URL = (
    f"https://wa.me/{SITE_WHATSAPP_NUMBER}"
    "?text=Hello%2C%20I%20would%20like%20to%20know%20more%20about%20Infinite360%20Tech%20Academy%20courses"
)
SITE_ADDRESS = "8th Floor, DLF Cyber City, Tower A, Phase III, Gurugram - 122002, India"
SITE_MAPS_URL = "https://maps.google.com/?q=DLF+Cyber+City+Tower+A+Phase+III+Gurugram+Haryana+122002"
# Same address split into schema.org PostalAddress parts for structured data.
SITE_POSTAL_ADDRESS = {
    "streetAddress": "8th Floor, DLF Cyber City, Tower A, Phase III",
    "addressLocality": "Gurugram",
    "addressRegion": "Haryana",
    "postalCode": "122002",
    "addressCountry": "IN",
}
# ─────────────────────────────────────────────────────────────────────────────

# ── SEO defaults ─────────────────────────────────────────────────────────────
SITE_NAME = "Infinite360"
SITE_LEGAL_NAME = "Infinite360 Tech Academy"
SEO_DEFAULT_TITLE = "Infinite360 Tech Academy | Online Live Classes, Video Courses & Test Series"
SEO_DEFAULT_DESCRIPTION = (
    "Infinite360 Tech Academy: live online classes, video courses, mock test series, "
    "previous year papers and e-books for board and competitive exams. Learn anytime, anywhere."
)
SEO_KEYWORDS = (
    "Infinite360, Infinite360 Tech Academy, Infinite 360, Infinite360 academy, online coaching, live online classes, video courses, online test series, "
    "mock tests, previous year papers, e-library, e-books, CBSE, board exam preparation, "
    "competitive exam preparation"
)
SEO_DEFAULT_IMAGE = "img/brand/logo-horizontal.png"
# ─────────────────────────────────────────────────────────────────────────────


def site_contact(request):
    """
    Injects sitewide contact details into every template context.
    Usage in templates:
        {{ site_contact.email }}
        {{ site_contact.phone }}
        {{ site_contact.whatsapp_url }}
        {{ site_contact.address }}
    """
    return {
        "site_contact": {
            "email": SITE_EMAIL,
            "phone": SITE_PHONE,
            "phone_display": SITE_PHONE_DISPLAY,
            "whatsapp_number": SITE_WHATSAPP_NUMBER,
            "whatsapp_url": SITE_WHATSAPP_URL,
            "address": SITE_ADDRESS,
            "maps_url": SITE_MAPS_URL,
        }
    }


def seo(request):
    """
    Injects SEO defaults into every template context.
    Canonical URLs always point at settings.SITE_URL so www/non-www and
    alternate domains consolidate onto one indexed origin.
        {{ seo.title }}  {{ seo.description }}  {{ seo.canonical_url }}  {{ seo.image }}
    """
    site_url = settings.SITE_URL
    return {
        "seo": {
            "site_name": SITE_NAME,
            "site_url": site_url,
            "title": SEO_DEFAULT_TITLE,
            "description": SEO_DEFAULT_DESCRIPTION,
            "keywords": SEO_KEYWORDS,
            "canonical_url": f"{site_url}{request.path}",
            "image": f"{site_url}{static(SEO_DEFAULT_IMAGE)}",
        }
    }


def navbar_settings(request):
    """Make navbar settings available in all templates"""
    try:
        settings = cache.get("site-navbar-settings-v3")
        if settings is None:
            settings = NavbarSettings.objects.filter(is_active=True).first()
        if not settings:
            settings = NavbarSettings.objects.create(
                contact_number=SITE_PHONE,
                contact_type="whatsapp",
            )
        cache.set("site-navbar-settings-v3", settings, 300)
        return {"navbar_settings": settings}
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning("navbar_settings context processor error: %s", e)
        return {"navbar_settings": None}


def footer_settings(request):
    """Make footer settings available in all templates"""
    try:
        cached_footer = cache.get("site-footer-settings-v3")
        if cached_footer is None:
            settings = FooterSettings.objects.filter(is_active=True).first()
            footer_links = list(FooterLink.objects.filter(is_active=True))
            footer_legal_links = list(FooterLegalLink.objects.filter(is_active=True))
        else:
            settings, footer_links, footer_legal_links = cached_footer

        if not settings:
            settings = FooterSettings.objects.create(
                email=SITE_EMAIL,
                copyright_text="Copyright \u00a9 2026 Infinite360. All rights reserved.",
            )

        cache.set(
            "site-footer-settings-v3",
            (settings, footer_links, footer_legal_links),
            300,
        )

        return {
            "footer_settings": settings,
            "footer_links": footer_links,
            "footer_legal_links": footer_legal_links,
        }
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning("footer_settings context processor error: %s", e)
        return {
            "footer_settings": None,
            "footer_links": [],
            "footer_legal_links": [],
        }
