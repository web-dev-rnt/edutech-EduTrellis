"""Who may use the owner-only admin tools: Backup Management, Audit Log and Tutor AI."""
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def is_site_owner(user):
    """A super admin whose email is in settings.SITE_OWNER_EMAILS."""
    allowed = {email.strip().lower() for email in getattr(settings, "SITE_OWNER_EMAILS", [])}
    return bool(
        user and user.is_authenticated and user.is_active and user.is_superuser
        and (user.email or "").strip().lower() in allowed
    )


can_manage_backups = is_site_owner


def site_owner_required(view_fn):
    """Logged-out visitors go to login; other admins are sent back to the dashboard (or get 403 on POST)."""
    @wraps(view_fn)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), "login")
        if not is_site_owner(request.user):
            if request.method != "GET":
                return HttpResponseForbidden("Access denied.")
            messages.error(request, "Access denied. This section is restricted to the site owner.")
            return redirect("admindashboard")
        return view_fn(request, *args, **kwargs)
    return wrapper
