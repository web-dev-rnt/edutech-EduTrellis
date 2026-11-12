import hashlib
import logging
import posixpath
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import dropbox
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile, File
from django.core.files.storage import FileSystemStorage, Storage
from django.core import signing
from django.db import DatabaseError, transaction
from django.urls import reverse
from django.templatetags.static import static
from django.utils.crypto import get_random_string
from django.utils.deconstruct import deconstructible
from dropbox.files import WriteMode


logger = logging.getLogger(__name__)


@deconstructible
class DropboxStorage(Storage):
    """Dropbox-backed storage with cached temporary download URLs."""

    BASE_PATH = "/elibrary"
    CHUNK_SIZE = 4 * 1024 * 1024
    URL_CACHE_SECONDS = 3 * 60 * 60 + 45 * 60
    MISSING_URL_CACHE_SECONDS = 5 * 60
    IMAGE_EXTENSIONS = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".webp"}

    def __init__(self):
        self._client = None

    @property
    def client(self):
        """Initialize the network client lazily instead of during Django import."""
        if self._client is None:
            credentials = (
                settings.DROPBOX_REFRESH_TOKEN,
                settings.DROPBOX_APP_KEY,
                settings.DROPBOX_APP_SECRET,
            )
            if not all(credentials):
                raise ImproperlyConfigured(
                    "Dropbox credentials must be configured through environment variables."
                )
            self._client = dropbox.Dropbox(
                oauth2_refresh_token=settings.DROPBOX_REFRESH_TOKEN,
                app_key=settings.DROPBOX_APP_KEY,
                app_secret=settings.DROPBOX_APP_SECRET,
            )
        return self._client

    def _clean_path(self, name):
        name = str(name).replace("\\", "/")
        name = re.sub(r"[^a-zA-Z0-9._/-]", "_", name)
        while "//" in name:
            name = name.replace("//", "/")
        return f"{self.BASE_PATH}/{name.lstrip('/')}"

    def _url_cache_key(self, path):
        digest = hashlib.sha256(path.encode("utf-8")).hexdigest()
        return f"dropbox-url:{digest}"

    def _is_configured(self):
        return all((
            settings.DROPBOX_REFRESH_TOKEN,
            settings.DROPBOX_APP_KEY,
            settings.DROPBOX_APP_SECRET,
        ))

    def _fallback_url(self, name):
        extension = f".{str(name).replace('\\', '/').rsplit('.', 1)[-1].lower()}"
        if extension in self.IMAGE_EXTENSIONS:
            return static("img/default-thumb.jpg")
        return ""

    def _save(self, name, content):
        path = self._clean_path(name)
        file_size = content.size
        content.seek(0)

        if file_size <= self.CHUNK_SIZE:
            self.client.files_upload(content.read(), path, mode=WriteMode.overwrite)
            cache.delete(self._url_cache_key(path))
            return name

        upload = self.client.files_upload_session_start(content.read(self.CHUNK_SIZE))
        cursor = dropbox.files.UploadSessionCursor(
            session_id=upload.session_id,
            offset=content.tell(),
        )
        commit = dropbox.files.CommitInfo(path=path, mode=WriteMode.overwrite)

        while content.tell() < file_size:
            remaining = file_size - content.tell()
            if remaining <= self.CHUNK_SIZE:
                self.client.files_upload_session_finish(
                    content.read(self.CHUNK_SIZE), cursor, commit
                )
            else:
                self.client.files_upload_session_append_v2(
                    content.read(self.CHUNK_SIZE), cursor
                )
                cursor.offset = content.tell()

        cache.delete(self._url_cache_key(path))
        return name

    def get_available_name(self, name, max_length=None):
        """A name no other file uses yet, so an upload never overwrites another course's file.

        Files are written in overwrite mode, so two uploads called e.g. "chapter1.pdf" used to replace each other.
        """
        name = str(name).replace("\\", "/")
        directory, file_name = posixpath.split(name)
        root, ext = posixpath.splitext(file_name)
        candidate = name
        while self._is_configured() and self.exists(candidate):
            candidate = posixpath.join(directory, f"{root}_{get_random_string(7)}{ext}")
        if max_length and len(candidate) > max_length:
            keep = max(1, max_length - len(directory) - len(ext) - 10)
            candidate = posixpath.join(directory, f"{root[:keep]}_{get_random_string(7)}{ext}")
        return candidate

    def exists(self, name):
        try:
            self.client.files_get_metadata(self._clean_path(name))
            return True
        except dropbox.exceptions.ApiError:
            return False

    def open(self, name, mode="rb"):
        if mode not in {"r", "rb"}:
            raise ValueError("DropboxStorage only supports read mode.")
        _, response = self.client.files_download(self._clean_path(name))
        return ContentFile(response.content, name=name)

    def url(self, name):
        """Return a local signed redirect URL without blocking page rendering."""
        if not name:
            return ""
        if not self._is_configured():
            return self._fallback_url(name)
        token = signing.dumps(str(name), salt="dropbox-media")
        return reverse("dropbox_file_redirect", kwargs={"token": token})

    def temporary_url(self, name):
        """Resolve and cache Dropbox's four-hour temporary URL."""
        if not name:
            return ""
        path = self._clean_path(name)
        cache_key = self._url_cache_key(path)
        cached_url = cache.get(cache_key)
        if cached_url:
            return cached_url

        try:
            link = self.client.files_get_temporary_link(path).link
        except Exception as exc:
            logger.warning("Unable to generate Dropbox URL for %s: %s", path, exc)
            fallback_url = self._fallback_url(name)
            if fallback_url:
                cache.set(cache_key, fallback_url, self.MISSING_URL_CACHE_SECONDS)
            return fallback_url

        cache.set(cache_key, link, self.URL_CACHE_SECONDS)
        return link

    def delete(self, name):
        path = self._clean_path(name)
        try:
            self.client.files_delete_v2(path)
        except dropbox.exceptions.ApiError:
            pass
        finally:
            cache.delete(self._url_cache_key(path))

    def size(self, name):
        return self.client.files_get_metadata(self._clean_path(name)).size


SHARING_UNAVAILABLE_KEY = "dropbox-sharing-unavailable"


def _links_db(query, default=None):
    """Run a DropboxFileLink query in its own savepoint.

    Files are also saved while migrations run (brand artwork), before the link table exists. A failed
    query there must not break the migration's transaction, so it is skipped and the link is created
    the first time the file is viewed.
    """
    try:
        with transaction.atomic():
            return query()
    except DatabaseError as exc:
        logger.info("Dropbox link table not available: %s", exc)
        return default


@deconstructible
class DropboxMediaStorage(DropboxStorage):
    """Default storage for every other upload: banners, logos, favicon, thumbnails, question images and so on.

    Files go to Dropbox under /media. Each one gets a permanent Dropbox link, saved in the database
    (base.DropboxFileLink), and pages point straight at that link. Rendering a page never calls Dropbox:
    a file without a saved link yet gets a link to /dropbox-media/<token>/, which creates the permanent
    link on first view (or, if the Dropbox app lacks the sharing.write permission, redirects to a
    four-hour temporary link).

    Files uploaded before Dropbox was the default still sit in MEDIA_ROOT; they are copied to Dropbox the
    first time they are viewed (or all at once with `manage.py upload_media_to_dropbox`). Without Dropbox
    credentials, or when Dropbox is unreachable during an upload, files are kept on local disk.
    """

    BASE_PATH = "/media"
    LINK_CACHE_SECONDS = 24 * 60 * 60
    SHARING_RETRY_SECONDS = 10 * 60

    def __init__(self):
        super().__init__()
        self.local = FileSystemStorage()

    # -- saving ------------------------------------------------------------------------------------
    def _save(self, name, content):
        if not self._is_configured():
            return self.local._save(name, content)
        try:
            name = super()._save(name, content)
        except Exception as exc:
            logger.warning("Dropbox upload failed for %s; keeping it on local disk: %s", name, exc)
            content.seek(0)
            return self.local._save(name, content)
        try:
            self.create_link(name)
        except Exception as exc:  # the file is safely in Dropbox; the link is created on first view
            logger.info("No permanent Dropbox link for %s yet: %s", name, exc)
        return name

    def get_available_name(self, name, max_length=None):
        if not self._is_configured():
            return self.local.get_available_name(name, max_length)
        return super().get_available_name(name, max_length)

    def _in_dropbox(self, name):
        return self._is_configured() and DropboxStorage.exists(self, name)

    def exists(self, name):
        return self.local.exists(name) or self._in_dropbox(name)

    def open(self, name, mode="rb"):
        return self.local.open(name, mode) if self.local.exists(name) else super().open(name, mode)

    def size(self, name):
        if self.local.exists(name):
            return self.local.size(name)
        try:
            return super().size(name)
        except Exception:
            return 0

    def delete(self, name):
        from base.models import DropboxFileLink

        if not name:
            return
        self.local.delete(name)
        if self._is_configured():
            super().delete(name)
        path = self._clean_path(name)
        _links_db(lambda: DropboxFileLink.objects.filter(path=path).delete())
        cache.delete(self._link_cache_key(name))

    # -- links ---------------------------------------------------------------------------------------
    def _link_cache_key(self, name):
        return "dropbox-link:" + hashlib.sha256(self._clean_path(name).encode("utf-8")).hexdigest()

    def saved_link(self, name):
        """The permanent link saved for this file, or "" (cache and database only; no network)."""
        from base.models import DropboxFileLink

        key = self._link_cache_key(name)
        link = cache.get(key)
        if link is None:
            path = self._clean_path(name)
            link = _links_db(
                lambda: DropboxFileLink.objects.filter(path=path).values_list("url", flat=True).first(), ""
            ) or ""
            if link:
                cache.set(key, link, self.LINK_CACHE_SECONDS)
        return link

    def url(self, name):
        if not name:
            return ""
        if not self._is_configured():
            return self.local.url(name)
        return self.saved_link(name) or reverse(
            "dropbox_media_redirect", kwargs={"token": signing.Signer(salt="dropbox-public-media").sign_object(str(name))}
        )

    def upload_local_copy(self, name):
        """Copy a file that is still on local disk into Dropbox. Returns False if there is nothing to copy."""
        if self._in_dropbox(name):
            return True
        if not self.local.exists(name):
            return False
        with self.local.open(name, "rb") as fh:
            DropboxStorage._save(self, name, File(fh, name=name))
        return True

    def create_link(self, name):
        """Create (or fetch) the file's permanent Dropbox link and save it in the database."""
        from base.models import DropboxFileLink

        if cache.get(SHARING_UNAVAILABLE_KEY):
            raise PermissionError("The Dropbox app is missing the sharing.write permission.")
        path = self._clean_path(name)
        try:
            link = self.client.sharing_create_shared_link_with_settings(path).url
        except dropbox.exceptions.AuthError as exc:
            cache.set(SHARING_UNAVAILABLE_KEY, True, self.SHARING_RETRY_SECONDS)
            raise PermissionError("The Dropbox app is missing the sharing.write permission.") from exc
        except dropbox.exceptions.ApiError as exc:
            if not exc.error.is_shared_link_already_exists():
                raise
            existing = exc.error.get_shared_link_already_exists()
            if existing is not None and existing.is_metadata():
                link = existing.get_metadata().url
            else:
                link = self.client.sharing_list_shared_links(path=path, direct_only=True).links[0].url
        link = direct_link(link)
        _links_db(lambda: DropboxFileLink.objects.update_or_create(path=path, defaults={"name": str(name)[:512], "url": link}))
        cache.set(self._link_cache_key(name), link, self.LINK_CACHE_SECONDS)
        return link

    def resolve(self, name):
        """(url, permanent) for the redirect view: uploads a local-only file, then links it."""
        link = self.saved_link(name)
        if link:
            return link, True
        if not self.upload_local_copy(name):
            return "", False
        try:
            return self.create_link(name), True
        except Exception as exc:
            logger.info("Using a temporary Dropbox link for %s: %s", name, exc)
        return self.temporary_url(name), False


def direct_link(link):
    """Turn a Dropbox share-page link into one that serves the file itself (for <img>, <video>, favicons)."""
    parts = urlsplit(link)
    query = [(key, value) for key, value in parse_qsl(parts.query) if key not in ("dl", "raw")]
    query.append(("raw", "1"))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), ""))


def media_file_names():
    """Every file name stored in an image/file field that uses DropboxMediaStorage."""
    from django.apps import apps
    from django.db import models

    names = set()
    for model in apps.get_models():
        for field in model._meta.get_fields():
            if isinstance(field, models.FileField) and isinstance(field.storage, DropboxMediaStorage):
                rows = model._default_manager.exclude(**{field.name: ""}).exclude(**{f"{field.name}__isnull": True})
                names.update(rows.values_list(field.name, flat=True))
    return sorted(names)


def sync_local_media(log=None):
    """Copy every uploaded file that is only on this server's disk into Dropbox, so backups are complete.

    Returns {'total', 'copied', 'missing', 'failed'}. Files already in Dropbox are skipped.
    """
    storage = DropboxMediaStorage()
    result = {"total": 0, "copied": 0, "missing": 0, "failed": 0}
    if not storage._is_configured():
        return result
    for name in media_file_names():
        result["total"] += 1
        try:
            if storage._in_dropbox(name):
                continue
            if storage.upload_local_copy(name):
                result["copied"] += 1
            else:
                result["missing"] += 1
                if log:
                    log(f"missing: {name}")
        except Exception as exc:
            result["failed"] += 1
            logger.warning("Could not copy %s to Dropbox: %s", name, exc)
            if log:
                log(f"failed: {name}: {exc}")
    return result

