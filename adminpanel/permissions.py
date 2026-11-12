"""Who may use the restricted admin tools."""
from django.conf import settings


def can_manage_backups(user):
    """Backups can restore or download the whole database, so only the listed owner accounts get them."""
    allowed = {email.strip().lower() for email in getattr(settings, "BACKUP_MANAGER_EMAILS", [])}
    return bool(
        user and user.is_authenticated and user.is_active and user.is_superuser
        and (user.email or "").strip().lower() in allowed
    )
