from django.db import migrations


FOOTER_LINKS = [
    # (section, title, url, order)
    ('about', 'Home', '/', 1),
    ('about', 'About Us', '/#about-us', 2),
    ('about', 'Video Courses', '/#video-courses-section', 3),

    ('help', 'Contact Us', '/page/contact-us/', 1),
    ('help', 'Privacy Policy', '/page/privacy-policy/', 2),
    ('help', 'Refund Policy', '/page/refund-policy/', 3),
    ('help', 'Disclaimer', '/page/disclaimer/', 4),

    ('student', 'My Purchases', '/my_purchases/', 1),
    ('student', 'My Results', '/my_results/', 2),
    ('student', 'My Library', '/my-library/', 3),
    ('student', 'Test Series', '/#testseries-carousel', 4),

    ('business', 'Live Classes', '/#live-carousel', 1),
    ('business', 'E-Library', '/#ebook-carousel', 2),
    ('business', 'Partner With Us', '/page/contact-us/', 3),
]


def seed_footer_links(apps, schema_editor):
    FooterLink = apps.get_model("adminpanel", "FooterLink")
    FooterLegalLink = apps.get_model("adminpanel", "FooterLegalLink")

    for section, title, url, order in FOOTER_LINKS:
        FooterLink.objects.get_or_create(
            section=section, title=title,
            defaults={"url": url, "order": order, "is_active": True},
        )

    # The legal pages now live in the Help column above, so they no longer
    # need their own row in the bottom copyright bar.
    FooterLegalLink.objects.all().delete()


def unseed_footer_links(apps, schema_editor):
    FooterLink = apps.get_model("adminpanel", "FooterLink")
    FooterLegalLink = apps.get_model("adminpanel", "FooterLegalLink")

    titles = [title for _, title, _, _ in FOOTER_LINKS]
    FooterLink.objects.filter(title__in=titles).delete()

    legal_pages = [
        ("Privacy Policy", "privacy-policy", 1),
        ("Disclaimer", "disclaimer", 2),
        ("Refund Policy", "refund-policy", 3),
        ("Contact Us", "contact-us", 4),
    ]
    for title, slug, order in legal_pages:
        FooterLegalLink.objects.get_or_create(
            title=title,
            defaults={"url": f"/page/{slug}/", "order": order, "is_active": True},
        )


class Migration(migrations.Migration):

    dependencies = [
        ("adminpanel", "0030_contactsubmission_notification_read_by"),
    ]

    operations = [
        migrations.RunPython(seed_footer_links, unseed_footer_links),
    ]
