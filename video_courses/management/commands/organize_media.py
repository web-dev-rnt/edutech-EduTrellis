"""Put every uploaded image/file in its proper Dropbox folder and save its permanent link in the database.

    python manage.py organize_media            # do it
    python manage.py organize_media --dry-run  # only report what would change

Runs on every deploy (Procfile). See video_courses/media_organizer.py for the folder layout.
"""
from django.core.management.base import BaseCommand, CommandError

from video_courses.dropbox_storage import DropboxMediaStorage
from video_courses.media_organizer import organize_media


class Command(BaseCommand):
    help = "Organise uploaded files into their Dropbox folders and save their permanent links."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Report what would change without changing anything.")

    def handle(self, *args, dry_run=False, **options):
        if not DropboxMediaStorage()._is_configured():
            raise CommandError("Dropbox keys are not configured.")
        stats, sharing_error = organize_media(apply=not dry_run, log=lambda line: self.stdout.write(f"  {line}"))
        self.stdout.write(self.style.SUCCESS(
            f"{stats['files']} files: {stats['moved']} {'to move' if dry_run else 'moved'} into their folders, "
            f"{stats['uploaded']} {'to upload' if dry_run else 'uploaded'}, {stats['linked']} links saved, "
            f"{stats['already_linked']} already linked, {stats['missing']} missing, {stats['failed']} failed."
        ))
        if sharing_error:
            self.stdout.write(self.style.WARNING(
                f"{stats['unlinked']} files have no permanent link: the Dropbox app is missing the sharing.write "
                "permission. Turn it on in the Dropbox App Console (Permissions tab), run "
                "`python manage.py dropbox_auth` for a new token, set DROPBOX_REFRESH_TOKEN, then run this again. "
                "Until then these files are served from the server's disk cache."
            ))
