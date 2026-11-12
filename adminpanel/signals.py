"""Audit-log staff logins and every failed login attempt."""
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver


def _ip(request):
    if request is None:
        return None
    from base.security import client_ip
    return client_ip(request) or None


@receiver(user_logged_in, dispatch_uid="audit-staff-login")
def audit_staff_login(sender, request, user, **kwargs):
    if not user.is_staff:
        return
    from .models import AdminAuditLog
    AdminAuditLog.objects.create(
        user=user, user_email=user.email[:254], action="login", method="POST",
        path=(request.path[:500] if request else ""), ip_address=_ip(request), status_code=200,
    )


@receiver(user_login_failed, dispatch_uid="audit-login-failed")
def audit_login_failed(sender, credentials, request=None, **kwargs):
    from .models import AdminAuditLog
    email = str(credentials.get("username") or credentials.get("email") or "")[:254]
    AdminAuditLog.objects.create(
        user_email=email, action="login_failed", method="POST",
        path=(request.path[:500] if request else ""), ip_address=_ip(request), status_code=401,
    )
