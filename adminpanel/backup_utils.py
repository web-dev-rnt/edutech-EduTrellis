"""
adminpanel/backup_utils.py
Dropbox backup manager for the site database.
Uses the Dropbox OAuth2 credentials already configured in settings.
"""
from __future__ import annotations

import os
import logging
import re
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.cache import cache

from .branding import brand, default_backup_folder

logger = logging.getLogger(__name__)

DB_PATH = str(Path(settings.BASE_DIR) / "db.sqlite3")  # kept for older imports; see db_path()
UPLOAD_PIECE_BYTES = 8 * 1024 * 1024


def is_sqlite() -> bool:
    return settings.DATABASES["default"]["ENGINE"].endswith("sqlite3")


def db_path() -> str:
    """The SQLite file the site is really using (DATABASE_URL can point somewhere else)."""
    return str(settings.DATABASES["default"]["NAME"])


def active_database_label() -> str:
    if is_sqlite():
        return os.path.basename(db_path())
    engine = settings.DATABASES["default"]["ENGINE"].rsplit(".", 1)[-1]
    return {"postgresql": "PostgreSQL", "mysql": "MySQL"}.get(engine, engine)


def restore_marker_path() -> str:
    """Touched after every restore so each server process drops its cached pages and data."""
    return db_path() + ".restored"


def _snapshot(dest_path: str) -> None:
    """A consistent copy of the live database, even while the site is writing to it."""
    import sqlite3

    source = sqlite3.connect(db_path(), timeout=60)
    target = sqlite3.connect(dest_path)
    try:
        source.backup(target)
    finally:
        target.close()
        source.close()


def _noop_progress(*args, **kwargs):
    pass


def _retry(call, attempts=4):
    """Run a Dropbox call, retrying network hiccups and rate limits with a growing pause."""
    import time

    import dropbox  # type: ignore

    for attempt in range(attempts):
        try:
            return call()
        except (dropbox.exceptions.InternalServerError, dropbox.exceptions.RateLimitError, OSError) as exc:
            if attempt == attempts - 1:
                raise
            wait = getattr(exc, "backoff", None) or 2 * (attempt + 1)
            logger.warning("Dropbox call failed (%s); retrying in %ss", exc, wait)
            time.sleep(wait)


def _upload_file(dbx, local_path: str, dropbox_path: str, progress=_noop_progress) -> None:
    """Upload a file of any size in pieces (a single request is limited to 150 MB)."""
    import dropbox  # type: ignore
    from dropbox.files import WriteMode  # type: ignore

    size = os.path.getsize(local_path)
    progress(done=0, total=size)
    with open(local_path, "rb") as fh:
        first = fh.read(UPLOAD_PIECE_BYTES)
        session_id = _retry(lambda: dbx.files_upload_session_start(first)).session_id
        progress(done=fh.tell(), total=size)
        while fh.tell() < size:
            offset = fh.tell()
            piece = fh.read(UPLOAD_PIECE_BYTES)
            cursor = dropbox.files.UploadSessionCursor(session_id=session_id, offset=offset)
            _retry(lambda: dbx.files_upload_session_append_v2(piece, cursor))
            progress(done=fh.tell(), total=size)
        cursor = dropbox.files.UploadSessionCursor(session_id=session_id, offset=size)
        commit = dropbox.files.CommitInfo(path=dropbox_path, mode=WriteMode.overwrite)
        _retry(lambda: dbx.files_upload_session_finish(b"", cursor, commit))


def _download_file(dbx, dropbox_path: str, local_path: str, progress=_noop_progress) -> None:
    """Download a file in a stream, reporting progress, into local_path."""
    metadata, response = _retry(lambda: dbx.files_download(dropbox_path))
    done = 0
    progress(done=0, total=metadata.size)
    try:
        with open(local_path, "wb") as fh:
            for piece in response.iter_content(chunk_size=1024 * 1024):
                fh.write(piece)
                done += len(piece)
                progress(done=done, total=metadata.size)
    finally:
        response.close()
    if done != metadata.size:
        raise RuntimeError(f"The download stopped early ({_human_size(done)} of {_human_size(metadata.size)}). Please try again.")


def load_into_live_database(source_path: str, progress=_noop_progress) -> None:
    """Make the site use the database in `source_path`.

    The backup is copied into the live database file in place (SQLite's backup API) rather than swapping
    files: a swapped file stays invisible to server processes that already have the old one open, so the
    site kept showing the old content. Afterwards the database is migrated to the current code (backups
    from older versions), caches are cleared, and the restore marker tells every other process to do the same.
    """
    import sqlite3

    from django.core.management import call_command
    from django.db import connections

    progress("Checking the backup file", force=True)
    check_sqlite_file(source_path)
    progress("Loading it into the site")
    connections.close_all()
    source = sqlite3.connect(f"file:{source_path}?mode=ro", uri=True)
    target = sqlite3.connect(db_path(), timeout=60)
    try:
        source.backup(target)
    finally:
        target.close()
        source.close()
    connections.close_all()
    progress("Updating the database to this version of the site")
    call_command("migrate", interactive=False, verbosity=0)
    cache.clear()
    Path(restore_marker_path()).touch()
# The listing is three Dropbox round trips (~2.5s); cache it and clear it on every change.
BACKUP_LIST_CACHE_KEY = "dropbox-backup-list-v1"
BACKUP_LIST_TIMEOUT = 60 * 10


def clear_backup_list_cache():
    cache.delete(BACKUP_LIST_CACHE_KEY)


def _credentials():
    """Use the active admin-saved configuration, falling back to settings (and the chosen folder)."""
    from .models import BackupPreference, DropboxConfiguration

    config = DropboxConfiguration.objects.filter(is_active=True).first()
    if config:
        return config.app_key, config.app_secret, config.refresh_token, config.backup_folder
    return (
        settings.DROPBOX_APP_KEY,
        settings.DROPBOX_APP_SECRET,
        settings.DROPBOX_REFRESH_TOKEN,
        BackupPreference.get_solo().folder or default_backup_folder(),
    )


def backup_folder() -> str:
    return _credentials()[3]


def normalize_folder(value: str) -> str:
    """'My Backups/' -> '/My Backups'. Raises ValueError for an unusable folder name."""
    value = (value or "").strip().replace("\\", "/").strip("/")
    if not value or ".." in value.split("/") or len(value) > 200 or not re.fullmatch(r"[A-Za-z0-9 _().&@+-]+(/[A-Za-z0-9 _().&@+-]+)*", value):
        raise ValueError("Use letters, numbers, spaces, - and _ for the folder name (e.g. /edutrellis-backup).")
    return "/" + value


def _client(app_key, app_secret, refresh_token):
    import dropbox  # type: ignore

    return dropbox.Dropbox(oauth2_refresh_token=refresh_token, app_key=app_key, app_secret=app_secret, timeout=120)


def check_credentials(app_key, app_secret, refresh_token) -> str:
    """Raise RuntimeError unless the credentials work. Returns the account's display name."""
    try:
        return _client(app_key, app_secret, refresh_token).users_get_current_account().name.display_name
    except Exception as exc:
        raise RuntimeError(f"Dropbox did not accept these credentials: {exc}")


# A checked client is reused for a few minutes: each check is a token refresh plus an account lookup.
_CLIENT_CACHE: dict = {}
CLIENT_REUSE_SECONDS = 5 * 60


def _get_dbx():
    """Return an authenticated Dropbox client, auto-refreshing the token."""
    import time

    try:
        import dropbox  # type: ignore  # noqa: F401
        app_key, app_secret, refresh_token, _ = _credentials()
        key = (app_key, app_secret, refresh_token)
        cached = _CLIENT_CACHE.get(key)
        if cached and time.monotonic() - cached[1] < CLIENT_REUSE_SECONDS:
            return cached[0]
        dbx = _client(app_key, app_secret, refresh_token)
        dbx.users_get_current_account()  # validates credentials
        _CLIENT_CACHE.clear()
        _CLIENT_CACHE[key] = (dbx, time.monotonic())
        return dbx
    except ImportError:
        raise RuntimeError("dropbox SDK not installed. Run: pip install dropbox")
    except Exception as exc:
        raise RuntimeError(f"Cannot authenticate with Dropbox: {exc}")


def _ensure_folder(dbx) -> None:
    """Create the backup folder on Dropbox if it does not already exist."""
    try:
        import dropbox  # type: ignore
        folder = backup_folder()
        dbx.files_get_metadata(folder)
    except Exception:
        try:
            import dropbox  # type: ignore
            dbx.files_create_folder_v2(folder)
            logger.info("Created Dropbox folder: %s", folder)
        except Exception as exc:
            # Folder may have been created concurrently – ignore
            logger.warning("Could not create Dropbox folder: %s", exc)


def _human_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 ** 2):.2f} MB"


class DropboxBackupManager:
    """High-level helper for database backup operations on Dropbox."""

    # ------------------------------------------------------------------ #
    #  CREATE                                                              #
    # ------------------------------------------------------------------ #
    @staticmethod
    def create_backup(progress=_noop_progress, label: str = "backup") -> dict:
        """
        Back up everything: copy uploaded files still on local disk into Dropbox (the database only stores
        their names), then upload a consistent snapshot of the database with a timestamped filename.
        `label` names the file (<site>_<label>_<time>.sqlite3), e.g. "before_restore" for safety copies.
        Returns a dict with keys: success, filename, message.
        """
        if not is_sqlite():
            return {"success": False, "message": f"The site uses {active_database_label()}; only SQLite databases can be backed up here."}
        if not os.path.exists(db_path()):
            return {"success": False, "message": f"Database file not found: {db_path()}"}

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{brand()['slug'].replace('-', '_')}_{label}_{timestamp}.sqlite3"
        dropbox_path = f"{backup_folder()}/{filename}"
        snapshot = db_path() + f".backup-snapshot-{timestamp}"

        try:
            from video_courses.dropbox_storage import sync_local_media

            progress("Connecting to Dropbox")
            dbx = _get_dbx()
            _ensure_folder(dbx)
            progress("Copying uploaded images to Dropbox")
            media = sync_local_media()
            progress("Taking a snapshot of the database")
            _snapshot(snapshot)
            size = os.path.getsize(snapshot)
            progress("Uploading to Dropbox", done=0, total=size)
            _upload_file(dbx, snapshot, dropbox_path, progress)
            file_size = _human_size(size)
            logger.info("Backup uploaded: %s (%s)", dropbox_path, file_size)
            clear_backup_list_cache()
            note = f" {media['copied']} image/file(s) copied to Dropbox." if media["copied"] else ""
            if media["missing"]:
                note += f" {media['missing']} file(s) listed in the database were not found anywhere."
            return {
                "success": True,
                "filename": filename,
                "size": size,
                "message": f"Backup '{filename}' ({file_size}) uploaded successfully.{note}",
            }
        except Exception as exc:
            logger.error("Backup failed: %s", exc)
            return {"success": False, "message": str(exc)}
        finally:
            if os.path.exists(snapshot):
                os.remove(snapshot)

    # ------------------------------------------------------------------ #
    #  LIST                                                                #
    # ------------------------------------------------------------------ #
    @staticmethod
    def list_backups() -> list[dict]:
        """
        Return a list of backup dicts sorted newest-first.
        Each dict: filename, path, size_bytes, size_human, modified (datetime).
        """
        cached = cache.get(BACKUP_LIST_CACHE_KEY)
        if cached is not None:
            return cached
        try:
            dbx = _get_dbx()
            _ensure_folder(dbx)
            result = dbx.files_list_folder(backup_folder())
            backups = []
            while True:
                for entry in result.entries:
                    import dropbox  # type: ignore
                    if isinstance(entry, dropbox.files.FileMetadata):
                        backups.append({
                            "filename": entry.name,
                            "path": entry.path_lower,
                            "size_bytes": entry.size,
                            "size_human": _human_size(entry.size),
                            "modified": entry.server_modified,
                            "kind": backup_kind(entry.name),
                        })
                if not result.has_more:
                    break
                result = dbx.files_list_folder_continue(result.cursor)

            backups.sort(key=lambda x: x["modified"], reverse=True)
            cache.set(BACKUP_LIST_CACHE_KEY, backups, BACKUP_LIST_TIMEOUT)
            return backups
        except Exception as exc:
            logger.error("Failed to list backups: %s", exc)
            return []

    # ------------------------------------------------------------------ #
    #  RESTORE                                                             #
    # ------------------------------------------------------------------ #
    @staticmethod
    def restore_backup(filename: str, progress=_noop_progress, safety_backup: bool = False) -> dict:
        """
        Download the specified backup from Dropbox and make the site use it. With safety_backup, the
        current database is backed up first, so the restore can be undone.
        Returns dict with keys: success, message (and safety_backup: the safety copy's file name).
        """
        if not is_sqlite():
            return {"success": False, "message": f"The site uses {active_database_label()}; a SQLite backup cannot be restored into it."}
        dropbox_path = f"{backup_folder()}/{filename}"
        tmp_path = db_path() + ".restore-download"
        safety_name = None
        try:
            if safety_backup:
                safety = DropboxBackupManager.create_backup(
                    lambda stage=None, **kw: progress(f"Safety backup: {stage}" if stage else None, **kw),
                    label="before_restore",
                )
                if not safety["success"]:
                    return {"success": False, "message": f"The safety backup failed, so nothing was restored: {safety['message']}"}
                safety_name = safety["filename"]
            progress("Downloading the backup from Dropbox", done=0, total=0)
            dbx = _get_dbx()
            _download_file(dbx, dropbox_path, tmp_path, progress)
            load_into_live_database(tmp_path, progress)
            logger.info("Database restored from: %s", dropbox_path)
            note = f" The previous data was saved as '{safety_name}'." if safety_name else ""
            return {"success": True, "message": f"Database restored from '{filename}' successfully.{note}",
                    "safety_backup": safety_name}
        except Exception as exc:
            logger.error("Restore failed: %s", exc)
            return {"success": False, "message": str(exc)}
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    # ------------------------------------------------------------------ #
    #  DOWNLOAD URL (temporary link)                                      #
    # ------------------------------------------------------------------ #
    @staticmethod
    def get_download_url(filename: str) -> dict:
        """
        Return a temporary direct download link (4 hour expiry) and the file size.
        Returns dict with keys: success, url, size / message.
        """
        dropbox_path = f"{backup_folder()}/{filename}"
        try:
            dbx = _get_dbx()
            link = dbx.files_get_temporary_link(dropbox_path)
            return {"success": True, "url": link.link, "size": link.metadata.size}
        except Exception as exc:
            logger.error("get_download_url failed: %s", exc)
            return {"success": False, "message": str(exc)}

    # ------------------------------------------------------------------ #
    #  DELETE                                                              #
    # ------------------------------------------------------------------ #
    @staticmethod
    def delete_backup(filename: str) -> dict:
        """
        Permanently delete a backup file from Dropbox.
        Returns dict with keys: success, message.
        """
        dropbox_path = f"{backup_folder()}/{filename}"
        try:
            dbx = _get_dbx()
            dbx.files_delete_v2(dropbox_path)
            logger.info("Deleted Dropbox backup: %s", dropbox_path)
            clear_backup_list_cache()
            return {"success": True, "message": f"Backup '{filename}' deleted successfully."}
        except Exception as exc:
            logger.error("Delete backup failed: %s", exc)
            return {"success": False, "message": str(exc)}


def backup_kind(filename: str) -> str:
    name = filename.lower()
    if "_before_restore_" in name:
        return "safety"
    if "_uploaded_" in name:
        return "uploaded"
    return "backup"


# ---------------------------------------------------------------------- #
#  CONNECTION STATUS AND FOLDERS                                          #
# ---------------------------------------------------------------------- #
def connection_status() -> dict:
    """Is Dropbox connected? Account, storage space, the backup folder and what is in it."""
    from .models import DropboxConfiguration

    saved = DropboxConfiguration.objects.filter(is_active=True).first()
    status = {
        "connected": False,
        "source": "Saved on this page" if saved else "Server settings (environment)",
        "folder": backup_folder(),
        "default_folder": default_backup_folder(),
    }
    try:
        dbx = _get_dbx()
        account = dbx.users_get_current_account()
        status.update(connected=True, account_name=account.name.display_name, account_email=account.email,
                      keep_last=_keep_last())
        try:
            space = dbx.users_get_space_usage()
            allocation = space.allocation
            allocated = (allocation.get_individual().allocated if allocation.is_individual()
                         else allocation.get_team().allocated)
            status.update(space_used=space.used, space_allocated=allocated)
        except Exception as exc:  # missing account_info.read scope or similar: not essential
            logger.info("Could not read Dropbox space usage: %s", exc)
        try:
            dbx.files_get_metadata(status["folder"])
            status["folder_exists"] = True
        except Exception:
            status["folder_exists"] = False
    except Exception as exc:
        status["error"] = str(exc)
        return status
    backups = DropboxBackupManager.list_backups()
    status.update(
        backup_count=len(backups),
        backup_bytes=sum(b["size_bytes"] for b in backups),
        latest=backups[0]["modified"].isoformat() if backups else None,
        latest_name=backups[0]["filename"] if backups else None,
    )
    return status


def backup_folders() -> list[dict]:
    """Top-level Dropbox folders that hold database backups (plus the current folder), with counts."""
    import dropbox  # type: ignore

    dbx = _get_dbx()
    current = backup_folder()
    candidates = {current.lower(): current}
    result = dbx.files_list_folder("")
    while True:
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FolderMetadata) and "backup" in entry.name.lower():
                candidates.setdefault(entry.path_lower, entry.path_display)
        if not result.has_more:
            break
        result = dbx.files_list_folder_continue(result.cursor)
    folders = []
    for key, path in candidates.items():
        count = size = 0
        latest = None
        try:
            listing = dbx.files_list_folder(path)
            while True:
                for entry in listing.entries:
                    if isinstance(entry, dropbox.files.FileMetadata) and entry.name.lower().endswith(UPLOAD_EXTENSIONS):
                        count += 1
                        size += entry.size
                        latest = max(latest, entry.server_modified) if latest else entry.server_modified
                if not listing.has_more:
                    break
                listing = dbx.files_list_folder_continue(listing.cursor)
            exists = True
        except dropbox.exceptions.ApiError:
            exists = False
        folders.append({
            "path": path, "count": count, "size_bytes": size, "size_human": _human_size(size),
            "latest": latest.isoformat() if latest else None, "current": key == current.lower(), "exists": exists,
        })
    folders.sort(key=lambda f: (not f["current"], -(f["count"] or 0), f["path"].lower()))
    return folders


def _keep_last() -> int:
    from .models import BackupPreference

    return BackupPreference.get_solo().keep_last


def apply_retention(progress=_noop_progress) -> list[str]:
    """Delete the oldest backups beyond the "keep last" setting. Uploaded files are never removed."""
    keep = _keep_last()
    if not keep:
        return []
    clear_backup_list_cache()
    backups = [b for b in DropboxBackupManager.list_backups() if b["kind"] in ("backup", "safety")]
    removed = []
    for old in backups[keep:]:  # newest first
        progress("Removing old backups")
        if DropboxBackupManager.delete_backup(old["filename"])["success"]:
            removed.append(old["filename"])
    return removed


def set_keep_last(value) -> int:
    from .models import BackupPreference

    keep = int(value)
    if keep < 0 or keep > 100:
        raise ValueError("Choose between 0 (keep all) and 100.")
    preference = BackupPreference.get_solo()
    preference.keep_last = keep
    preference.save()
    return keep


def set_backup_folder(folder: str) -> str:
    """Make `folder` the backup folder (creating it in Dropbox if needed). Returns the normalised path."""
    from .models import BackupPreference, DropboxConfiguration

    folder = normalize_folder(folder)
    dbx = _get_dbx()
    try:
        dbx.files_get_metadata(folder)
    except Exception:
        dbx.files_create_folder_v2(folder)
    saved = DropboxConfiguration.objects.filter(is_active=True).first()
    if saved:
        saved.backup_folder = folder
        saved.save(update_fields=["backup_folder", "updated_at"])
    preference = BackupPreference.get_solo()
    preference.folder = folder
    preference.save()
    clear_backup_list_cache()
    return folder


# ---------------------------------------------------------------------- #
#  MANUAL UPLOAD of a database file, sent from the browser in pieces      #
# ---------------------------------------------------------------------- #
SQLITE_HEADER = b"SQLite format 3\x00"
UPLOAD_EXTENSIONS = (".sqlite3", ".sqlite", ".db")
UPLOAD_CHUNK_BYTES = 8 * 1024 * 1024
MAX_UPLOAD_BYTES = 2 * 1024 ** 3
UPLOAD_TOKEN_SALT = "backup-upload"
UPLOAD_TOKEN_MAX_AGE = 24 * 60 * 60


class UploadError(Exception):
    def __init__(self, message, expected_offset=None):
        super().__init__(message)
        self.expected_offset = expected_offset


def _offset_error(exc):
    """The offset Dropbox expects, if `exc` is an "incorrect offset" upload error."""
    error = getattr(exc, "error", None)
    lookup = getattr(error, "get_incorrect_offset", None) if error is not None else None
    if lookup and error.is_incorrect_offset():
        return lookup().correct_offset
    return None


def upload_start(file_name: str, size: int, first_chunk: bytes, user_id: int) -> str:
    """Check the file looks like a SQLite database and open a Dropbox upload with its first piece."""
    from django.core import signing

    file_name = os.path.basename(file_name or "").strip()
    if not file_name.lower().endswith(UPLOAD_EXTENSIONS):
        raise UploadError("Choose a SQLite database file (.sqlite3, .sqlite or .db).")
    if size <= 0 or size > MAX_UPLOAD_BYTES:
        raise UploadError("The file must be between 1 byte and 2 GB.")
    if not first_chunk.startswith(SQLITE_HEADER):
        raise UploadError("This file is not a SQLite database.")
    if len(first_chunk) > UPLOAD_CHUNK_BYTES or len(first_chunk) > size:
        raise UploadError("Upload piece is too large.")
    dbx = _get_dbx()
    session_id = dbx.files_upload_session_start(first_chunk).session_id
    return signing.dumps(
        {"sid": session_id, "size": size, "name": file_name, "uid": user_id}, salt=UPLOAD_TOKEN_SALT,
    )


def _upload_state(token: str, user_id: int) -> dict:
    from django.core import signing

    try:
        state = signing.loads(token, salt=UPLOAD_TOKEN_SALT, max_age=UPLOAD_TOKEN_MAX_AGE)
    except signing.BadSignature:
        raise UploadError("This upload has expired. Please start again.")
    if state["uid"] != user_id:
        raise UploadError("This upload belongs to another account.")
    return state


def upload_append(token: str, user_id: int, data: bytes, offset: int) -> int:
    """Add the piece that starts at `offset`. Returns the new uploaded size."""
    import dropbox  # type: ignore

    state = _upload_state(token, user_id)
    if not data or len(data) > UPLOAD_CHUNK_BYTES or offset + len(data) > state["size"]:
        raise UploadError("Upload piece has the wrong size.")
    cursor = dropbox.files.UploadSessionCursor(session_id=state["sid"], offset=offset)
    try:
        _get_dbx().files_upload_session_append_v2(data, cursor)
    except Exception as exc:
        expected = _offset_error(exc)
        if expected is not None:
            raise UploadError("Out of step with Dropbox.", expected_offset=expected)
        raise
    return offset + len(data)


def upload_finish(token: str, user_id: int) -> str:
    """Save the uploaded file into the backup folder. Returns the backup's file name."""
    import dropbox  # type: ignore
    from dropbox.files import WriteMode  # type: ignore

    from .branding import brand

    state = _upload_state(token, user_id)
    folder = backup_folder()
    stem = re.sub(r"[^A-Za-z0-9_-]+", "_", os.path.splitext(state["name"])[0]).strip("_")[:40] or "database"
    prefix = brand()["slug"].replace("-", "_")
    filename = f"{prefix}_uploaded_{datetime.now():%Y%m%d_%H%M%S}_{stem}.sqlite3"
    cursor = dropbox.files.UploadSessionCursor(session_id=state["sid"], offset=state["size"])
    commit = dropbox.files.CommitInfo(path=f"{folder}/{filename}", mode=WriteMode.add, autorename=True)
    try:
        metadata = _get_dbx().files_upload_session_finish(b"", cursor, commit)
    except Exception as exc:
        expected = _offset_error(exc)
        if expected is not None:
            raise UploadError("The upload is incomplete.", expected_offset=expected)
        raise
    clear_backup_list_cache()
    logger.info("Uploaded database file saved as %s", metadata.path_display)
    return metadata.name


def check_sqlite_file(path: str) -> None:
    """Raise ValueError unless `path` is an intact SQLite database of this site."""
    import sqlite3

    with open(path, "rb") as fh:
        if fh.read(len(SQLITE_HEADER)) != SQLITE_HEADER:
            raise ValueError("The backup is not a SQLite database.")
    connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        if connection.execute("PRAGMA quick_check").fetchone()[0] != "ok":
            raise ValueError("The backup file is damaged.")
        tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    finally:
        connection.close()
    if not {"django_migrations", "base_user"} <= tables:
        raise ValueError("The backup is not a database of this site.")
