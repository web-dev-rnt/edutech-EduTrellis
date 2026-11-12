"""
Django settings for the Infinite360 project (Django 5.2+ ready).
Optimized for performance, caching, security, and Core Web Vitals.
"""

from pathlib import Path
import os
import sys
import dj_database_url

try:
    from dotenv import load_dotenv
except ImportError:  # python-dotenv is optional; real environment variables still work
    load_dotenv = None

# --------------------
# BASE SETTINGS
# --------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Local secrets live in .env (git-ignored). Variables already set in the environment win.
if load_dotenv:
    load_dotenv(BASE_DIR / ".env")

# SECURITY
# Project secret key, kept in the code. A DJANGO_SECRET_KEY set on the server still takes priority.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or "r+a1=de2k9k%lrf6!hgq5-n3knqj4)vwc4b5ztdoyh5sig=k41"

# Off unless explicitly enabled: production must never run with DEBUG (it disables every
# HTTPS/cookie protection below and shows settings on error pages). Set DJANGO_DEBUG=True in .env locally.
DEBUG = os.environ.get("DJANGO_DEBUG", "False").strip().lower() in ("1", "true", "yes")


ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1,testserver,www.thevedaeducation.info,"
        "ganeshsirclasses.online,www.ganeshsirclasses.online,"
        "indoretutorials.online,www.indoretutorials.online,"
        "exams.edutrellis.in,www.exams.edutrellis.in,"
        "web-production-ab46.up.railway.app,infinite360-production.up.railway.app",
    ).split(",")
    if host.strip()
]

# Domains that must always work, even when ALLOWED_HOSTS is set on the server and replaces the list above:
# the exam domains, the Railway app, and whatever public domain Railway gives this service.
RAILWAY_HOSTS = [
    host for host in (
        "infinite360-production.up.railway.app",
        os.environ.get("RAILWAY_PUBLIC_DOMAIN", "").strip(),
        os.environ.get("RAILWAY_STATIC_URL", "").strip().removeprefix("https://"),
    ) if host
]
for host in ("exams.edutrellis.in", "www.exams.edutrellis.in", *RAILWAY_HOSTS):
    if host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(host)

# --------------------
# APPLICATIONS
# --------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",

    # Local apps
    "base",
    "live_class",
    "elibrary",
    "testseries",
    "video_courses",
    "adminpanel",
]

# --------------------
# MIDDLEWARE
# (GZipMiddleware first for maximum compression coverage)
# --------------------
MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "adminpanel.middleware.ManagementAccessMiddleware",
    "adminpanel.middleware.SecurityHeadersAndAuditMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "indore_tutorials.urls"

# --------------------
# TEMPLATES
# Cached template loader reduces template parsing overhead significantly
# --------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": False,  # Must be False when using loaders explicitly
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Custom context processors
                "adminpanel.context_processors.navbar_settings",
                "adminpanel.context_processors.footer_settings",
                "adminpanel.context_processors.site_contact",
                "adminpanel.context_processors.seo",
                "video_courses.context_processors.categories_context",
                "base.context_processors.auth_redirect",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                )
            ],
        },
    },
]

WSGI_APPLICATION = "indore_tutorials.wsgi.application"

# --------------------
# DATABASE
# CONN_MAX_AGE=600 enables persistent DB connections (no reconnect overhead per request)
# --------------------
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

if DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3":
    DATABASES["default"].setdefault("OPTIONS", {})["timeout"] = 20

# --------------------
# CACHING
# LocMemCache is zero-dependency and ideal for single-process deployments (Railway)
# --------------------
REDIS_URL = os.environ.get("REDIS_URL")
if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
            "TIMEOUT": 300,
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "indore-tutorials-cache",
            "TIMEOUT": 300,
            "OPTIONS": {"MAX_ENTRIES": 1000},
        }
    }

# --------------------
# SESSIONS
# cached_db backend: reads from fast cache, writes to DB for persistence
# --------------------
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "default"

# --------------------
# PASSWORD VALIDATION
# --------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------
# INTERNATIONALIZATION
# --------------------
LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# --------------------
# STATIC & MEDIA FILES
# --------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
if len(sys.argv) > 1 and sys.argv[1] == "test":
    # Data migrations copy banner artwork into MEDIA_ROOT; keep test runs out of the real media folder.
    import tempfile
    MEDIA_ROOT = Path(tempfile.mkdtemp(prefix="infinite360-test-media-"))

# WhiteNoise: serve compressed static files with aggressive browser caching (1 year)
# Uploaded files (banners, logos, favicon, thumbnails, question images...) are stored in Dropbox and
# linked from the database; see video_courses/dropbox_storage.py. Paid videos and PDFs use their own
# Dropbox storage with expiring links.
STORAGES = {
    "default": {
        "BACKEND": "video_courses.dropbox_storage.DropboxMediaStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
if len(sys.argv) > 1 and sys.argv[1] == "test":
    STORAGES["default"] = {"BACKEND": "django.core.files.storage.FileSystemStorage"}  # tests never touch Dropbox
WHITENOISE_MAX_AGE = 31536000
WHITENOISE_ALLOW_ALL_ORIGINS = True

# --------------------
# CUSTOM USER MODEL
# --------------------
AUTH_USER_MODEL = "base.User"

# --------------------
# SECURITY HEADERS
# --------------------
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

X_FRAME_OPTIONS = "DENY"

# Session & cookie hardening
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14  # two weeks unless "remember me" changes it
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"  # Razorpay checkout opens a popup
PERMISSIONS_POLICY = "camera=(self), microphone=(self), geolocation=(), payment=(self)"

# Behind Railway / PythonAnywhere the client IP arrives in X-Forwarded-For.
TRUST_X_FORWARDED_FOR = os.environ.get("TRUST_X_FORWARDED_FOR", "True").strip().lower() in ("1", "true", "yes")

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # larger uploads stream to a temp file
FILE_UPLOAD_PERMISSIONS = 0o644

# --------------------
# LOGIN / LOGOUT
# --------------------
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"
LOGIN_URL = "/login/"

# --------------------
# THIRD-PARTY INTEGRATIONS
# --------------------
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "")

# Live classes run on Jitsi. Default: the free public server meet.jit.si.
# Free public servers no longer allow embedding (since 2024 a meet.jit.si call embedded on another site ends after
# 5 minutes; meet.ffmuc.net blocks iframes since 2026), so on those the class opens in its own tab with no time limit.
# With a self-hosted Jitsi (set JITSI_DOMAIN) the class is embedded in the page instead.
#
# JaaS (Jitsi as a Service by 8x8, free up to 25 users a month): set the three JAAS_* variables and classes are
# embedded on 8x8.vc with admins as hosts automatically (no "log in to become a moderator" screen).
JAAS_APP_ID = os.environ.get("JAAS_APP_ID", "").strip()              # vpaas-magic-cookie-…
JAAS_API_KEY_ID = os.environ.get("JAAS_API_KEY_ID", "").strip()      # vpaas-magic-cookie-…/abc123
JAAS_PRIVATE_KEY = os.environ.get("JAAS_PRIVATE_KEY", "")            # PEM text; "\n" escapes are fine
if JAAS_PRIVATE_KEY.strip() and not JAAS_PRIVATE_KEY.strip().startswith("-----"):
    _key_file = Path(JAAS_PRIVATE_KEY.strip())                          # or a path to the .pk file
    JAAS_PRIVATE_KEY = _key_file.read_text() if _key_file.is_file() else JAAS_PRIVATE_KEY
JAAS_ENABLED = bool(JAAS_APP_ID and JAAS_API_KEY_ID and JAAS_PRIVATE_KEY.strip())

JITSI_DOMAIN = "8x8.vc" if JAAS_ENABLED else (
    os.environ.get("JITSI_DOMAIN", "meet.jit.si").strip().lower().removeprefix("https://").strip("/"))
JITSI_EMBED = JAAS_ENABLED or os.environ.get(
    "JITSI_EMBED", "false" if JITSI_DOMAIN in ("meet.jit.si", "meet.ffmuc.net") else "true"
).strip().lower() in ("1", "true", "yes")
if JITSI_EMBED:
    # The embedded meeting is a cross-origin iframe: let it use the camera, microphone and screen sharing.
    _jitsi = f'"https://{JITSI_DOMAIN}"'
    PERMISSIONS_POLICY = (f"camera=(self {_jitsi}), microphone=(self {_jitsi}), display-capture=(self {_jitsi}), "
                          "geolocation=(), payment=(self)")

# "Tutor" AI teacher chat. Key, model and options are edited in the admin panel (Tutor AI);
# this environment variable is only the fallback key when none is saved there.
TUTOR_API_KEY = os.environ.get("TUTOR_API_KEY") or "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"

# --------------------
# DEFAULTS
# --------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CSRF cookie readable by JS (needed for AJAX payment flow)
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False

# --------------------
# SEO
# Canonical public origin used for canonical links, Open Graph URLs and the sitemap.
# --------------------
# Defaults to the live Railway address; set SITE_URL once a custom domain is attached. Pointing this at a
# different domain than the one serving the login page makes Chrome treat the site as a phishing copy.
SITE_URL = (
    os.environ.get("SITE_URL", "").strip()
    or "https://" + (os.environ.get("RAILWAY_PUBLIC_DOMAIN", "").strip() or "infinite360-production.up.railway.app")
).rstrip("/")

# --------------------
# PWA SETTINGS
# --------------------
PWA_APP_NAME = 'Infinite360'
PWA_APP_DESCRIPTION = 'Online live classes, video courses, test series and e-library by Infinite360'
PWA_APP_THEME_COLOR = '#2459E0'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'portrait-primary'
PWA_APP_START_URL = '/'

PWA_APP_ICONS = [
    {'src': '/static/img/icon-192.png', 'sizes': '192x192'},
    {'src': '/static/img/icon-512.png', 'sizes': '512x512'},
]

# --------------------
# CSRF TRUSTED ORIGINS
# --------------------
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CSRF_TRUSTED_ORIGINS",
        "https://www.thevedaeducation.info,"
        "https://ganeshsirclasses.online,https://www.ganeshsirclasses.online,"
        "https://indoretutorials.online,https://www.indoretutorials.online,"
        "https://exams.edutrellis.in,https://www.exams.edutrellis.in,"
        "https://web-production-ab46.up.railway.app",
    ).split(",")
    if origin.strip()
]

for origin in (
    "https://exams.edutrellis.in",
    "https://www.exams.edutrellis.in",
    *(f"https://{host}" for host in RAILWAY_HOSTS),
):
    if origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(origin)

# --------------------
# DROPBOX STORAGE
# --------------------
# Only these accounts see Backup Management (backups, restore, upload, Dropbox credentials).
# Other super admins, such as admin@gmail.com, get every other admin option but not this one.
BACKUP_MANAGER_EMAILS = ["rnt@gmail.com"]

# Keys are kept in the code. A variable of the same name set on the server still takes priority.
DROPBOX_APP_KEY = os.environ.get("DROPBOX_APP_KEY") or "wgg2fsw5pf16x8q"
DROPBOX_APP_SECRET = os.environ.get("DROPBOX_APP_SECRET") or "38dg9gi6djz3zuu"
DROPBOX_REFRESH_TOKEN = os.environ.get("DROPBOX_REFRESH_TOKEN") or "Si57f7yXuB0AAAAAAAAAAZGrsYbd1YLQpvGHxlJES4DRvKr7mDfZo8xqLaJBTY_s"

# --------------------
# LOGGING
# --------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "base": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
