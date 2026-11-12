"""
Small security helpers shared by the auth, exam and contact views.

* rate_limit()      - fixed-window counters in the cache (works with LocMem or Redis)
* client_ip()       - the caller's IP, honouring the proxy header only when configured
* OTP brute-force   - count wrong codes per user and burn the code after a few misses
"""
import logging

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

OTP_MAX_FAILURES = 5
OTP_FAILURE_WINDOW = 15 * 60


def client_ip(request):
    """Client IP. Behind a proxy (Railway, PythonAnywhere) the first X-Forwarded-For hop is the client."""
    if getattr(settings, "TRUST_X_FORWARDED_FOR", False):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded:
            return forwarded.split(",")[0].strip()[:64]
    return request.META.get("REMOTE_ADDR", "")[:64]


def rate_limit(scope, ident, limit, window):
    """
    Count one hit for (scope, ident) and return True when the caller is over `limit`
    hits within `window` seconds. Identity is usually an IP or a normalised email.
    """
    if not ident:
        return False
    key = f"rl:{scope}:{ident}"
    if cache.add(key, 1, window):
        return False
    try:
        count = cache.incr(key)
    except ValueError:  # expired between add() and incr()
        cache.add(key, 1, window)
        return False
    if count > limit:
        if count == limit + 1:
            logger.warning("Rate limit hit: scope=%s ident=%s", scope, ident)
        return True
    return False


def is_rate_limited(request, scope, limit, window, extra_ident=None):
    """Rate-limit by client IP and, when given, by a second identity such as the email address."""
    limited = rate_limit(scope, client_ip(request), limit, window)
    if extra_ident:
        # Per-account limit is stricter in spirit: it can't be dodged by changing IP.
        limited = rate_limit(f"{scope}:acct", str(extra_ident).lower(), limit, window) or limited
    return limited


def reset_rate_limit(scope, ident):
    cache.delete(f"rl:{scope}:{ident}")


# ── OTP brute force ─────────────────────────────────────────────────────────

def _otp_key(user_id, kind):
    return f"otp-fail:{kind}:{user_id}"


def otp_locked(user_id, kind):
    return (cache.get(_otp_key(user_id, kind)) or 0) >= OTP_MAX_FAILURES


def record_otp_failure(user_id, kind):
    """Count a wrong code; after OTP_MAX_FAILURES the outstanding codes are burned."""
    from base.models import OTPVerification

    key = _otp_key(user_id, kind)
    cache.add(key, 0, OTP_FAILURE_WINDOW)
    try:
        failures = cache.incr(key)
    except ValueError:
        cache.set(key, 1, OTP_FAILURE_WINDOW)
        failures = 1
    if failures >= OTP_MAX_FAILURES:
        OTPVerification.objects.filter(user_id=user_id, verification_type=kind, is_used=False).update(is_used=True)
        logger.warning("OTP locked after %s failures: user=%s type=%s", failures, user_id, kind)
    return failures


def clear_otp_failures(user_id, kind):
    cache.delete(_otp_key(user_id, kind))
