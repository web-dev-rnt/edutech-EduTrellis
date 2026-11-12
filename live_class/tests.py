import json
import re
import shutil
import tempfile
from datetime import date, timedelta
from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from base.models import User, UserCourseAccess

from . import recording
from .models import LiveClassCourse, LiveClassRecording, LiveClassSession
from .utils.jitsi_free import generate_room_name

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
}


@override_settings(JITSI_DOMAIN='meet.jit.si', JITSI_EMBED=False, STORAGES=STORAGES)
class LiveRoomTests(TestCase):
    def setUp(self):
        self.course = LiveClassCourse.objects.create(
            name='Physics Live', language='English', original_price=100, current_price=50,
            start_date=date.today() - timedelta(days=1), end_date=date.today() + timedelta(days=30),
        )
        self.session = LiveClassSession.objects.create(
            course=self.course, class_name='Kinematics', scheduled_datetime=timezone.now() - timedelta(minutes=5),
        )
        self.url = reverse('live_class_join', args=[self.session.pk])
        self.student = User.objects.create_user(email='s@example.com', password='Str0ng!Passw0rd#2026', first_name='Asha')
        self.teacher = User.objects.create_user(email='t@example.com', password='Str0ng!Passw0rd#2026', is_staff=True)

    def enroll(self):
        UserCourseAccess.objects.create(user=self.student, course_id=self.course.pk, course_type='live_class')

    def test_room_name_is_stable_and_branded(self):
        first = generate_room_name(self.session.pk, self.session.class_name)
        self.assertEqual(first, generate_room_name(self.session.pk, self.session.class_name))
        self.assertTrue(first.startswith('Infinite360LiveClass'))

    def test_logged_out_and_not_enrolled_students_cannot_get_the_room_link(self):
        page = self.client.get(self.url, secure=True)
        self.assertContains(page, 'Log in to join this class')
        self.assertNotContains(page, 'meet.jit.si/')
        self.client.force_login(self.student)
        page = self.client.get(self.url, secure=True)
        self.assertContains(page, 'Enroll to join this class')
        self.assertNotContains(page, 'meet.jit.si/')

    def test_enrolled_student_gets_a_browser_friendly_link_on_the_free_server(self):
        self.enroll()
        self.client.force_login(self.student)
        page = self.client.get(self.url, secure=True)
        self.assertContains(page, 'Join class now')
        room = generate_room_name(self.session.pk, self.session.class_name)
        link = re.search(r'href="(https://meet\.jit\.si/[^"]+)"', page.content.decode()).group(1)
        self.assertIn(room, link)
        self.assertIn('config.disableDeepLinking=true', link)       # phones stay in the browser
        self.assertIn('userInfo.displayName=%22Asha%22', link)       # name filled in
        self.assertNotContains(page, 'external_api.js')              # not embedded: meet.jit.si ends embeds after 5 min
        self.assertNotContains(page, 'id="recorder"')                # students don't get the recorder

    def test_room_opens_15_minutes_early_and_closes_after_the_class(self):
        self.enroll()
        self.client.force_login(self.student)
        self.session.scheduled_datetime = timezone.now() + timedelta(hours=2)
        self.session.save()
        page = self.client.get(self.url, secure=True)
        self.assertContains(page, 'Class starts in')
        self.assertNotContains(page, 'Join class now')
        self.session.scheduled_datetime = timezone.now() - timedelta(hours=3)
        self.session.save()
        self.assertContains(self.client.get(self.url, secure=True), 'This class has ended')

    def test_teacher_can_start_any_time_and_gets_the_recorder(self):
        self.session.scheduled_datetime = timezone.now() + timedelta(days=3)
        self.session.save()
        self.client.force_login(self.teacher)
        page = self.client.get(self.url, secure=True)
        self.assertContains(page, 'Start class')
        self.assertContains(page, 'id="recorder"')

    def test_free_session_needs_only_a_login(self):
        self.session.is_free = True
        self.session.save()
        self.client.force_login(self.student)
        self.assertContains(self.client.get(self.url, secure=True), 'Join class now')

    @override_settings(JITSI_DOMAIN='jitsi.example.org', JITSI_EMBED=True)
    def test_self_hosted_server_is_embedded(self):
        self.enroll()
        self.client.force_login(self.student)
        page = self.client.get(self.url, secure=True)
        self.assertContains(page, 'https://jitsi.example.org/external_api.js')
        self.assertContains(page, 'id="jitsi-container"')

    def test_course_page_shows_join_now_while_the_class_is_live(self):
        page = self.client.get(reverse('live_class_detail', args=[self.course.pk]), secure=True)
        self.assertContains(page, 'Join now')


@override_settings(STORAGES=STORAGES, DROPBOX_APP_KEY='', DROPBOX_APP_SECRET='', DROPBOX_REFRESH_TOKEN='')
class RecordingTests(TestCase):
    def setUp(self):
        self.media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media, ignore_errors=True)
        course = LiveClassCourse.objects.create(
            name='Chem Live', language='Hindi', original_price=100, current_price=50,
            start_date=date.today(), end_date=date.today(),
        )
        self.session = LiveClassSession.objects.create(course=course, class_name='Moles', scheduled_datetime=timezone.now())
        self.teacher = User.objects.create_user(email='t@example.com', password='Str0ng!Passw0rd#2026', is_staff=True)
        self.student = User.objects.create_user(email='s@example.com', password='Str0ng!Passw0rd#2026')

    def post_chunk(self, url, data, offset):
        return self.client.post(url, data, content_type='application/octet-stream', HTTP_X_OFFSET=str(offset), secure=True)

    def test_pieces_are_appended_in_order_and_the_recording_becomes_watchable(self):
        with self.settings(MEDIA_ROOT=self.media):
            self.client.force_login(self.teacher)
            start = self.client.post(reverse('live_recording_start', args=[self.session.pk]),
                                     json.dumps({'mime_type': 'video/webm;codecs=vp9,opus'}), content_type='application/json', secure=True).json()
            self.assertEqual(start['storage'], 'local')
            self.assertEqual(self.post_chunk(start['chunk_url'], b'A' * 1000, 0).json()['size'], 1000)
            self.assertEqual(self.post_chunk(start['chunk_url'], b'A' * 1000, 0).json()['size'], 1000)   # retry is fine
            self.assertEqual(self.post_chunk(start['chunk_url'], b'B' * 500, 0).status_code, 409)       # out of order
            self.assertEqual(self.post_chunk(start['chunk_url'], b'B' * 500, 1000).json()['size'], 1500)
            done = self.client.post(start['finish_url'], json.dumps({'duration': 75}), content_type='application/json', secure=True).json()
            self.assertEqual((done['status'], done['duration']), ('ready', '1:15'))

            rec = LiveClassRecording.objects.get()
            with open(f"{self.media}/{rec.file_name}", 'rb') as fh:
                self.assertEqual(fh.read(), b'A' * 1000 + b'B' * 500)

            # Students: only with access to the course.
            self.client.force_login(self.student)
            self.assertEqual(self.client.get(reverse('live_recording_play', args=[rec.pk]), secure=True).status_code, 404)
            UserCourseAccess.objects.create(user=self.student, course_id=self.session.course.pk, course_type='live_class')
            self.assertEqual(self.client.get(reverse('live_recording_play', args=[rec.pk]), secure=True).status_code, 302)
            self.assertContains(self.client.get(reverse('live_class_join', args=[self.session.pk]), secure=True), 'Class recordings')
            # Students can't upload.
            self.assertNotEqual(self.post_chunk(start['chunk_url'], b'C', 1500).status_code, 200)

    def test_a_recording_left_open_by_a_closed_browser_is_finished_later(self):
        with self.settings(MEDIA_ROOT=self.media):
            rec = recording.start(self.session, self.teacher, 'video/webm')
            recording.append(rec, b'X' * 10, 0)
            LiveClassRecording.objects.filter(pk=rec.pk).update(updated_at=timezone.now() - timedelta(minutes=10))
            recording.finish_stale(self.session)
            rec.refresh_from_db()
            self.assertEqual(rec.status, 'ready')

    def test_dropbox_upload_session_is_used_when_connected(self):
        client = MagicMock()
        client.files_upload_session_start.return_value.session_id = 'sess-1'
        storage = MagicMock(client=client, _is_configured=lambda: True, _clean_path=lambda n: '/elibrary/' + n)
        with patch.object(recording, 'dropbox_storage', return_value=storage):
            rec = recording.start(self.session, self.teacher, 'video/webm')
            self.assertEqual(rec.storage, 'dropbox')
            recording.append(rec, b'1' * 10, 0)
            recording.append(rec, b'2' * 10, 10)
            recording.finish(rec, 30)
        client.files_upload_session_start.assert_called_once_with(b'1' * 10)
        cursor = client.files_upload_session_append_v2.call_args[0][1]
        self.assertEqual((cursor.session_id, cursor.offset), ('sess-1', 10))
        _, cursor, commit = client.files_upload_session_finish.call_args[0]
        self.assertEqual(cursor.offset, 20)
        self.assertTrue(commit.path.startswith('/elibrary/live_recordings/chem-live/'))
        self.assertEqual(rec.status, 'ready')


@override_settings(STORAGES=STORAGES)
class DemoLiveClassCommandTests(TestCase):
    def test_creates_a_free_cbse_demo_whose_first_class_is_open_now(self):
        from django.core.management import call_command
        from io import StringIO
        from . import access
        media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, media, ignore_errors=True)
        with self.settings(MEDIA_ROOT=media):
            call_command('create_demo_live_class', stdout=StringIO())
            call_command('create_demo_live_class', stdout=StringIO())   # running again changes nothing
        course = LiveClassCourse.objects.get(name__startswith='CBSE Class 10 Science')
        self.assertTrue(course.is_free)
        self.assertTrue(course.banner_image_desktop)
        sessions = list(course.sessions.order_by('scheduled_datetime'))
        self.assertEqual(len(sessions), 3)
        self.assertEqual(access.room_state(sessions[0]), 'open')
