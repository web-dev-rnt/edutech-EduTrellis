"""One-off setup of the permanent accounts on every existing database (local and production).

Runs once per database. If an account already exists (admin@gmail.com did), its role and password are set to
the ones below. Afterwards base.apps.ensure_permanent_accounts keeps the accounts present and in their roles on
every `migrate`, without touching passwords again. Only password hashes are stored here.
"""
from django.db import migrations

ACCOUNTS = [
    # email, first name, last name, is_staff, is_superuser, password hash
    ('rnt@gmail.com', 'RNT', '', True, True,
     'pbkdf2_sha256$1000000$9Dd46VO7IBTKg2pWjiS4EM$l5KcCHisx2k/HaWKBKTSU5tRBreK58ETfFwdhAsMMw0='),
    ('admin@gmail.com', 'Admin', '', True, True,
     'pbkdf2_sha256$1000000$MzBQNb83O4hxYaCf3TfElo$/ahAJxpNN8cYXausHf6+RU0tAWIaOKirQwVXhxMKDOg='),
    ('student@gmail.com', 'Student', '', False, False,
     'pbkdf2_sha256$1000000$MzBQNb83O4hxYaCf3TfElo$/ahAJxpNN8cYXausHf6+RU0tAWIaOKirQwVXhxMKDOg='),
]


def create_accounts(apps, schema_editor):
    User = apps.get_model('base', 'User')
    for email, first, last, staff, superuser, password in ACCOUNTS:
        user = User.objects.filter(email__iexact=email).first() or User(email=email)
        user.first_name = user.first_name or first
        user.last_name = user.last_name or last
        user.is_staff = staff
        user.is_superuser = superuser
        user.is_active = True
        user.is_verified = True
        user.password = password
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_daily_quiz_attempt'),
    ]

    operations = [
        migrations.RunPython(create_accounts, migrations.RunPython.noop),
    ]
