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

DB_PATH = str(Path(settings.BASE_DIR) / "db.sqlite3")
# The listing is three Dropbox round trips (~2.5s); cache it and clear it on every change.
BACKUP_LIST_CACHE_KEY = "dropbox-backup-list-v1"
BACKUP_LIST_TIMEOUT = 60 * 10


def clear_backup_list_cache():
    cache.delete(BACKUP_LIST_CACHE_KEY)


def _credentials():
    """Use the active admin-saved configuration, falling back to settings."""
    from .models import DropboxConfiguration

    config = DropboxConfiguration.objects.filter(is_active=True).first()
    if config:
        return config.app_key, config.app_secret, config.refresh_token, config.backup_folder
    return (
        settings.DROPBOX_APP_KEY,
        settings.DROPBOX_APP_SECRET,
        settings.DROPBOX_REFRESH_TOKEN,
        default_backup_folder(),
    )


def _get_dbx():
    """Return an authenticated Dropbox client, auto-refreshing the token."""
    try:
        import dropbox  # type: ignore
        app_key, app_secret, refresh_token, _ = _credentials()
        dbx = dropbox.Dropbox(
            oauth2_refresh_token=refresh_token,
            app_key=app_key,
            app_secret=app_secret,
        )
        dbx.users_get_current_account()  # validates credentials
        return dbx
    except ImportError:
        raise RuntimeError("dropbox SDK not installed. Run: pip install dropbox")
    except Exception as exc:
        raise RuntimeError(f"Cannot authenticate with Dropbox: {exc}")


def _ensure_folder(dbx) -> None:
    """Create the backup folder on Dropbox if it does not already exist."""
    try:
        import dropbox  # type: ignore
        _, _, _, backup_folder = _credentials()
        dbx.files_get_metadata(backup_folder)
    except Exception:
        try:
            import dropbox  # type: ignore
            dbx.files_create_folder_v2(backup_folder)
            logger.info("Created Dropbox folder: %s", backup_folder)
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
    def create_backup() -> dict:
        """
        Upload db.sqlite3 to Dropbox with a timestamped filename.
        Returns a dict with keys: success, filename, message.
        """
        if not os.path.exists(DB_PATH):
            return {"success": False, "message": f"Database file not found: {DB_PATH}"}

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{brand()['slug'].replace('-', '_')}_backup_{timestamp}.sqlite3"
        _, _, _, backup_folder = _credentials()
        dropbox_path = f"{backup_folder}/{filename}"

        try:
            dbx = _get_dbx()
            _ensure_folder(dbx)

            with open(DB_PATH, "rb") as fh:
                data = fh.read()

            import dropbox  # type: ignore
            dbx.files_upload(
                data,
                dropbox_path,
                mode=dropbox.files.WriteMode("overwrite"),
            )
            file_size = _human_size(len(data))
            logger.info("Backup uploaded: %s (%s)", dropbox_path, file_size)
            clear_backup_list_cache()
            return {
                "success": True,
                "filename": filename,
                "message": f"Backup '{filename}' ({file_size}) uploaded successfully.",
            }
        except Exception as exc:
            logger.error("Backup failed: %s", exc)
            return {"success": False, "message": str(exc)}

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
            _, _, _, backup_folder = _credentials()
            result = dbx.files_list_folder(backup_folder)
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
    def restore_backup(filename: str) -> dict:
        """
        Download the specified backup from Dropbox and replace db.sqlite3.
        Returns dict with keys: success, message.
        """
        _, _, _, backup_folder = _credentials()
        dropbox_path = f"{backup_folder}/{filename}"
        try:
            dbx = _get_dbx()
            _, response = dbx.files_download(dropbox_path)
            data = response.content

            # Write atomically: write to temp, check it is a healthy database of this site, then rename
            tmp_path = DB_PATH + ".tmp_restore"
            with open(tmp_path, "wb") as fh:
                fh.write(data)
            try:
                check_sqlite_file(tmp_path)
            except Exception:
                os.remove(tmp_path)
                raise
            os.replace(tmp_path, DB_PATH)

            logger.info("Database restored from: %s", dropbox_path)
            return {"success": True, "message": f"Database restored from '{filename}' successfully."}
        except Exception as exc:
            logger.error("Restore failed: %s", exc)
            return {"success": False, "message": str(exc)}

    # ------------------------------------------------------------------ #
    #  DOWNLOAD URL (temporary link)                                      #
    # ------------------------------------------------------------------ #
    @staticmethod
    def get_download_url(filename: str) -> dict:
        """
        Return a temporary direct download link (4 hour expiry).
        Returns dict with keys: success, url / message.
        """
        _, _, _, backup_folder = _credentials()
        dropbox_path = f"{backup_folder}/{filename}"
        try:
            dbx = _get_dbx()
            link = dbx.files_get_temporary_link(dropbox_path)
            return {"success": True, "url": link.link}
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
        _, _, _, backup_folder = _credentials()
        dropbox_path = f"{backup_folder}/{filename}"
        try:
            dbx = _get_dbx()
            dbx.files_delete_v2(dropbox_path)
            logger.info("Deleted Dropbox backup: %s", dropbox_path)
            clear_backup_list_cache()
            return {"success": True, "message": f"Backup '{filename}' deleted successfully."}
        except Exception as exc:
            logger.error("Delete backup failed: %s", exc)
            return {"success": False, "message": str(exc)}


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
    _, _, _, backup_folder = _credentials()
    stem = re.sub(r"[^A-Za-z0-9_-]+", "_", os.path.splitext(state["name"])[0]).strip("_")[:40] or "database"
    prefix = brand()["slug"].replace("-", "_")
    filename = f"{prefix}_uploaded_{datetime.now():%Y%m%d_%H%M%S}_{stem}.sqlite3"
    cursor = dropbox.files.UploadSessionCursor(session_id=state["sid"], offset=state["size"])
    commit = dropbox.files.CommitInfo(path=f"{backup_folder}/{filename}", mode=WriteMode.add, autorename=True)
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
