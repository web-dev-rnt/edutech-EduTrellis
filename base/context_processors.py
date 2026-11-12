from urllib.parse import urlencode

from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

# Pages that are part of the sign-in flow itself: never send the user "back" to these.
AUTH_URL_NAMES = {
    "login", "signup", "logout_user", "verify_otp", "resend_otp",
    "verify_reset_otp", "forgot_password_request", "reset_password",
}


def safe_next_url(request, url):
    """Return ``url`` if it is a same-site relative/absolute URL, else None."""
    if url and url_has_allowed_host_and_scheme(
        url=url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return url
    return None


def current_next(request):
    """The page a login/signup started from should return the user to."""
    match = getattr(request, "resolver_match", None)
    if match and match.url_name in AUTH_URL_NAMES:
        # Already on an auth page: keep whatever ``next`` it was given.
        return safe_next_url(request, request.GET.get("next") or request.POST.get("next"))
    path = request.get_full_path()
    return path if path != "/" else None


def auth_redirect(request):
    """Expose ``login_url`` / ``signup_url`` that bring the user back to this page."""
    next_url = current_next(request)
    query = f"?{urlencode({'next': next_url})}" if next_url else ""
    return {
        "login_url": reverse("login") + query,
        "signup_url": reverse("signup") + query,
        "auth_next": next_url or "",
    }
