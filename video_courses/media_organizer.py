"""Keep every uploaded site file in its proper Dropbox folder, with its permanent link saved.

Folder layout (all under /media in the Dropbox app folder; each model field's upload_to decides it):

    site/navbar/logo/  site/navbar/favicon/  site/footer/logo/  site/about/  site/auth-pages/
    site/banners/desktop/  site/banners/mobile/  site/stat-icons/  site/cta/  site/developer/
    bundles/thumbnails/  bundles/banners/  users/profile-pictures/
    test-series/thumbnails/  test-series/questions/  test-series/solutions/
    live-classes/banners/desktop/  live-classes/banners/mobile/
    video-courses/<course>/thumbnail/  video-courses/<course>/video-thumbnails/  video-courses/instructors/
    elibrary/covers/

Paid videos and PDFs are not touched: they stay in the private /elibrary storage with expiring links.

For each file in the database this:
  1. copies it into the folder its field now uses, if it is somewhere else (an old folder, the old
     /elibrary storage, or only on this server's disk), and points the database row at the new name;
  2. uploads it if it is only on local disk;
  3. creates its permanent Dropbox link and saves it in base.DropboxFileLink.

Files are copied, never moved or deleted: the local and live databases share one Dropbox, so the old
copy must stay until both have been organised. Safe to run again; finished files cost no Dropbox calls.
"""
import posixpath

from django.apps import apps
from django.core.cache import cache
from django.core.files import File
from django.db import models

from .dropbox_storage import DropboxMediaStorage, DropboxStorage

# Site caches that hold model rows (and so file names) for a few minutes.
CACHE_KEYS = (
    "site-theme-settings-v1", "site-theme-settings-v2", "site-navbar-settings-v3",
    "site-footer-settings-v3", "site-auth-page-settings-v1", "home-test-series-stats",
)


def media_fields():
    """(model, field) for every file field stored in the Dropbox media storage."""
    for model in apps.get_models():
        for field in model._meta.get_fields():
            if isinstance(field, models.FileField) and isinstance(field.storage, DropboxMediaStorage):
                yield model, field


def _list_paths(client, root):
    """{path_lower: content_hash} for every file under root (one paginated listing, not a call per file)."""
    import dropbox

    found = {}
    try:
        result = client.files_list_folder(root, recursive=True)
    except dropbox.exceptions.ApiError:
        return found  # the folder does not exist yet
    while True:
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                found[entry.path_lower] = entry.content_hash
        if not result.has_more:
            return found
        result = client.files_list_folder_continue(result.cursor)


class Organizer:
    def __init__(self, apply=True, log=print, fields=None):
        self.apply = apply
        self.log = log
        self.fields = fields
        self.storage = DropboxMediaStorage()
        self.legacy = DropboxStorage()  # the private storage course pictures used to live in
        self.stats = dict(files=0, moved=0, uploaded=0, linked=0, already_linked=0, unlinked=0, missing=0, failed=0)
        self.sharing_error = None
        self._paths = None

    @property
    def paths(self):
        if self._paths is None:
            client = self.storage.client
            self._paths = {**_list_paths(client, DropboxStorage.BASE_PATH), **_list_paths(client, DropboxMediaStorage.BASE_PATH)}
        return self._paths

    def in_dropbox(self, path):
        return path.lower() in self.paths

    def run(self):
        for model, field in (self.fields or media_fields()):
            rows = model._default_manager.exclude(**{field.name: ""}).exclude(**{f"{field.name}__isnull": True})
            for obj in rows.iterator():
                self.stats["files"] += 1
                name = getattr(obj, field.name).name
                try:
                    self.organize(model, field, obj, name)
                except Exception as exc:  # one bad file must not stop the rest
                    self.stats["failed"] += 1
                    self.log(f"FAILED {model._meta.label}.{field.name} {name}: {exc}")
        if self.apply:
            cache.delete_many(CACHE_KEYS)
        return self.stats

    def target_name(self, field, obj, name):
        """Where the field's upload_to puts this file now; the current name if it is already there."""
        wanted = field.generate_filename(obj, posixpath.basename(name)).replace("\\", "/")  # Windows
        return name if posixpath.dirname(wanted) == posixpath.dirname(name) else wanted

    def organize(self, model, field, obj, name):
        label = f"{model._meta.label}.{field.name}"
        target = self.target_name(field, obj, name)
        if target == name and self.storage.saved_link(name):
            self.stats["already_linked"] += 1
            return
        final = self.place(name, target, label)
        if final is None:
            self.stats["missing"] += 1
            self.log(f"MISSING {label} {name}: not in Dropbox or on this server's disk")
            return
        if final != name:
            self.stats["moved"] += 1
            self.log(f"{'moved' if self.apply else 'would move'} {label}: {name} -> {final}")
            if self.apply:
                model._default_manager.filter(pk=obj.pk).update(**{field.name: final})
        self.link(final, label)

    def place(self, name, target, label):
        """Make sure the file is in Dropbox at `target`; returns the name it ends up under (or None)."""
        storage = self.storage
        sources = [storage._clean_path(name), self.legacy._clean_path(name)]
        source = next((path for path in sources if self.in_dropbox(path)), None)
        local = storage.local.exists(name)
        if source is None and not local:
            return None
        dest = storage._clean_path(target)
        if target != name and self.in_dropbox(dest):
            if source and self.paths[dest.lower()] == self.paths[source.lower()]:
                return target  # already copied (e.g. by the other database)
            target = storage.get_available_name(target)
            dest = storage._clean_path(target)
        if source is None:  # only on this server's disk
            self.stats["uploaded"] += 1
            self.log(f"{'uploaded' if self.apply else 'would upload'} {label}: {target}")
            if self.apply:
                with storage.local.open(name, "rb") as fh:
                    DropboxStorage._save(storage, target, File(fh, name=target))
                self.paths[dest.lower()] = None
            return target
        if source.lower() != dest.lower() and self.apply:
            storage.client.files_copy_v2(source, dest)
            self.paths[dest.lower()] = self.paths[source.lower()]
        return target

    def link(self, name, label):
        if self.storage.saved_link(name):
            self.stats["already_linked"] += 1
            return
        if self.sharing_error or not self.apply:
            self.stats["unlinked"] += 1
            return
        try:
            self.storage.create_link(name)
            self.stats["linked"] += 1
        except PermissionError as exc:
            self.sharing_error = exc
            self.stats["unlinked"] += 1
        except Exception as exc:
            self.stats["unlinked"] += 1
            self.log(f"no link for {label} {name}: {exc}")


def organize_media(apply=True, log=print, fields=None):
    organizer = Organizer(apply=apply, log=log, fields=fields)
    stats = organizer.run()
    return stats, organizer.sharing_error
