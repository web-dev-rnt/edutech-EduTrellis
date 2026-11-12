from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import RazorpayConfiguration


@override_settings(STORAGES={
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
})
class RazorpayConfigurationTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_user(
            email='admin@example.com',
            password='test-password',
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(self.admin)

    def test_admin_can_save_and_view_masked_configuration(self):
        response = self.client.post(reverse('razorpay_configuration'), {
            'name': 'Test account',
            'key_id': 'rzp_test_example',
            'key_secret': 'super-secret-value',
            'is_active': 'on',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rzp_test_example')
        self.assertContains(response, '********alue')
        self.assertNotContains(response, 'super-secret-value')
        self.assertTrue(
            RazorpayConfiguration.objects.get(name='Test account').is_active
        )

    def test_only_latest_selected_configuration_remains_active(self):
        first = RazorpayConfiguration.objects.create(
            name='First', key_id='rzp_test_first', key_secret='first-secret'
        )
        self.client.post(reverse('razorpay_configuration'), {
            'name': 'Second',
            'key_id': 'rzp_test_second',
            'key_secret': 'second-secret',
            'is_active': 'on',
        })

        first.refresh_from_db()
        self.assertFalse(first.is_active)
        self.assertTrue(RazorpayConfiguration.objects.get(name='Second').is_active)

    def test_blank_secret_on_edit_keeps_saved_secret(self):
        config = RazorpayConfiguration.objects.create(
            name='Existing', key_id='rzp_test_existing', key_secret='saved-secret'
        )
        self.client.post(reverse('razorpay_edit', args=[config.pk]), {
            'config_id': config.pk,
            'name': 'Updated',
            'key_id': 'rzp_test_updated',
            'key_secret': '',
            'is_active': 'on',
        })

        config.refresh_from_db()
        self.assertEqual(config.name, 'Updated')
        self.assertEqual(config.key_secret, 'saved-secret')

    @patch('base.views.razorpay.Client')
    def test_payment_client_uses_active_saved_configuration(self, client_class):
        RazorpayConfiguration.objects.create(
            name='Live', key_id='rzp_live_saved', key_secret='live-secret'
        )

        from base.views import get_razorpay_client

        _, key_id = get_razorpay_client()
        self.assertEqual(key_id, 'rzp_live_saved')
        client_class.assert_called_once_with(auth=('rzp_live_saved', 'live-secret'))


@override_settings(STORAGES={
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
})
class SignupAnalyticsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(
            email='analytics-admin@example.com',
            password='test-password',
            is_staff=True,
            is_superuser=True,
        )
        self.matching_user = User.objects.create_user(
            email='amit.sharma@example.com',
            password='test-password',
            first_name='Amit',
            last_name='Sharma',
            contact_number='8296893895',
        )
        User.objects.create_user(
            email='different@example.com',
            password='test-password',
            first_name='Different',
            last_name='User',
        )
        self.client.force_login(self.admin)

    def test_multi_word_search_matches_first_and_last_name(self):
        response = self.client.get(
            reverse('signupdashboard'),
            {'search': '  Amit Sharma  '},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['users']), [self.matching_user])
        self.assertEqual(response.context['search_query'], 'Amit Sharma')

    def test_filter_controls_use_page_specific_button_styles(self):
        response = self.client.get(reverse('signupdashboard'))

        self.assertContains(response, 'signup-filter-search')
        self.assertContains(response, 'signup-filter-clear')
        self.assertContains(response, '<option value="regular"', html=False)
        self.assertNotContains(response, '<option value="superuser"', html=False)


@override_settings(STORAGES={
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
})
class BrandNameTests(TestCase):
    """The brand name comes from the database, so renaming it in the admin panel renames the site."""

    def setUp(self):
        from django.core.cache import cache
        cache.clear()
        self.admin = get_user_model().objects.create_user(
            email='brand-admin@example.com', password='test-password', is_staff=True, is_superuser=True,
        )

    def rename(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('theme_settings_edit'), {
            'site_name': 'BrightPath', 'site_full_name': 'BrightPath Learning', 'primary_color': '#2459e0',
        })
        self.assertEqual(response.status_code, 302)

    def test_rename_updates_pages_admin_and_backups(self):
        from .backup_utils import _credentials
        from .branding import brand

        self.rename()
        self.assertEqual(brand(), {'name': 'BrightPath', 'full_name': 'BrightPath Learning', 'slug': 'brightpath'})

        self.client.logout()
        home = self.client.get('/').content.decode()
        self.assertIn('<title>BrightPath Learning |', home)
        self.assertIn('content="BrightPath"', home)  # app name meta
        login = self.client.get('/login/').content.decode()
        self.assertIn('Login | BrightPath', login)
        self.assertNotIn('Infinite360', login)
        manifest = self.client.get('/manifest.json').json()
        self.assertEqual(manifest['short_name'], 'BrightPath')

        self.client.force_login(self.admin)
        self.assertContains(self.client.get('/admin/'), 'BrightPath Admin Panel')
        self.assertEqual(_credentials()[3], '/brightpath-backup')

    def test_homepage_sections_use_brand_name(self):
        """About Us and the footer are drawn by inclusion tags, which have their own context."""
        from .models import AboutUsSection, WhyChooseUsItem

        AboutUsSection.objects.update_or_create(pk=1, defaults={'company_name': '', 'is_active': True})
        WhyChooseUsItem.objects.create(title='Fast results', description='Fast results', is_active=True)
        self.rename()
        self.client.logout()
        home = self.client.get('/').content.decode()
        self.assertIn('Why Choose BrightPath?', home)
        self.assertIn('Get the BrightPath app', home)

    def test_blank_name_is_rejected(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('theme_settings_edit'), {
            'site_name': '  ', 'site_full_name': '', 'primary_color': '#2459e0',
        })
        self.assertEqual(response.status_code, 200)
        from .branding import brand_name
        self.assertEqual(brand_name(), 'Infinite360')


@override_settings(SITE_OWNER_EMAILS=['owner@example.com'])
class DatabaseUploadTests(TestCase):
    """Manual database upload: only real SQLite databases of this site are accepted or restored."""

    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp()
        self.admin = get_user_model().objects.create_user(
            email='owner@example.com', password='test-password', is_staff=True, is_superuser=True,
        )

    def make_db(self, tables):
        import os
        import sqlite3
        path = os.path.join(self.tmp, f"{'_'.join(tables) or 'empty'}.sqlite3")
        connection = sqlite3.connect(path)
        for table in tables:
            connection.execute(f'CREATE TABLE {table} (id INTEGER)')
        connection.commit()
        connection.close()
        return path

    def test_check_sqlite_file(self):
        import os
        from .backup_utils import check_sqlite_file

        check_sqlite_file(self.make_db(['django_migrations', 'base_user']))
        with self.assertRaisesMessage(ValueError, 'not a database of this site'):
            check_sqlite_file(self.make_db(['other']))
        junk = os.path.join(self.tmp, 'junk.sqlite3')
        with open(junk, 'wb') as fh:
            fh.write(b'hello world, definitely not sqlite')
        with self.assertRaisesMessage(ValueError, 'not a SQLite database'):
            check_sqlite_file(junk)

    def test_start_rejects_non_database_files_before_contacting_dropbox(self):
        self.client.force_login(self.admin)
        with patch('adminpanel.backup_utils._get_dbx', side_effect=AssertionError('no Dropbox call expected')):
            response = self.client.post('/backup/upload/start/', b'plain text', content_type='application/octet-stream',
                                        HTTP_X_FILE_NAME='notes.sqlite3', HTTP_X_FILE_SIZE='10')
            self.assertEqual(response.status_code, 400)
            self.assertIn('not a SQLite database', response.json()['error'])
            response = self.client.post('/backup/upload/start/', b'SQLite format 3\x00', content_type='application/octet-stream',
                                        HTTP_X_FILE_NAME='photo.png', HTTP_X_FILE_SIZE='16')
            self.assertEqual(response.status_code, 400)

    def test_backups_are_owner_only(self):
        """Other super admins (like admin@gmail.com) get no backup link, page or action."""
        other = get_user_model().objects.create_user(
            email='admin@example.com', password='x', is_staff=True, is_superuser=True,
        )
        self.client.force_login(other)
        dashboard = self.client.get(reverse('admindashboard'))
        self.assertEqual(dashboard.status_code, 200)
        self.assertNotContains(dashboard, 'Backup Management')
        self.assertRedirects(self.client.get('/backup/'), reverse('admindashboard'), fetch_redirect_response=False)
        with patch('adminpanel.backup_utils._get_dbx', side_effect=AssertionError('no Dropbox call expected')):
            for url in ('/backup/now/', '/backup/restore/', '/backup/delete/', '/backup/configuration/',
                        '/backup/upload/start/', '/backup/upload/chunk/', '/backup/upload/finish/'):
                response = self.client.post(url, b'SQLite format 3\x00', content_type='application/octet-stream',
                                            HTTP_X_FILE_NAME='db.sqlite3', HTTP_X_FILE_SIZE='16')
                self.assertEqual(response.status_code, 403, url)
            self.assertRedirects(self.client.get('/backup/download/x.sqlite3/'), reverse('admindashboard'),
                                 fetch_redirect_response=False)

        self.client.force_login(self.admin)
        self.assertContains(self.client.get(reverse('admindashboard')), 'Backup Management')

    def test_upload_token_is_tied_to_the_user(self):
        from .backup_utils import UploadError, upload_append
        from django.core import signing

        token = signing.dumps({'sid': 's', 'size': 10, 'name': 'db.sqlite3', 'uid': self.admin.pk + 1}, salt='backup-upload')
        with self.assertRaisesMessage(UploadError, 'another account'):
            upload_append(token, self.admin.pk, b'x', 0)


class DropboxMediaStorageTests(TestCase):
    """Uploads go to Dropbox; pages use the saved permanent link and never call Dropbox while rendering."""

    def setUp(self):
        import tempfile
        from django.core.cache import cache
        cache.clear()
        self.media = tempfile.mkdtemp()
        self.override = override_settings(
            MEDIA_ROOT=self.media, DROPBOX_APP_KEY='k', DROPBOX_APP_SECRET='s', DROPBOX_REFRESH_TOKEN='t',
        )
        self.override.enable()
        self.addCleanup(self.override.disable)

    def storage(self):
        from video_courses.dropbox_storage import DropboxMediaStorage
        return DropboxMediaStorage()

    def test_direct_link(self):
        from video_courses.dropbox_storage import direct_link
        self.assertEqual(
            direct_link('https://www.dropbox.com/scl/fi/abc/logo.png?rlkey=xyz&dl=0'),
            'https://www.dropbox.com/scl/fi/abc/logo.png?rlkey=xyz&raw=1',
        )

    def test_url_uses_saved_link_without_network(self):
        from base.models import DropboxFileLink
        from video_courses.dropbox_storage import DropboxStorage

        storage = self.storage()
        DropboxFileLink.objects.create(path='/media/banners/a.webp', name='banners/a.webp', url='https://dl.example/a.webp?raw=1')
        with patch.object(DropboxStorage, 'client', new_callable=lambda: property(lambda self: (_ for _ in ()).throw(AssertionError('network')))):
            self.assertEqual(storage.url('banners/a.webp'), 'https://dl.example/a.webp?raw=1')
            self.assertTrue(storage.url('banners/b.webp').startswith('/dropbox-media/'))

    def test_without_keys_files_stay_local(self):
        from django.core.files.base import ContentFile

        with override_settings(DROPBOX_APP_KEY='', DROPBOX_APP_SECRET='', DROPBOX_REFRESH_TOKEN=''):
            storage = self.storage()
            name = storage.save('logos/x.png', ContentFile(b'png'))
            self.assertTrue(storage.local.exists(name))
            self.assertEqual(storage.url(name), f'/media/{name}')

    def test_redirect_view_copies_local_file_and_saves_link(self):
        from django.core.files.base import ContentFile
        from base.models import DropboxFileLink
        from video_courses.dropbox_storage import DropboxMediaStorage, DropboxStorage

        storage = self.storage()
        name = storage.local.save('banners/old.webp', ContentFile(b'old image'))
        uploaded = []
        link_result = type('Link', (), {'url': 'https://www.dropbox.com/scl/fi/1/old.webp?rlkey=r&dl=0'})()
        fake_client = type('Client', (), {'sharing_create_shared_link_with_settings': lambda self, path: link_result})()
        with patch.object(DropboxMediaStorage, '_in_dropbox', return_value=False), \
                patch.object(DropboxStorage, '_save', side_effect=lambda _self, n, c: uploaded.append((n, c.read())) or n), \
                patch.object(DropboxStorage, 'client', new_callable=lambda: property(lambda self: fake_client)):
            response = self.client.get(storage.url(name))
        self.assertEqual(uploaded, [(name, b'old image')])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'https://www.dropbox.com/scl/fi/1/old.webp?rlkey=r&raw=1')
        self.assertIn('max-age=86400', response['Cache-Control'])
        self.assertEqual(DropboxFileLink.objects.get(name=name).url, response['Location'])
        self.assertEqual(storage.url(name), response['Location'])  # pages now link straight to Dropbox

    def test_tampered_token_is_rejected(self):
        self.assertEqual(self.client.get('/dropbox-media/abc:def/').status_code, 404)


@override_settings(SITE_OWNER_EMAILS=['owner@example.com'])
class RestoreSessionTests(TestCase):
    """A restore replaces the sessions table; the admin who clicked Restore must stay logged in."""

    def test_admin_stays_logged_in_after_restore(self):
        from django.contrib.sessions.models import Session

        from .backup_utils import DropboxBackupManager

        owner = get_user_model().objects.create_user(
            email='owner@example.com', password='x', is_staff=True, is_superuser=True,
        )
        self.client.force_login(owner)

        def fake_restore(filename):
            Session.objects.all().delete()  # what loading another database does to this request's session
            return {'success': True, 'message': 'Restored.'}

        with patch.object(DropboxBackupManager, 'restore_backup', side_effect=fake_restore):
            response = self.client.post('/backup/restore/', {'filename': 'x.sqlite3'})
        self.assertRedirects(response, '/backup/', fetch_redirect_response=False)
        with patch.object(DropboxBackupManager, 'list_backups', return_value=[]):
            page = self.client.get('/backup/')
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, 'upload-card')


@override_settings(SITE_OWNER_EMAILS=['owner@example.com'])
class SiteOwnerOnlyTests(TestCase):
    """Audit Log and Tutor AI are for the site owner only, not for other super admins."""

    def test_other_super_admin_cannot_see_audit_log_or_tutor_ai(self):
        other = get_user_model().objects.create_user(email='admin@example.com', password='x', is_staff=True, is_superuser=True)
        owner = get_user_model().objects.create_user(email='owner@example.com', password='x', is_staff=True, is_superuser=True)

        self.client.force_login(other)
        dashboard = self.client.get(reverse('admindashboard'))
        self.assertNotContains(dashboard, 'Audit Log')
        self.assertNotContains(dashboard, 'Tutor AI')
        for name in ('audit_log', 'tutor_admin'):
            self.assertRedirects(self.client.get(reverse(name)), reverse('admindashboard'), fetch_redirect_response=False)
        self.assertEqual(self.client.post(reverse('tutor_admin'), {'action': 'save'}).status_code, 403)
        self.assertEqual(self.client.get('/admin/adminpanel/adminauditlog/').status_code, 403)

        self.client.force_login(owner)
        dashboard = self.client.get(reverse('admindashboard'))
        self.assertContains(dashboard, 'Audit Log')
        self.assertContains(dashboard, 'Tutor AI')
        self.assertEqual(self.client.get(reverse('audit_log')).status_code, 200)
        self.assertEqual(self.client.get(reverse('tutor_admin')).status_code, 200)
