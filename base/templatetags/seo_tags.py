import json

from django import template
from django.conf import settings
from django.db.models.fields.files import FieldFile
from django.templatetags.static import static
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from adminpanel.context_processors import (
    SITE_EMAIL,
    SITE_LEGAL_NAME,
    SITE_NAME,
    SITE_PHONE,
    SITE_POSTAL_ADDRESS,
    SEO_DEFAULT_DESCRIPTION,
)

register = template.Library()

SOCIAL_FIELDS = ("facebook_url", "twitter_url", "youtube_url", "linkedin_url", "instagram_url", "telegram_url")


def _script(data):
    # Escape "<" so a stray "</script>" inside course text can't close the tag.
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    return mark_safe(f'<script type="application/ld+json">{payload}</script>')


def _absolute(url):
    """Absolute URL for a path, URL string or (possibly empty) image field."""
    if isinstance(url, FieldFile):
        if not url:  # no file attached; .url would raise
            return ""
        url = url.url
    url = str(url or "")
    if not url:
        return ""
    return url if url.startswith(("http://", "https://")) else f"{settings.SITE_URL}{url}"


def _organization(footer_settings=None):
    same_as = [
        url for url in (getattr(footer_settings, f, "") for f in SOCIAL_FIELDS) if url
    ]
    org = {
        "@type": "EducationalOrganization",
        "@id": f"{settings.SITE_URL}/#organization",
        "name": SITE_NAME,
        "legalName": SITE_LEGAL_NAME,
        "alternateName": [SITE_LEGAL_NAME, "Infinite 360", "Infinite360 Academy"],
        "url": f"{settings.SITE_URL}/",
        "logo": _absolute(static("img/brand/logo-badge.png")),
        "image": _absolute(static("img/brand/logo-horizontal.png")),
        "description": SEO_DEFAULT_DESCRIPTION,
        "email": SITE_EMAIL,
        "telephone": f"+91-{SITE_PHONE}",
        "address": {"@type": "PostalAddress", **SITE_POSTAL_ADDRESS},
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": f"+91-{SITE_PHONE}",
            "email": SITE_EMAIL,
            "contactType": "customer support",
            "areaServed": "IN",
            "availableLanguage": ["English", "Hindi"],
        },
    }
    if same_as:
        org["sameAs"] = same_as
    return org


@register.simple_tag(takes_context=True)
def site_jsonld(context):
    """Organization + WebSite (with sitelinks search box) graph for every page."""
    return _script({
        "@context": "https://schema.org",
        "@graph": [
            _organization(context.get("footer_settings")),
            {
                "@type": "WebSite",
                "@id": f"{settings.SITE_URL}/#website",
                "name": SITE_NAME,
                "alternateName": SITE_LEGAL_NAME,
                "url": f"{settings.SITE_URL}/",
                "inLanguage": "en-IN",
                "publisher": {"@id": f"{settings.SITE_URL}/#organization"},
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": f"{settings.SITE_URL}/search/?q={{search_term_string}}",
                    "query-input": "required name=search_term_string",
                },
            },
        ],
    })


@register.simple_tag(takes_context=True)
def course_jsonld(context, name, description="", image="", price=None, currency="INR", is_free=False):
    """schema.org Course for course/test-series/e-book detail pages."""
    request = context.get("request")
    url = f"{settings.SITE_URL}{request.path}" if request else settings.SITE_URL
    name = strip_tags(str(name or "")).strip()
    text = strip_tags(description or "").strip() or f"{name} by {SITE_NAME}."
    data = {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": name,
        "description": text[:500],
        "url": url,
        "inLanguage": "en-IN",
        "provider": {"@type": "Organization", "name": SITE_NAME, "sameAs": f"{settings.SITE_URL}/"},
    }
    image_url = _absolute(image)
    if image_url:
        data["image"] = image_url
    if is_free or price is not None:
        data["offers"] = {
            "@type": "Offer",
            "category": "Free" if is_free else "Paid",
            "price": "0" if is_free else str(price),
            "priceCurrency": currency or "INR",
            "availability": "https://schema.org/InStock",
            "url": url,
        }
    return _script(data)


@register.filter
def absolute_url(url):
    """Turn a /media/... or /static/... path (or an image field) into an absolute URL on SITE_URL."""
    return _absolute(url)
