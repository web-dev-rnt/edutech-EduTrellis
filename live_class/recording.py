"""Save class recordings to Dropbox while the class is still running.

The teacher's browser records the class and sends it here in pieces of a few MB. Each piece is appended to a Dropbox
upload session straight away, so nothing large sits on the server, no request runs long, and if the browser closes
mid-class everything sent so far is still saved (stale recordings are finished the next time the room is opened).
Without Dropbox credentials the pieces are appended to a file on the server disk instead.
"""
import logging
import os
from datetime import timedelta

from django.conf import settings
from django.core.files.storage import default_storage
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.text import slugify

logger = logging.getLogger(__name__)

MAX_CHUNK_BYTES = 8 * 1024 * 1024        # keep under DATA_UPLOAD_MAX_MEMORY_SIZE (10 MB)
STALE_AFTER = timedelta(minutes=3)       # no piece for this long while "recording" = the browser went away
LOW_SPACE_BYTES = 500 * 1024 * 1024      # warn the teacher below this much free Dropbox space

EXTENSIONS = {'video/webm': 'webm', 'video/mp4': 'mp4'}


class OffsetMismatch(Exception):
    def __init__(self, expected):
        super().__init__(f'expected offset {expected}')
        self.expected = expected


def dropbox_storage():
    from video_courses.dropbox_storage import DropboxStorage
    return DropboxStorage()


def dropbox_ready():
    return dropbox_storage()._is_configured()


def free_space_bytes():
    """Free Dropbox space in bytes, or None when unknown."""
    try:
        usage = dropbox_storage().client.users_get_space_usage()
        allocation = usage.allocation
        total = allocation.get_individual().allocated if allocation.is_individual() else allocation.get_team().allocated
        return max(0, total - usage.used)
    except Exception as exc:  # space is only advisory
        logger.warning('Could not read Dropbox space: %s', exc)
        return None


def new_file_name(session, mime_type):
    base = mime_type.split(';')[0].strip()
    ext = EXTENSIONS.get(base, 'webm')
    stamp = timezone.localtime().strftime('%Y-%m-%d_%H%M')
    course = slugify(session.course.name)[:60] or 'course'
    title = slugify(session.class_name)[:60] or 'class'
    return f'live_recordings/{course}/{stamp}_{title}_{get_random_string(6)}.{ext}'


def start(session, user, mime_type):
    from .models import LiveClassRecording
    base = (mime_type or 'video/webm').split(';')[0].strip().lower()
    if base not in EXTENSIONS:
        base = 'video/webm'
    return LiveClassRecording.objects.create(
        session=session,
        started_by=user if user and user.is_authenticated else None,
        title=f"{session.class_name} – {timezone.localtime().strftime('%d %b %Y, %I:%M %p')}",
        file_name=new_file_name(session, base),
        storage='dropbox' if dropbox_ready() else 'local',
        mime_type=base,
    )


def _local_path(recording):
    return os.path.join(settings.MEDIA_ROOT, recording.file_name)


def append(recording, data, offset):
    """Append one piece that starts at `offset` bytes. Retries of a piece already saved are accepted."""
    if recording.status != 'recording':
        raise ValueError('This recording is already finished.')
    if offset + len(data) == recording.size_bytes and offset < recording.size_bytes:
        return recording.size_bytes  # the browser retried a piece we already have
    if offset != recording.size_bytes:
        raise OffsetMismatch(recording.size_bytes)
    if not data:
        return recording.size_bytes

    if recording.storage == 'dropbox':
        import dropbox
        client = dropbox_storage().client
        if not recording.upload_session_id:
            recording.upload_session_id = client.files_upload_session_start(data).session_id
        else:
            cursor = dropbox.files.UploadSessionCursor(session_id=recording.upload_session_id, offset=offset)
            client.files_upload_session_append_v2(data, cursor)
    else:
        path = _local_path(recording)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'ab') as fh:
            fh.write(data)
    recording.size_bytes = offset + len(data)
    recording.save(update_fields=['upload_session_id', 'size_bytes', 'updated_at'])
    return recording.size_bytes


def finish(recording, duration_seconds=None):
    """Close the upload and make the recording watchable. Empty recordings are marked failed."""
    if recording.status != 'recording':
        return recording
    if duration_seconds:
        recording.duration_seconds = max(0, int(duration_seconds))
    elif recording.duration_seconds == 0 and recording.created_at:
        recording.duration_seconds = int((timezone.now() - recording.created_at).total_seconds())
    if recording.size_bytes == 0:
        recording.status = 'failed'
    elif recording.storage == 'dropbox':
        import dropbox
        storage = dropbox_storage()
        try:
            cursor = dropbox.files.UploadSessionCursor(session_id=recording.upload_session_id, offset=recording.size_bytes)
            commit = dropbox.files.CommitInfo(path=storage._clean_path(recording.file_name), mode=dropbox.files.WriteMode.add, autorename=False)
            storage.client.files_upload_session_finish(b'', cursor, commit)
            recording.status = 'ready'
        except Exception:
            logger.exception('Could not finish Dropbox upload for recording %s', recording.pk)
            recording.status = 'failed'
    else:
        recording.status = 'ready'
    recording.finished_at = timezone.now()
    recording.save(update_fields=['status', 'duration_seconds', 'finished_at', 'updated_at'])
    return recording


def finish_stale(session):
    """Finish recordings whose browser stopped sending pieces (closed tab, lost connection)."""
    cutoff = timezone.now() - STALE_AFTER
    for recording in session.recordings.filter(status='recording', updated_at__lt=cutoff):
        finish(recording)


def playback_url(recording):
    """A URL the browser can stream the recording from."""
    if recording.storage == 'dropbox':
        return dropbox_storage().temporary_url(recording.file_name)
    return default_storage.url(recording.file_name)


def delete(recording):
    try:
        if recording.storage == 'dropbox' and recording.status == 'ready':
            dropbox_storage().delete(recording.file_name)
        elif recording.storage == 'local' and os.path.exists(_local_path(recording)):
            os.remove(_local_path(recording))
    finally:
        recording.delete()
