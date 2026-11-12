"""Create the free "CBSE Class 10 Science – Demo Live Class" course with a few classes.

    python manage.py create_demo_live_class               # create it (does nothing if it already has classes)
    python manage.py create_demo_live_class --reschedule  # move the classes to fresh times from now

The first class starts a few minutes from now, so the room is open straight away to try it out.
"""
from datetime import datetime, time, timedelta
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from live_class.models import LiveClassCourse, LiveClassSession
from video_courses.models import Category

NAME = 'CBSE Class 10 Science – Free Demo Live Class'
BANNER = Path(settings.BASE_DIR) / 'base' / 'static' / 'img' / 'live' / 'cbse-demo-live.webp'
ABOUT = (
    "Try a live class before you enrol. An experienced teacher covers key CBSE Class 10 Science chapters "
    "in a live, interactive session: ask doubts in real time, solve board-style questions together and "
    "watch the recording later. Free for every registered student. Join from your phone, tablet or laptop, "
    "with no app needed."
)
# (title, subject, minutes)
CLASSES = [
    ('Chemical Reactions & Equations – Live Demo', 'Chemistry', 60),
    ('Light – Reflection & Refraction', 'Physics', 60),
    ('Electricity – Ohm\'s Law & Circuits', 'Physics', 60),
]


class Command(BaseCommand):
    help = 'Create the free CBSE Class 10 Science demo live class (first class starts in a few minutes).'

    def add_arguments(self, parser):
        parser.add_argument('--reschedule', action='store_true',
                            help='Replace the classes (those without recordings) with fresh times starting now.')

    def handle(self, *args, **options):
        today = timezone.localdate()
        course, created = LiveClassCourse.objects.get_or_create(name=NAME, defaults={
            'language': 'Hindi & English',
            'original_price': 0, 'current_price': 0, 'is_free': True,
            'start_date': today, 'end_date': today + timedelta(days=30),
            'about': ABOUT,
            'category': Category.objects.filter(name__iexact='CBSE').first(),
            'is_active': True,
        })
        if not course.banner_image_desktop and BANNER.exists():
            with BANNER.open('rb') as fh:
                course.banner_image_desktop.save('cbse-demo-live.webp', File(fh), save=False)
            with BANNER.open('rb') as fh:
                course.banner_image_mobile.save('cbse-demo-live.webp', File(fh), save=False)
            course.save()

        if options['reschedule']:
            course.sessions.filter(recordings__isnull=True).delete()
        if course.sessions.exists():
            self.stdout.write(f'"{course.name}" already has classes (use --reschedule for fresh times).')
            return self._report(course, created)

        now = timezone.localtime()
        first = now.replace(second=0, microsecond=0) + timedelta(minutes=5)
        evening = lambda days: timezone.make_aware(datetime.combine(today + timedelta(days=days), time(17, 0)))
        starts = [first, evening(1), evening(2)]
        if course.end_date < starts[-1].date():
            course.end_date = starts[-1].date() + timedelta(days=30)
            course.save(update_fields=['end_date'])
        for (title, subject, minutes), start in zip(CLASSES, starts):
            LiveClassSession.objects.create(
                course=course, class_name=title, subject=subject, scheduled_datetime=start,
                duration_minutes=minutes, is_free=True, enable_auto_recording=True, max_participants=100,
            )
        self._report(course, created)

    def _report(self, course, created):
        self.stdout.write(self.style.SUCCESS(f'{"Created" if created else "Updated"} "{course.name}" (id {course.pk}).'))
        for s in course.sessions.order_by('scheduled_datetime'):
            self.stdout.write(f'  #{s.pk} {timezone.localtime(s.scheduled_datetime):%a %d %b, %I:%M %p}  {s.class_name}'
                              f'  ->  /liveclass/session/{s.pk}/join/')
        self.stdout.write(f'  Course page: /live-class/{course.pk}/')
