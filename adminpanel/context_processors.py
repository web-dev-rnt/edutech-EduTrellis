# adminpanel/context_processors.py
from .models import NavbarSettings, FooterSettings, FooterLink, FooterLegalLink
from video_courses.models import Category
from django.conf import settings
from django.core.cache import cache
from django.templatetags.static import static

from .branding import brand

# ── Site-wide contact constants ──────────────────────────────────────────────
SITE_EMAIL = "support@edutrellis.in"
SITE_CEO_EMAIL = "ceo@edutrellis.in"
SITE_PHONE = "9194130645"
SITE_PHONE_DISPLAY = "+91 91941 30645"
SITE_WHATSAPP_NUMBER = "919194130645"  # country code + number, no +
SITE_SUPPORT_HOURS = "Mon to Fri, 10 AM to 7 PM"
# schema.org opening hours of the support desk (Monday to Friday, 10:00-19:00 IST).
SITE_SUPPORT_HOURS_SPEC = {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "10:00",
    "closes": "19:00",
}
SITE_STUDENTS_TRAINED_COUNT = 10000  # shown as "10,000+" (home page counter, footer, SEO)
SITE_STUDENTS_TRAINED = f"{SITE_STUDENTS_TRAINED_COUNT:,}+"
SITE_WHATSAPP_URL = (
    f"https://wa.me/{SITE_WHATSAPP_NUMBER}"
    "?text=Hello%2C%20I%20would%20like%20to%20know%20more%20about%20your%20courses"
)
SITE_ADDRESS = "P-109, Prembagh, Shahpur, Chinhat, Lucknow, Uttar Pradesh 226028"
SITE_MAPS_URL = "https://maps.google.com/?q=P-109+Prembagh+Shahpur+Chinhat+Lucknow+Uttar+Pradesh+226028"
# Same address split into schema.org PostalAddress parts for structured data.
SITE_POSTAL_ADDRESS = {
    "streetAddress": "P-109, Prembagh, Shahpur, Chinhat",
    "addressLocality": "Lucknow",
    "addressRegion": "Uttar Pradesh",
    "postalCode": "226028",
    "addressCountry": "IN",
}
# ─────────────────────────────────────────────────────────────────────────────

# ── SEO defaults ─────────────────────────────────────────────────────────────
# The brand name itself lives in the database (Brand & Theme settings); see adminpanel/branding.py.
SEO_TITLE_SUFFIX = "Online Test Series & Mock Tests for Competitive and Board Exams"
SEO_DESCRIPTION_BODY = (
    "online test series & mock tests for competitive and board exams, with PYQs, "
    f"instant results and solutions. {SITE_STUDENTS_TRAINED} students trained."
)
SEO_KEYWORD_TOPICS = (
    "online test series, mock tests, online mock test, test series for competitive exams, "
    "previous year papers, PYQ, practice tests, SSC test series, banking test series, "
    "railway test series, UPSC test series, JEE mock test, NEET mock test, CBSE test series, "
    "board exam mock tests, all-India rank, exam preparation, test series Lucknow"
)


def seo_texts(site_brand=None):
    """Default title, description and keywords built from the saved brand name."""
    site_brand = site_brand or brand()
    name, full_name = site_brand["name"], site_brand["full_name"]
    names = list(dict.fromkeys([name, full_name, f"{name} test series"]))
    return {
        "title": f"{full_name} | {SEO_TITLE_SUFFIX}",
        "description": f"{full_name}: {SEO_DESCRIPTION_BODY}",
        "keywords": ", ".join(names) + ", " + SEO_KEYWORD_TOPICS,
    }
SEO_DEFAULT_IMAGE = "img/brand/logo-horizontal.png"
# ─────────────────────────────────────────────────────────────────────────────


def site_contact(request):
    """
    Injects sitewide contact details into every template context.
    Usage in templates:
        {{ site_contact.email }}  {{ site_contact.ceo_email }}
        {{ site_contact.phone }}  {{ site_contact.hours }}
        {{ site_contact.whatsapp_url }}
        {{ site_contact.address }}
    """
    return {
        "site_contact": {
            "email": SITE_EMAIL,
            "ceo_email": SITE_CEO_EMAIL,
            "phone": SITE_PHONE,
            "hours": SITE_SUPPORT_HOURS,
            "students_trained": SITE_STUDENTS_TRAINED,
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
    site_brand = brand()
    texts = seo_texts(site_brand)
    return {
        "brand": site_brand,
        "seo": {
            "site_name": site_brand["name"],
            "site_url": site_url,
            "title": texts["title"],
            "description": texts["description"],
            "keywords": texts["keywords"],
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
                copyright_text=f"Copyright \u00a9 2026 {brand()['name']}. All rights reserved.",
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
