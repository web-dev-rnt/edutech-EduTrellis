# base/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate

# Permanent accounts, checked after every `migrate` (the Procfile runs it on every deploy):
# a missing account is recreated with its starting password, and an existing one is kept active, verified and
# in its role. Passwords are only set on creation, so a password changed on the site stays changed.
# Only password hashes live in the code. To create a new hash: python manage.py shell -c
#   "from django.contrib.auth.hashers import make_password; print(make_password('new-password'))"
PERMANENT_ACCOUNTS = [
    # email, first name, is_staff (admin panel), is_superuser (everything), starting password hash
    ('rnt@gmail.com', 'RNT', True, True,
     'pbkdf2_sha256$1000000$9Dd46VO7IBTKg2pWjiS4EM$l5KcCHisx2k/HaWKBKTSU5tRBreK58ETfFwdhAsMMw0='),
    ('admin@gmail.com', 'Admin', True, True,
     'pbkdf2_sha256$1000000$MzBQNb83O4hxYaCf3TfElo$/ahAJxpNN8cYXausHf6+RU0tAWIaOKirQwVXhxMKDOg='),
    ('student@gmail.com', 'Student', False, False,
     'pbkdf2_sha256$1000000$MzBQNb83O4hxYaCf3TfElo$/ahAJxpNN8cYXausHf6+RU0tAWIaOKirQwVXhxMKDOg='),
]


def ensure_permanent_accounts(sender, using="default", **kwargs):
    """Recreate any permanent account that is missing and keep each one active, verified and in its role."""
    from django.contrib.auth import get_user_model

    User = get_user_model()
    for email, first_name, staff, superuser, password_hash in PERMANENT_ACCOUNTS:
        user = User.objects.using(using).filter(email__iexact=email).first()
        if user is None:
            user = User(email=email, first_name=first_name, is_verified=True,
                        is_staff=staff, is_superuser=superuser, is_active=True)
            user.password = password_hash
            user.save(using=using)
            continue
        wanted = {'is_staff': staff, 'is_superuser': superuser, 'is_active': True, 'is_verified': True}
        changed = [field for field, value in wanted.items() if getattr(user, field) != value]
        if changed:
            for field in changed:
                setattr(user, field, wanted[field])
            user.save(using=using, update_fields=changed)


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

    def ready(self):
        import base.signals
        from base.search import connect_signals

        connect_signals()
        post_migrate.connect(ensure_permanent_accounts, sender=self, dispatch_uid="base-permanent-accounts")
