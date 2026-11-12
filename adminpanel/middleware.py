import logging

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse

logger = logging.getLogger(__name__)

AUDITED_MODULES = {"adminpanel.views", "adminpanel.backup_views", "video_courses.views", "elibrary.views",
                   "testseries.views", "live_class.views", "django.contrib.admin.options", "django.contrib.admin.sites"}
UNAUDITED_VIEWS = {"apply_coupon", "use_coupon", "remove_coupon", "validate_coupon", "my_coupons", "live_class_join", "live_recording_chunk", "backup_upload_chunk",
                   "mark_notification_read", "mark_all_notifications_read"}


class ManagementAccessMiddleware:
    """Require staff access for every management app view."""

    MANAGEMENT_MODULES = {
        "adminpanel.views",
        "video_courses.views",
        "elibrary.views",
        "testseries.views",
    }
    PUBLIC_ADMINPANEL_VIEWS = {
        "apply_coupon",
        "my_coupons",
        "use_coupon",
        "remove_coupon",
        "validate_coupon",
    }
    PUBLIC_LIVE_CLASS_VIEWS = {"live_class_join", "live_recording_play"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        module = view_func.__module__
        name = view_func.__name__
        is_management_view = module in self.MANAGEMENT_MODULES
        if module == "live_class.views" and name not in self.PUBLIC_LIVE_CLASS_VIEWS:
            is_management_view = True
        if module == "adminpanel.views" and name in self.PUBLIC_ADMINPANEL_VIEWS:
            is_management_view = False

        if is_management_view and not (
            request.user.is_authenticated and request.user.is_staff
        ):
            return redirect_to_login(request.get_full_path(), reverse("login"))
        return None


def _audit_action(view_name, method):
    name = view_name.lower()
    if method == "DELETE" or "delete" in name or "remove" in name:
        return "delete"
    if any(word in name for word in ("create", "add", "upload", "new")):
        return "create"
    return "update"


class SecurityHeadersAndAuditMiddleware:
    """
    Adds Permissions-Policy and records every state-changing request staff make in the
    management apps (admin panel, course/test/e-library managers, Django admin).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        policy = getattr(settings, "PERMISSIONS_POLICY", "")
        if policy:
            response.setdefault("Permissions-Policy", policy)

        match = getattr(request, "resolver_match", None)
        user = getattr(request, "user", None)
        if (
            match is not None
            and request.method not in ("GET", "HEAD", "OPTIONS")
            and user is not None and user.is_authenticated and user.is_staff
        ):
            module = getattr(match.func, "__module__", "")
            view_name = match.url_name or getattr(match.func, "__name__", "")
            if module in AUDITED_MODULES and view_name not in UNAUDITED_VIEWS:
                self._log(request, user, match, view_name, response.status_code)
        return response

    @staticmethod
    def _log(request, user, match, view_name, status_code):
        from base.security import client_ip
        from .models import AdminAuditLog

        object_id = next((str(v) for k, v in match.kwargs.items() if k in ("pk", "id") or k.endswith("_id") or k.endswith("_pk")), "")
        try:
            AdminAuditLog.objects.create(
                user=user, user_email=user.email[:254],
                action=_audit_action(view_name, request.method),
                method=request.method, path=request.get_full_path()[:500], view_name=view_name[:120],
                object_id=object_id[:64], status_code=status_code, ip_address=client_ip(request) or None,
            )
        except Exception:  # auditing must never break the admin action itself
            logger.exception("Could not write audit log entry")
