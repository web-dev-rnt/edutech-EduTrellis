from django import template

from adminpanel.models import TutorSettings

register = template.Library()


@register.simple_tag
def get_tutor_settings():
    """Tutor chat settings for the widget (cached; never exposes the key to templates that don't ask)."""
    try:
        return TutorSettings.load()
    except Exception:  # e.g. before migrations have run
        return None
