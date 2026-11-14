"""
adminpanel/backup_views.py
Superuser-only views for Dropbox database backup/restore management.
"""
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
import logging
from urllib.parse import unquote

from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from . import backup_jobs, backup_utils
from .backup_utils import DropboxBackupManager, clear_backup_list_cache
from .branding import default_backup_folder
from .forms import DropboxConfigurationForm
from .models import DropboxConfiguration
from .permissions import can_manage_backups

logger = logging.getLogger(__name__)


def _stay_logged_in(request, email=None):
    """The restored database has its own accounts and sessions; log the same person in again."""
    from django.contrib.auth import get_user_model, login

    email = email or request.user.email
    # This request's session row was replaced with the backup's sessions; store the session under a new key
    # (login() alone keeps the old key when the same person logs in again, and saving it would fail).
    request.session.cycle_key()
    user = get_user_model().objects.filter(email__iexact=email, is_active=True).first()
    if user:
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    return user


def _superuser_required(view_fn):
    """Decorator: allow only the site owner accounts (settings.SITE_OWNER_EMAILS)."""
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if not can_manage_backups(request.user):
            if request.path.startswith(("/backup/upload/", "/backup/api/")):
                return JsonResponse({"error": "Access denied."}, status=403)
            if request.method != "GET":
                return HttpResponseForbidden("Access denied.")
            messages.error(request, "Access denied. Backup Management is restricted to the site owner.")
            return redirect('admindashboard')
        return view_fn(request, *args, **kwargs)
    wrapper.__name__ = view_fn.__name__
    return wrapper


@_superuser_required
def backup_dashboard(request):
    """The backup page. It renders without calling Dropbox; status and backups load from the JSON API."""
    saved_config = DropboxConfiguration.objects.filter(is_active=True).first()
    active_config = saved_config or DropboxConfiguration(
        name="settings.py fallback",
        app_key=settings.DROPBOX_APP_KEY,
        app_secret=settings.DROPBOX_APP_SECRET,
        refresh_token=settings.DROPBOX_REFRESH_TOKEN,
        backup_folder=default_backup_folder(),
    )
    form = DropboxConfigurationForm(instance=saved_config)
    running = backup_jobs.active_job()
    context = {
        "backup_folder": backup_utils.backup_folder(),
        "running_job_token": backup_jobs.token(running) if running else "",
        "active_database": backup_utils.active_database_label(),
        "can_restore": backup_utils.is_sqlite(),
        "active_config": active_config,
        "has_saved_config": bool(saved_config),
        "config_form": form,
        "configuration_source": "Saved on this page" if saved_config else "Server settings (environment)",
    }
    return render(request, "adminpanel/backup_dashboard.html", context)


@_superuser_required
@require_POST
def backup_configuration_save(request):
    """Save and activate the Dropbox configuration used for all backups."""
    active_config = DropboxConfiguration.objects.filter(is_active=True).first()
    form = DropboxConfigurationForm(request.POST, instance=active_config)
    if form.is_valid():
        config = form.save(commit=False)
        try:
            config.backup_folder = backup_utils.normalize_folder(config.backup_folder)
            account = backup_utils.check_credentials(config.app_key, config.app_secret, config.refresh_token)
        except (ValueError, RuntimeError) as exc:
            messages.error(request, f"Not saved: {exc}")
            return redirect("backup_dashboard")
        DropboxConfiguration.objects.exclude(pk=config.pk).update(is_active=False)
        config.is_active = True
        config.save()
        clear_backup_list_cache()
        messages.success(request, f"Dropbox settings saved and activated (connected to {account}'s Dropbox).")
    else:
        messages.error(request, "Please correct the Dropbox settings below.")
    return redirect("backup_dashboard")


@_superuser_required
@require_POST
def backup_configuration_reset(request):
    """Stop using the credentials saved on this page; use the server settings (environment) again."""
    DropboxConfiguration.objects.filter(is_active=True).update(is_active=False)
    clear_backup_list_cache()
    messages.success(request, "Now using the Dropbox credentials from the server settings.")
    return redirect("backup_dashboard")


@_superuser_required
@require_POST
def backup_now(request):
    """Trigger an immediate database backup to Dropbox."""
    result = DropboxBackupManager.create_backup()
    if result["success"]:
        messages.success(request, f"\u2705 {result['message']}")
    else:
        messages.error(request, f"\u274c Backup failed: {result['message']}")
    return redirect("backup_dashboard")


@_superuser_required
@require_POST
def backup_restore(request):
    """Restore the database from a selected Dropbox backup."""
    filename = request.POST.get("filename", "").strip()
    if not filename:
        messages.error(request, "No backup file specified.")
        return redirect("backup_dashboard")

    # Basic sanitisation: no path traversal
    if "/" in filename or ".." in filename:
        messages.error(request, "Invalid filename.")
        return redirect("backup_dashboard")

    result = DropboxBackupManager.restore_backup(filename)
    if result["success"]:
        _stay_logged_in(request)
        messages.success(request, f"\u2705 {result['message']} The site is now using the restored database.")
    else:
        messages.error(request, f"\u274c Restore failed: {result['message']}")
    return redirect("backup_dashboard")


@_superuser_required
def backup_download(request, filename):
    """Redirect the user to a temporary Dropbox download link."""
    if "/" in filename or ".." in filename:
        messages.error(request, "Invalid filename.")
        return redirect("backup_dashboard")

    result = DropboxBackupManager.get_download_url(filename)
    if result["success"]:
        return HttpResponseRedirect(result["url"])
    else:
        messages.error(request, f"\u274c Download failed: {result['message']}")
        return redirect("backup_dashboard")


@_superuser_required
@require_POST
def backup_delete(request):
    """Delete a backup file from Dropbox."""
    filename = request.POST.get("filename", "").strip()
    if not filename:
        messages.error(request, "No backup file specified.")
        return redirect("backup_dashboard")

    if "/" in filename or ".." in filename:
        messages.error(request, "Invalid filename.")
        return redirect("backup_dashboard")

    result = DropboxBackupManager.delete_backup(filename)
    if result["success"]:
        messages.success(request, f"\u2705 {result['message']}")
    else:
        messages.error(request, f"\u274c Delete failed: {result['message']}")
    return redirect("backup_dashboard")


# ---------------------------------------------------------------------------
#  Manual upload of a database file (browser sends it in pieces)
# ---------------------------------------------------------------------------
def _upload_error(exc, status=400):
    payload = {"error": str(exc)}
    if getattr(exc, "expected_offset", None) is not None:
        payload["expected"] = exc.expected_offset
        status = 409
    return JsonResponse(payload, status=status)


@_superuser_required
@require_POST
def backup_upload_start(request):
    try:
        size = int(request.headers.get("X-File-Size", ""))
    except ValueError:
        return JsonResponse({"error": "Missing file size."}, status=400)
    try:
        token = backup_utils.upload_start(
            unquote(request.headers.get("X-File-Name", "")), size, request.body, request.user.pk,
        )
    except backup_utils.UploadError as exc:
        return _upload_error(exc)
    except Exception as exc:
        logger.exception("Backup upload could not start")
        return JsonResponse({"error": f"Dropbox error: {exc}"}, status=502)
    return JsonResponse({"token": token, "chunk_bytes": backup_utils.UPLOAD_CHUNK_BYTES})


@_superuser_required
@require_POST
def backup_upload_chunk(request):
    try:
        offset = int(request.headers.get("X-Offset", ""))
    except ValueError:
        return JsonResponse({"error": "Missing X-Offset header."}, status=400)
    try:
        size = backup_utils.upload_append(request.headers.get("X-Upload-Token", ""), request.user.pk, request.body, offset)
    except backup_utils.UploadError as exc:
        return _upload_error(exc)
    except Exception as exc:
        logger.exception("Backup upload piece failed")
        return JsonResponse({"error": f"Dropbox error: {exc}"}, status=502)
    return JsonResponse({"size": size})


@_superuser_required
@require_POST
def backup_upload_finish(request):
    try:
        filename = backup_utils.upload_finish(request.headers.get("X-Upload-Token", ""), request.user.pk)
    except backup_utils.UploadError as exc:
        return _upload_error(exc)
    except Exception as exc:
        logger.exception("Backup upload could not finish")
        return JsonResponse({"error": f"Dropbox error: {exc}"}, status=502)
    if request.headers.get("X-Restore") == "1":
        result = DropboxBackupManager.restore_backup(filename)
        if not result["success"]:
            messages.error(request, f"\u274c Uploaded '{filename}', but restoring it failed: {result['message']}")
            return JsonResponse({"filename": filename, "restored": False})
        _stay_logged_in(request)
        messages.success(request, f"\u2705 Uploaded '{filename}' and restored it. The site is now using this database.")
        return JsonResponse({"filename": filename, "restored": True})
    messages.success(request, f"\u2705 Uploaded '{filename}'. Use Restore to switch the site to it.")
    return JsonResponse({"filename": filename})


# ---------------------------------------------------------------------------
#  JSON API used by the backup page
# ---------------------------------------------------------------------------
def _valid_backup_name(filename):
    return bool(filename) and "/" not in filename and "\\" not in filename and ".." not in filename


def _job_response(job, status=200):
    return JsonResponse({"job": backup_jobs.public(job), "token": backup_jobs.token(job)}, status=status)


@_superuser_required
def backup_api_status(request):
    """Connection, account, storage space, backup folder and its contents."""
    if request.GET.get("refresh"):
        clear_backup_list_cache()
    status = backup_utils.connection_status()
    running = backup_jobs.active_job()
    status["running_job"] = backup_jobs.token(running) if running else None
    return JsonResponse(status)


@_superuser_required
def backup_api_list(request):
    if request.GET.get("refresh"):
        clear_backup_list_cache()
    try:
        backups = DropboxBackupManager.list_backups()
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=502)
    return JsonResponse({
        "folder": backup_utils.backup_folder(),
        "backups": [dict(b, modified=b["modified"].isoformat()) for b in backups],
    })


@_superuser_required
def backup_api_folders(request):
    try:
        return JsonResponse({"folders": backup_utils.backup_folders()})
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=502)


@_superuser_required
@require_POST
def backup_api_retention(request):
    try:
        keep = backup_utils.set_keep_last(request.POST.get("keep_last", "0"))
    except (TypeError, ValueError) as exc:
        return JsonResponse({"error": str(exc) or "Invalid number."}, status=400)
    return JsonResponse({"keep_last": keep})


@_superuser_required
@require_POST
def backup_api_folder(request):
    """Switch to (or create) a backup folder."""
    try:
        folder = backup_utils.set_backup_folder(request.POST.get("folder", ""))
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    except Exception as exc:
        logger.exception("Could not switch the backup folder")
        return JsonResponse({"error": f"Dropbox error: {exc}"}, status=502)
    return JsonResponse({"folder": folder})


def _backup_work(progress):
    result = DropboxBackupManager.create_backup(progress)
    if not result["success"]:
        raise RuntimeError(result["message"])
    removed = backup_utils.apply_retention(progress)
    if removed:
        result["message"] += f" {len(removed)} old backup(s) removed to keep the latest {backup_utils._keep_last()}."
    return result


def _restore_work(progress, filename, safety_backup):
    result = DropboxBackupManager.restore_backup(filename, progress, safety_backup=safety_backup)
    if not result["success"]:
        raise RuntimeError(result["message"])
    return result


@_superuser_required
@require_POST
def backup_api_start(request):
    """Start a backup or restore in the background. Returns the job and a token to poll it with."""
    action = request.POST.get("action")
    try:
        if action == "backup":
            if not backup_utils.is_sqlite():
                return JsonResponse({"error": f"The site uses {backup_utils.active_database_label()}; only SQLite can be backed up here."}, status=400)
            job = backup_jobs.start("backup", request.user, _backup_work)
        elif action == "restore":
            filename = request.POST.get("filename", "").strip()
            if not _valid_backup_name(filename):
                return JsonResponse({"error": "Invalid backup file name."}, status=400)
            if not backup_utils.is_sqlite():
                return JsonResponse({"error": f"The site uses {backup_utils.active_database_label()}; a SQLite backup cannot be restored into it."}, status=400)
            job = backup_jobs.start("restore", request.user, _restore_work, filename=filename,
                                    safety_backup=request.POST.get("safety_backup") == "1")
        else:
            return JsonResponse({"error": "Unknown action."}, status=400)
    except backup_jobs.JobBusy as busy:
        return JsonResponse({"error": str(busy), "token": backup_jobs.token(busy.job)}, status=409)
    return _job_response(job, status=202)


def backup_api_job(request, token):
    """Progress of a backup/restore job. Authorised by the signed token, not the session: a restore
    replaces the sessions table, so the admin who started it is logged in again here when it finishes."""
    job = backup_jobs.from_token(token)
    if job is None:
        return JsonResponse({"error": "This job has expired."}, status=404)
    if job["kind"] == "restore" and job["status"] == "done":
        user = request.user
        if not (user.is_authenticated and user.email.lower() == (job.get("email") or "").lower()):
            _stay_logged_in(request, email=job.get("email"))
    elif not (request.user.is_authenticated and can_manage_backups(request.user)):
        return JsonResponse({"error": "Access denied."}, status=403)
    return JsonResponse({"job": backup_jobs.public(job)})


@_superuser_required
def backup_api_download(request, filename):
    """A temporary Dropbox link the page downloads from (with progress), plus the file size."""
    if not _valid_backup_name(filename):
        return JsonResponse({"error": "Invalid file name."}, status=400)
    result = DropboxBackupManager.get_download_url(filename)
    if not result["success"]:
        return JsonResponse({"error": result["message"]}, status=502)
    return JsonResponse({"url": result["url"], "size": result["size"], "filename": filename})


@_superuser_required
@require_POST
def backup_api_delete(request):
    filename = request.POST.get("filename", "").strip()
    if not _valid_backup_name(filename):
        return JsonResponse({"error": "Invalid file name."}, status=400)
    result = DropboxBackupManager.delete_backup(filename)
    if not result["success"]:
        return JsonResponse({"error": result["message"]}, status=502)
    return JsonResponse({"deleted": filename})
