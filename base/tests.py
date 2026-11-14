import re
from io import BytesIO
from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from base.models import User
from elibrary.models import ELibraryCourse, ELibraryDownload, ELibraryPDF
from video_courses.dropbox_storage import DropboxStorage
from video_courses.models import Category


class ManagementAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="student@example.com",
            password="strong-test-password",
        )

    def test_anonymous_users_cannot_open_management_pages(self):
        for url in (
            "/video-courses/create/",
            "/video-courses/manage/",
            "/liveclass/",
            "/liveclass/create/",
            "/banner-edit/",
        ):
            with self.subTest(url=url):
                response = self.client.get(url, secure=True)
                self.assertEqual(response.status_code, 302)

    def test_regular_users_cannot_open_management_pages(self):
        self.client.force_login(self.user)
        for url in (
            "/video-courses/create/",
            "/liveclass/",
            "/banner-edit/",
            "/smtp/",
        ):
            with self.subTest(url=url):
                response = self.client.get(url, secure=True)
                self.assertEqual(response.status_code, 302)


class ELibraryAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="reader@example.com",
            password="strong-test-password",
        )
        category = Category.objects.create(name="Books")
        self.course = ELibraryCourse.objects.create(
            title="Paid Library",
            description="Course description",
            short_description="Short description",
            category=category,
            instructor="Instructor",
            price=100,
            created_by=self.user,
        )
        self.pdf = ELibraryPDF(
            course=self.course,
            title="Chapter One",
            file="elibrary/pdfs/chapter-one.pdf",
            uploaded_by=self.user,
        )
        ELibraryPDF.objects.bulk_create([self.pdf])
        self.client.force_login(self.user)

    def test_paid_pdf_rejects_user_without_access(self):
        response = self.client.get(
            reverse("view_pdf", args=[self.pdf.pk]),
            secure=True,
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(ELibraryDownload.objects.count(), 0)

    def test_preview_pdf_streams_without_local_path(self):
        self.pdf.is_preview = True
        ELibraryPDF.objects.filter(pk=self.pdf.pk).update(is_preview=True)

        with patch.object(
            DropboxStorage,
            "open",
            return_value=BytesIO(b"%PDF-1.4 test"),
        ):
            response = self.client.get(
                reverse("view_pdf", args=[self.pdf.pk]),
                secure=True,
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ELibraryDownload.objects.count(), 1)
        self.pdf.refresh_from_db()
        self.assertEqual(self.pdf.download_count, 1)


class PerformanceAndPWATests(TestCase):
    def setUp(self):
        cache.clear()

    def test_dropbox_url_generation_does_not_make_network_request(self):
        storage = DropboxStorage()
        with self.settings(
            DROPBOX_REFRESH_TOKEN="refresh-token",
            DROPBOX_APP_KEY="app-key",
            DROPBOX_APP_SECRET="app-secret",
        ):
            with patch.object(
                DropboxStorage,
                "temporary_url",
                side_effect=AssertionError("network resolution must not happen during render"),
            ):
                url = storage.url("video_courses/example/thumb.jpg")
        self.assertTrue(url.startswith("/dropbox-file/"))

    def test_missing_dropbox_credentials_use_local_image_fallback(self):
        storage = DropboxStorage()
        with self.settings(
            DROPBOX_REFRESH_TOKEN="",
            DROPBOX_APP_KEY="",
            DROPBOX_APP_SECRET="",
            STORAGES={
                "default": {
                    "BACKEND": "django.core.files.storage.FileSystemStorage"
                },
                "staticfiles": {
                    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
                },
            },
        ):
            url = storage.url("video_courses/example/thumb.jpg")
        self.assertTrue(url.endswith("/static/img/default-thumb.jpg"))

    def test_homepage_has_no_blocking_checkout_or_external_font_stylesheet(self):
        with self.settings(
            STORAGES={
                "default": {
                    "BACKEND": "django.core.files.storage.FileSystemStorage"
                },
                "staticfiles": {
                    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
                },
            },
        ):
            response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "checkout.razorpay.com")
        self.assertNotContains(response, "fonts.googleapis.com")

    def test_service_worker_only_caches_public_static_files(self):
        response = self.client.get(reverse("service-worker"), secure=True)
        self.assertEqual(response.status_code, 200)
        source = response.content.decode("utf-8")
        self.assertIn("url.pathname.startsWith('/static/')", source)
        self.assertNotIn("cache.put(request, responseClone)", source)
        self.assertIn("/static/img/icon-192.png", source)

    def test_manifest_references_existing_icon_names(self):
        response = self.client.get(reverse("manifest1"), secure=True)
        self.assertEqual(response.status_code, 200)
        icon_urls = {icon["src"] for icon in response.json()["icons"]}
        # Hashed static names (icon-192.<hash>.png) bust browser caches when the icons change.
        self.assertTrue(any(re.search(r"/static/img/icon-192(\.[0-9a-f]{12})?\.png$", url) for url in icon_urls))
        self.assertTrue(any(re.search(r"/static/img/icon-512(\.[0-9a-f]{12})?\.png$", url) for url in icon_urls))


class DailyQuizTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_logged_out_visitors_see_a_login_prompt_but_never_the_questions(self):
        response = self.client.get('/')
        self.assertContains(response, 'id="daily-quiz"')
        self.assertContains(response, 'data-locked="1"')
        self.assertNotContains(response, 'id="dq-initial"')  # no questions/answers in the page source
        self.assertEqual(self.client.get(reverse('daily_quiz_api', args=['gk'])).status_code, 401)
        submit = self.client.post(reverse('daily_quiz_submit', args=['gk']), '{"picks": []}', content_type='application/json')
        self.assertEqual(submit.status_code, 401)

    def test_every_category_has_ten_fair_questions_and_changes_daily(self):
        import datetime
        from base.daily_quiz import CATEGORY_KEYS, build_quiz
        self.client.force_login(User.objects.create_user(email='quiz@example.com', password='Str0ng!Passw0rd#2026'))
        self.assertContains(self.client.get('/'), 'id="dq-initial"')
        for category in CATEGORY_KEYS:
            data = self.client.get(reverse('daily_quiz_api', args=[category])).json()
            self.assertEqual(len(data['questions']), 10, category)
            for q in data['questions']:
                self.assertEqual(len(set(q['options'])), 4, (category, q['html']))
                self.assertIn(q['answer'], range(4))
        today = datetime.date(2026, 11, 12)
        self.assertEqual(build_quiz(today, 'mixed'), build_quiz(today, 'mixed'))
        self.assertNotEqual(build_quiz(today, 'mixed')['questions'], build_quiz(today + datetime.timedelta(days=1), 'mixed')['questions'])
        self.assertEqual(self.client.get('/daily-quiz/astrology/').status_code, 404)

    def test_scores_are_marked_on_the_server_saved_once_per_day_and_shown_in_results_and_profile(self):
        import datetime
        import json
        from django.utils import timezone
        from base.daily_quiz import build_quiz
        from base.models import DailyQuizAttempt
        user = User.objects.create_user(email='streak@example.com', password='Str0ng!Passw0rd#2026')
        self.client.force_login(user)
        questions = build_quiz(timezone.localdate(), 'gk')['questions']
        right = [q['answer'] for q in questions]
        wrong_three = [(a + 1) % 4 if i < 3 else a for i, a in enumerate(right)]
        url = reverse('daily_quiz_submit', args=['gk'])

        first = self.client.post(url, json.dumps({'picks': wrong_three}), content_type='application/json').json()
        self.assertEqual((first['score'], first['total'], first['streak']), (7, 10, 1))
        retake = self.client.post(url, json.dumps({'picks': right}), content_type='application/json').json()
        self.assertEqual((retake['score'], retake['first_score'], retake['best'], retake['attempts']), (10, 7, 10, 2))
        self.assertEqual(DailyQuizAttempt.objects.filter(user=user).count(), 1)
        self.assertEqual(self.client.post(url, json.dumps({'picks': [9] * 10}), content_type='application/json').status_code, 400)

        # Yesterday and the day before as well: a 3-day streak.
        for days_ago in (1, 2):
            DailyQuizAttempt.objects.create(user=user, quiz_date=timezone.localdate() - datetime.timedelta(days=days_ago),
                                            category='maths', score=5, best_score=5, total=10)
        results = self.client.get(reverse('my_test_results'))
        quiz = results.context['quiz']
        self.assertEqual((quiz['taken'], quiz['answered'], quiz['correct'], quiz['current_streak'], quiz['best_streak']), (3, 30, 17, 3, 3))
        self.assertContains(results, 'Quizzes taken')
        profile = self.client.get(reverse('profile_edit'))
        self.assertEqual(profile.context['quiz']['taken'], 3)
        self.assertContains(profile, 'Daily Quiz')


class SearchAndAIVisibilityTests(TestCase):
    """The site presents itself as EduTrellis's official test series website to Google and AI assistants."""

    def setUp(self):
        cache.clear()

    def test_home_names_the_site_and_its_parent_company(self):
        import json

        page = self.client.get('/').content.decode()
        self.assertIn('<title>EduTrellis Test Series — Online Mock Tests', page)
        self.assertIn('Official EduTrellis test series website', page)
        graphs = [json.loads(m) for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)]
        nodes = [node for g in graphs for node in g.get('@graph', [g])]
        website = next(n for n in nodes if n.get('@type') == 'WebSite')
        org = next(n for n in nodes if n.get('@type') == 'EducationalOrganization')
        faq = next(n for n in nodes if n.get('@type') == 'FAQPage')
        self.assertEqual(website['name'], 'EduTrellis Test Series')
        self.assertEqual(org['parentOrganization'], {'@id': 'https://www.edutrellis.in/#organization'})
        self.assertTrue(any(n.get('@id') == 'https://www.edutrellis.in/#organization' for n in nodes))
        self.assertIn('official online test series website of EduTrellis', faq['mainEntity'][0]['acceptedAnswer']['text'])
        self.assertIn('Frequently asked questions', page)  # the FAQ is visible, not only in the markup

    def test_llms_txt_and_favicon(self):
        llms = self.client.get('/llms.txt')
        self.assertEqual(llms.status_code, 200)
        self.assertTrue(llms['Content-Type'].startswith('text/markdown'))
        text = llms.content.decode()
        self.assertTrue(text.startswith('# EduTrellis Test Series'))
        for snippet in ('official online test series website of EduTrellis', 'https://www.edutrellis.in/ai/',
                        '## Frequently asked questions', 'support@edutrellis.in'):
            self.assertIn(snippet, text)
        icon = self.client.get('/favicon.ico')
        self.assertEqual((icon.status_code, icon['Content-Type']), (200, 'image/x-icon'))
        self.assertIn('/llms.txt', self.client.get('/robots.txt').content.decode())
