"""Who may join a live class, and when the room is open."""
from datetime import timedelta

from django.utils import timezone

# Students can enter this long before the start, and up to this long after the scheduled end.
OPEN_BEFORE = timedelta(minutes=15)
OPEN_AFTER = timedelta(minutes=30)


def is_teacher(user):
    return bool(user and user.is_authenticated and user.is_staff)


def has_course_access(user, course):
    """Free course, or an active purchase of it (teachers always)."""
    if is_teacher(user):
        return True
    if not (user and user.is_authenticated):
        return False
    if course.is_free:
        return True
    from base.models import UserCourseAccess
    access = UserCourseAccess.objects.filter(
        user=user, course_id=course.pk, course_type='live_class', is_active=True,
    ).first()
    return bool(access and access.has_access)


def can_join(user, session):
    """Logged in, and the session or course is free or bought."""
    if not (user and user.is_authenticated):
        return False
    return session.is_free or has_course_access(user, session.course)


def room_state(session, now=None):
    """'upcoming' (too early), 'open' (students may join) or 'ended'."""
    now = now or timezone.now()
    if now < session.scheduled_datetime - OPEN_BEFORE:
        return 'upcoming'
    if now > session.ends_at + OPEN_AFTER:
        return 'ended'
    return 'open'


def opens_at(session):
    return session.scheduled_datetime - OPEN_BEFORE
