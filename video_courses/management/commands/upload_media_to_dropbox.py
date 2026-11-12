"""Copy every uploaded site file that is still on local disk into Dropbox.

Covers all image and file fields that use the default storage (banners, logos, favicon, thumbnails,
question images and so on). Safe to run again: files already in Dropbox are skipped. Backup Now on the
backup page does the same before every backup.

    python manage.py upload_media_to_dropbox
"""
from django.core.management.base import BaseCommand, CommandError

from video_courses.dropbox_storage import DropboxMediaStorage, sync_local_media


class Command(BaseCommand):
    help = "Upload local media files to Dropbox."

    def handle(self, *args, **options):
        if not DropboxMediaStorage()._is_configured():
            raise CommandError("Dropbox keys are not configured.")
        result = sync_local_media(log=lambda line: self.stdout.write(self.style.WARNING(f"  {line}")))
        self.stdout.write(self.style.SUCCESS(
            f"{result['total']} files: {result['copied']} copied to Dropbox, "
            f"{result['missing']} missing, {result['failed']} failed; the rest were already there."
        ))
