# live_class/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.views import redirect_to_login
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_datetime
from django.contrib.auth import authenticate, login
from django.conf import settings
import json
import logging
from urllib.parse import quote

from . import access, recording
from .models import LiveClassSession, LiveClassCourse, LiveClassRecording
from .forms import LiveClassCourseForm
from .utils.jitsi_free import generate_room_name

logger = logging.getLogger(__name__)


# Course Management Views
@staff_member_required(login_url="login")
def live_class_course_manage(request):
    """Display and filter live class courses"""
    courses = LiveClassCourse.objects.select_related('category').all()
    
    # Search filter
    q = request.GET.get('q')
    if q:
        courses = courses.filter(name__icontains=q)
    
    # Course type filter (free/paid)
    course_type = request.GET.get('type')
    if course_type == 'free':
        courses = courses.filter(is_free=True)
    elif course_type == 'paid':
        courses = courses.filter(is_free=False)
    
    return render(request, "live_classes/live_class_course_manage.html", {
        "courses": courses,
        "selected_type": course_type,
    })


@staff_member_required(login_url="login")
def live_class_course_create(request):
    """Create a new live class course"""
    if request.method == "POST":
        form = LiveClassCourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            messages.success(request, "Live class course created successfully.")
            return redirect('liveclass')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LiveClassCourseForm()
    return render(request, "live_classes/live_class_course_create.html", {
        "form": form,
    })


@staff_member_required(login_url="login")
def live_class_course_edit(request, pk):
    """Edit an existing live class course"""
    course = get_object_or_404(LiveClassCourse, pk=pk)
    if request.method == "POST":
        form = LiveClassCourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Live class course updated successfully.")
            return redirect('liveclass')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LiveClassCourseForm(instance=course)
    return render(request, "live_classes/live_class_course_edit.html", {
        "form": form,
        "course": course,
    })


@require_POST
@staff_member_required(login_url="login")
def live_class_course_delete(request, pk):
    """Delete a live class course"""
    course = get_object_or_404(LiveClassCourse, pk=pk)
    course.delete()
    messages.success(request, "Live class course deleted.")
    return redirect('liveclass')


@require_POST
@staff_member_required(login_url="login")
def live_class_course_toggle_status(request, pk):
    """Toggle active status of a course"""
    course = get_object_or_404(LiveClassCourse, pk=pk)
    course.is_active = not course.is_active
    course.save()
    return JsonResponse({
        'success': True, 
        'status': course.is_active, 
        'message': 'Course status updated.'
    })


@staff_member_required(login_url="login")
def live_class_course_classes(request, pk):
    """Get all classes for a specific course"""
    course = get_object_or_404(LiveClassCourse, pk=pk)
    classes = [{
        "id": s.id,
        "class_name": s.class_name,
        "scheduled_datetime": s.scheduled_datetime.strftime("%b %d, %Y, %I:%M %p"),
        "duration_minutes": s.duration_minutes,
        "max_participants": s.max_participants,
        "is_free": s.is_free,
        "enable_auto_recording": s.enable_auto_recording,
        "subject": s.subject or "-",
    } for s in course.sessions.all()]
    return JsonResponse({
        "course_name": course.name,
        "is_course_free": course.is_free,
        "classes": classes
    })


# Session Management Views
@staff_member_required(login_url="login")
@require_POST
def add_scheduled_class(request, course_id):
    """Add a new scheduled class to a course"""
    if request.method != "POST":
        return HttpResponseBadRequest()
    
    course = get_object_or_404(LiveClassCourse, pk=course_id)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "success": False, 
            "error": "Invalid JSON data."
        }, status=400)
    
    # Validate datetime
    scheduled_dt = parse_datetime(data.get("scheduled_datetime"))
    if not scheduled_dt:
        return JsonResponse({
            "success": False, 
            "error": "Invalid date/time format."
        }, status=400)
    
    # Check if datetime is within course duration
    if scheduled_dt.date() < course.start_date or scheduled_dt.date() > course.end_date:
        return JsonResponse({
            "success": False, 
            "error": "Class must be scheduled within course start and end dates."
        }, status=400)

    try:
        # Create session with transaction safety
        with transaction.atomic():
            session = LiveClassSession.objects.create(
                course=course,
                class_name=data.get("class_name", "").strip(),
                enable_auto_recording=bool(data.get("enable_auto_recording", False)),
                scheduled_datetime=scheduled_dt,
                duration_minutes=int(data.get("duration_minutes", 60)),
                max_participants=100,
                is_free=bool(data.get("is_free", False)),
                subject=data.get("subject", "").strip(),
            )
        return JsonResponse({
            "success": True, 
            "id": session.id, 
            "message": "Class scheduled successfully."
        })
    except Exception as e:
        return JsonResponse({
            "success": False, 
            "error": f"Failed to create session: {str(e)}"
        }, status=500)


@staff_member_required(login_url="login")
@require_POST
def live_class_schedule_delete(request, session_id):
    """Delete a scheduled class"""
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST method allowed")
    
    session = get_object_or_404(LiveClassSession, id=session_id)
    
    try:
        session.delete()
        return JsonResponse({
            "success": True, 
            "message": "Class schedule deleted successfully."
        })
    except Exception as e:
        return JsonResponse({
            "success": False, 
            "error": f"Failed to delete session: {str(e)}"
        }, status=500)


# Live Session View
def _jitsi_join_url(domain, room_name, display_name, subject, is_moderator):
    """meet.jit.si link that opens straight in the browser (also on phones) with the student's name filled in."""
    params = {
        'userInfo.displayName': display_name,
        'config.subject': subject,
        'config.disableDeepLinking': True,       # phones: stay in the browser instead of "get the app"
        'config.prejoinConfig.enabled': True,    # students check camera / mic before entering
        'config.startWithVideoMuted': not is_moderator,
        'config.startWithAudioMuted': not is_moderator,
        'interfaceConfig.MOBILE_APP_PROMO': False,
    }
    fragment = '&'.join(f"{key}={quote(json.dumps(value), safe='')}" for key, value in params.items())
    return f"https://{domain}/{room_name}#{fragment}"


def live_class_join(request, session_id):
    """The class room page for students and teachers (mobile friendly, site layout)."""
    session = get_object_or_404(LiveClassSession.objects.select_related('course'), id=session_id)
    user = request.user
    teacher = access.is_teacher(user)
    state = access.room_state(session)
    allowed = access.can_join(user, session)
    if teacher:
        recording.finish_stale(session)

    display_name = ''
    if user.is_authenticated:
        display_name = user.get_full_name() or user.first_name or user.email.split('@')[0]
    room_name = generate_room_name(session.pk, session.class_name)
    domain = settings.JITSI_DOMAIN
    recordings = session.recordings.filter(status='ready')
    if not teacher:
        recordings = recordings.filter(is_published=True)

    context = {
        'session': session,
        'course': session.course,
        'state': 'open' if teacher else state,
        'real_state': state,
        'opens_at': access.opens_at(session),
        'can_join': allowed and (teacher or state == 'open'),
        'has_access': allowed,
        'is_moderator': teacher,
        'jitsi_domain': domain,
        'jitsi_embed': settings.JITSI_EMBED,
        'room_name': room_name,
        'display_name': display_name,
        'user_email': user.email if user.is_authenticated else '',
        'join_url': _jitsi_join_url(domain, room_name, display_name or 'Student', session.class_name, teacher) if allowed else '',
        'recordings': recordings if allowed else [],
        'dropbox_ready': recording.dropbox_ready(),
        'login_url': f"{reverse('login')}?next={quote(request.get_full_path())}",
    }
    return render(request, 'live_classes/live_room.html', context)


# Recording: the teacher's browser streams the class into Dropbox piece by piece.
def _json_body(request):
    try:
        return json.loads(request.body or b'{}')
    except (ValueError, UnicodeDecodeError):
        return {}


@require_POST
@staff_member_required(login_url="login")
def live_recording_start(request, session_id):
    session = get_object_or_404(LiveClassSession.objects.select_related('course'), id=session_id)
    recording.finish_stale(session)
    rec = recording.start(session, request.user, _json_body(request).get('mime_type', 'video/webm'))
    warning = ''
    if rec.storage == 'dropbox':
        free = recording.free_space_bytes()
        if free is not None and free < recording.LOW_SPACE_BYTES:
            warning = f"Only {free // (1024 * 1024)} MB free in Dropbox. A 1-hour class needs about 400 MB."
    else:
        warning = 'Dropbox is not connected, so this recording is saved on the server disk.'
    return JsonResponse({
        'id': rec.pk,
        'storage': rec.storage,
        'chunk_url': reverse('live_recording_chunk', args=[rec.pk]),
        'finish_url': reverse('live_recording_finish', args=[rec.pk]),
        'max_chunk': recording.MAX_CHUNK_BYTES,
        'warning': warning,
    })


@require_POST
@staff_member_required(login_url="login")
def live_recording_chunk(request, recording_id):
    try:
        offset = int(request.headers.get('X-Offset', ''))
    except ValueError:
        return JsonResponse({'error': 'Missing X-Offset header.'}, status=400)
    data = request.body
    if len(data) > recording.MAX_CHUNK_BYTES:
        return JsonResponse({'error': 'Piece too large.'}, status=413)
    with transaction.atomic():
        rec = get_object_or_404(LiveClassRecording.objects.select_for_update(), pk=recording_id)
        try:
            size = recording.append(rec, data, offset)
        except recording.OffsetMismatch as exc:
            return JsonResponse({'error': 'offset_mismatch', 'expected': exc.expected}, status=409)
        except ValueError as exc:
            return JsonResponse({'error': str(exc)}, status=409)
        except Exception:
            logger.exception('Recording %s: could not save a piece', recording_id)
            return JsonResponse({'error': 'Could not save to Dropbox, retrying.'}, status=502)
    return JsonResponse({'size': size})


@require_POST
@staff_member_required(login_url="login")
def live_recording_finish(request, recording_id):
    with transaction.atomic():
        rec = get_object_or_404(LiveClassRecording.objects.select_for_update(), pk=recording_id)
        recording.finish(rec, _json_body(request).get('duration'))
    return JsonResponse({'status': rec.status, 'size_mb': rec.size_mb, 'duration': rec.duration_display,
                         'play_url': reverse('live_recording_play', args=[rec.pk])})


@require_POST
@staff_member_required(login_url="login")
def live_recording_delete(request, recording_id):
    rec = get_object_or_404(LiveClassRecording, pk=recording_id)
    session_id = rec.session_id
    recording.delete(rec)
    messages.success(request, 'Recording deleted.')
    return redirect('live_class_join', session_id=session_id)


def live_recording_play(request, recording_id):
    """Stream a recording to a student who has access (redirects to a short-lived Dropbox link)."""
    rec = get_object_or_404(LiveClassRecording.objects.select_related('session__course'), pk=recording_id, status='ready')
    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path(), reverse('login'))
    teacher = access.is_teacher(request.user)
    if not teacher and not (rec.is_published and access.can_join(request.user, rec.session)):
        raise Http404('Recording not available')
    url = recording.playback_url(rec)
    if not url:
        raise Http404('Recording is temporarily unavailable')
    return redirect(url)
