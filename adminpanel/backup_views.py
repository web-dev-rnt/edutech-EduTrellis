"""
adminpanel/backup_views.py
Superuser-only views for Dropbox database backup/restore management.
"""
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
import logging
from urllib.parse import unquote

from django.http import HttpResponseRedirect, JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from . import backup_utils
from .backup_utils import DropboxBackupManager, clear_backup_list_cache
from .branding import default_backup_folder
from .forms import DropboxConfigurationForm
from .models import DropboxConfiguration

logger = logging.getLogger(__name__)


def _superuser_required(view_fn):
    """Decorator: allow only superusers; redirect others with an error message."""
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "Access denied. This section is restricted to Super Admins only.")
            return redirect('admindashboard')
        return view_fn(request, *args, **kwargs)
    wrapper.__name__ = view_fn.__name__
    return wrapper


@_superuser_required
def backup_dashboard(request):
    """Display the backup management page listing all Dropbox backups."""
    backups = []
    dropbox_error = None
    try:
        backups = DropboxBackupManager.list_backups()
    except Exception as exc:
        dropbox_error = str(exc)

    saved_config = DropboxConfiguration.objects.filter(is_active=True).first()
    active_config = saved_config or DropboxConfiguration(
        name="settings.py fallback",
        app_key=settings.DROPBOX_APP_KEY,
        app_secret=settings.DROPBOX_APP_SECRET,
        refresh_token=settings.DROPBOX_REFRESH_TOKEN,
        backup_folder=default_backup_folder(),
    )
    form = DropboxConfigurationForm(instance=saved_config)
    context = {
        "backups": backups,
        "dropbox_error": dropbox_error,
        "total_backups": len(backups),
        "backup_folder": active_config.backup_folder,
        "active_config": active_config,
        "has_saved_config": bool(saved_config),
        "config_form": form,
        "configuration_source": "Saved dashboard configuration" if saved_config else "settings.py fallback",
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
        DropboxConfiguration.objects.exclude(pk=config.pk).update(is_active=False)
        config.is_active = True
        config.save()
        clear_backup_list_cache()
        messages.success(request, "Dropbox settings saved and activated.")
    else:
        messages.error(request, "Please correct the Dropbox settings below.")
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
    messages.success(request, f"\u2705 Uploaded '{filename}'. Use Restore to switch the site to it.")
    return JsonResponse({"filename": filename})
