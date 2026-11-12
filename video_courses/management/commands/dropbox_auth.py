"""Get a new Dropbox refresh token, e.g. after adding the sharing.write permission to the app.

1. python manage.py dropbox_auth          -> prints a link; open it, click Allow, copy the code
2. python manage.py dropbox_auth <code>   -> prints the new refresh token for DROPBOX_REFRESH_TOKEN
"""
from django.conf import settings
from django.core.management.base import BaseCommand
from dropbox import DropboxOAuth2FlowNoRedirect


class Command(BaseCommand):
    help = "Authorise the Dropbox app and print a new refresh token."

    def add_arguments(self, parser):
        parser.add_argument("code", nargs="?", help="The code Dropbox shows after you click Allow.")

    def handle(self, *args, code=None, **options):
        flow = DropboxOAuth2FlowNoRedirect(
            settings.DROPBOX_APP_KEY, settings.DROPBOX_APP_SECRET, token_access_type="offline",
        )
        if not code:
            self.stdout.write("Open this link, click Allow, then run this command again with the code:\n")
            self.stdout.write(flow.start())
            return
        result = flow.finish(code.strip())
        self.stdout.write(self.style.SUCCESS("New refresh token (put it in DROPBOX_REFRESH_TOKEN):"))
        self.stdout.write(result.refresh_token)
        self.stdout.write(f"Permissions granted: {result.scope}")
