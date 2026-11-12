"""Copy every uploaded site file that is still on local disk into Dropbox and save its link.

Covers all image and file fields that use the default storage (banners, logos, favicon, thumbnails,
question images and so on). Safe to run again: files already in Dropbox are only linked.

    python manage.py upload_media_to_dropbox
"""
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import models

from video_courses.dropbox_storage import DropboxMediaStorage


class Command(BaseCommand):
    help = "Upload local media files to Dropbox and save their links in the database."

    def handle(self, *args, **options):
        storage = DropboxMediaStorage()
        if not storage._is_configured():
            raise CommandError("Dropbox keys are not configured.")

        names = set()
        for model in apps.get_models():
            for field in model._meta.get_fields():
                if isinstance(field, models.FileField) and isinstance(field.storage, DropboxMediaStorage):
                    values = model._default_manager.exclude(**{field.name: ""}).exclude(**{f"{field.name}__isnull": True})
                    names.update(values.values_list(field.name, flat=True))

        linked = uploaded_only = missing = 0
        for name in sorted(names):
            try:
                if not storage.upload_local_copy(name):
                    missing += 1
                    self.stdout.write(self.style.WARNING(f"  missing: {name}"))
                    continue
                if storage.saved_link(name):
                    linked += 1
                    continue
                storage.create_link(name)
                linked += 1
            except PermissionError:
                uploaded_only += 1
            except Exception as exc:
                self.stdout.write(self.style.ERROR(f"  failed: {name}: {exc}"))
        self.stdout.write(self.style.SUCCESS(
            f"{len(names)} files: {linked} in Dropbox with a saved link, "
            f"{uploaded_only} in Dropbox without a permanent link, {missing} missing."
        ))
        if uploaded_only:
            self.stdout.write(
                "Permanent links need the sharing.write permission on the Dropbox app "
                "(see `python manage.py dropbox_auth`). Until then those files use temporary links."
            )
