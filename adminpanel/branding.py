"""The site's brand name, stored in the database (Brand & Theme settings) and editable in the admin panel.

Every page title, email, SEO tag and admin heading reads the name from here, so renaming the brand
needs no code change.
"""
from django.utils.text import slugify

DEFAULT_NAME = 'EduTrellis'
DEFAULT_FULL_NAME = 'EduTrellis Test Series'


def brand():
    """{'name', 'full_name', 'slug'} from the saved settings, or the defaults if the table isn't ready yet."""
    name, full_name = DEFAULT_NAME, DEFAULT_FULL_NAME
    try:
        from django.db import transaction

        from .models import ThemeSettings
        with transaction.atomic():  # a savepoint, so a failed lookup never breaks the caller's transaction
            theme = ThemeSettings.get_solo()
        name = (theme.site_name or '').strip() or DEFAULT_NAME
        full_name = (theme.site_full_name or '').strip() or name
    except Exception:  # before migrations run, or the database is unavailable
        pass
    return {'name': name, 'full_name': full_name, 'slug': slugify(name) or 'site'}


def brand_name():
    return brand()['name']


def brand_full_name():
    return brand()['full_name']


def default_backup_folder():
    return f"/{brand()['slug']}-backup"
