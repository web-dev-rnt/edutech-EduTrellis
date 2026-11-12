"""Regression tests for the security hardening: auth, OTP, exams, roles, uploads and output escaping."""
from datetime import timedelta

from django.contrib.messages import constants, get_messages
from django.core import mail
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.utils import timezone

from adminpanel.models import AdminAuditLog, SMTPConfiguration
from base.models import OTPVerification, User
from base.validators import validate_pdf_content
from testseries.models import Question, StudentAnswer, Test, TestAttempt, TestSeries

STRONG = "Str0ng!Passw0rd#2026"


class SecurityTestCase(TestCase):
    def setUp(self):
        cache.clear()
        self.student = User.objects.create_user(email="student@example.com", password=STRONG)


class LoginSecurityTests(SecurityTestCase):
    def test_same_message_for_unknown_email_and_wrong_password(self):
        unknown = self.client.post("/login/", {"email": "nobody@example.com", "password": "x"}, secure=True)
        wrong = self.client.post("/login/", {"email": "student@example.com", "password": "x"}, secure=True)
        texts = [str(m) for r in (unknown, wrong) for m in get_messages(r.wsgi_request)]
        self.assertTrue(all("Incorrect email or password" in t for t in texts), texts)

    def test_login_is_rate_limited_per_account(self):
        for _ in range(10):
            self.client.post("/login/", {"email": "student@example.com", "password": "wrong"}, secure=True)
        response = self.client.post("/login/", {"email": "student@example.com", "password": STRONG}, secure=True)
        self.assertEqual(response.status_code, 429)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_failed_logins_are_audited(self):
        self.client.post("/login/", {"email": "student@example.com", "password": "wrong"}, secure=True)
        self.assertTrue(AdminAuditLog.objects.filter(action="login_failed", user_email="student@example.com").exists())

    def test_user_supplied_name_is_escaped_in_flash_messages(self):
        self.student.first_name = "<script>alert(1)</script>"
        self.student.save()
        response = self.client.post("/login/", {"email": "student@example.com", "password": STRONG}, secure=True, follow=True)
        self.assertNotContains(response, "<script>alert(1)</script>")
        self.assertContains(response, "&lt;script&gt;alert(1)&lt;/script&gt;")


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class PasswordResetSecurityTests(SecurityTestCase):
    def setUp(self):
        super().setUp()
        SMTPConfiguration.objects.create(
            email_backend="django.core.mail.backends.locmem.EmailBackend",
            email_host_user="noreply@example.com", email_host_password="x",
            default_from_email="noreply@example.com", is_active=True, test_status="success",
        )

    def _request_code(self, email="student@example.com"):
        return self.client.post("/forgot-password/", {"email": email}, secure=True).json()

    def _code(self):
        return OTPVerification.objects.get(user=self.student, verification_type="password_reset", is_used=False).otp_code

    def test_full_reset_flow_with_the_parameter_names_the_page_sends(self):
        self.assertTrue(self._request_code()["success"])
        self.assertEqual(len(mail.outbox), 1)
        verify = self.client.post("/verify-reset-otp/", {"userid": "", "otpcode": self._code()}, secure=True).json()
        self.assertTrue(verify["success"], verify)
        done = self.client.post("/reset-password/", {"new_password": "N3w!Secure#Pass", "confirm_password": "N3w!Secure#Pass"}, secure=True).json()
        self.assertTrue(done["success"], done)
        self.student.refresh_from_db()
        self.assertTrue(self.student.check_password("N3w!Secure#Pass"))

    def test_unknown_email_gets_the_same_answer_and_no_email(self):
        known = self._request_code()
        self.client = Client()
        unknown = self._request_code("ghost@example.com")
        self.assertEqual(known["message"], unknown["message"])
        self.assertEqual(len(mail.outbox), 1)

    def test_code_is_burned_after_five_wrong_guesses(self):
        self._request_code()
        code = self._code()
        for guess in ("000000", "111111", "222222", "333333", "444444"):
            self.client.post("/verify-reset-otp/", {"otp_code": guess}, secure=True)
        result = self.client.post("/verify-reset-otp/", {"otp_code": code}, secure=True).json()
        self.assertFalse(result["success"])

    def test_cannot_verify_a_code_for_an_account_this_session_did_not_request(self):
        # Attacker never called forgot-password in their session, so a posted user id is ignored.
        result = self.client.post("/verify-reset-otp/", {"user_id": self.student.pk, "otp_code": "123456"}, secure=True).json()
        self.assertFalse(result["success"])

    def test_weak_new_password_is_rejected(self):
        self._request_code()
        self.client.post("/verify-reset-otp/", {"otp_code": self._code()}, secure=True)
        result = self.client.post("/reset-password/", {"new_password": "12345678", "confirm_password": "12345678"}, secure=True).json()
        self.assertFalse(result["success"])


class ExamIntegrityTests(SecurityTestCase):
    def setUp(self):
        super().setUp()
        self.series = TestSeries.objects.create(
            title="Integrity Series", description="d", estimated_duration="1 hour", is_free=True, has_negative_marking=False,
        )
        self.test = Test.objects.create(test_series=self.series, title="Mock 1", duration_minutes=30, shuffle_questions=False, max_attempts=3)
        self.questions = [
            Question.objects.create(
                test=self.test, question_text=f"Q{i}", question_type="mcq_single", options={"a": "A", "b": "B"},
                correct_answer={"answer": "a"}, marks=4, order=i,
            )
            for i in range(3)
        ]
        self.client.force_login(self.student)
        self.client.get(f"/exam/{self.test.pk}/start/", secure=True)
        self.attempt = TestAttempt.objects.get(user=self.student, test=self.test)

    def _all_correct(self):
        return {f"question_{q.pk}": "a" for q in self.questions}

    def test_double_submit_grades_once(self):
        url = f"/exam/session/{self.attempt.pk}/submit/"
        self.client.post(url, self._all_correct(), secure=True)
        self.client.post(url, {f"question_{q.pk}": "b" for q in self.questions}, secure=True)
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.status, "submitted")
        self.assertEqual(float(self.attempt.marks_obtained), 12.0)
        self.assertEqual(StudentAnswer.objects.filter(attempt=self.attempt).count(), 3)

    def test_answers_after_the_deadline_are_ignored(self):
        TestAttempt.objects.filter(pk=self.attempt.pk).update(started_at=timezone.now() - timedelta(minutes=40))
        self.client.post(f"/exam/session/{self.attempt.pk}/submit/", self._all_correct(), secure=True)
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.status, "submitted")
        self.assertEqual(float(self.attempt.marks_obtained), 0.0)

    def test_tampered_option_counts_as_unanswered(self):
        data = self._all_correct()
        data[f"question_{self.questions[0].pk}"] = "<script>"
        self.client.post(f"/exam/session/{self.attempt.pk}/submit/", data, secure=True)
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.attempted_questions, 2)

    def test_other_users_cannot_submit_or_view_an_attempt(self):
        intruder = User.objects.create_user(email="intruder@example.com", password=STRONG)
        other = Client()
        other.force_login(intruder)
        self.assertEqual(other.post(f"/exam/session/{self.attempt.pk}/submit/", self._all_correct(), secure=True).status_code, 404)
        self.assertEqual(other.get(f"/exam/session/{self.attempt.pk}/review/", secure=True).status_code, 404)

    def test_test_page_never_contains_correct_answers(self):
        Question.objects.filter(pk=self.questions[0].pk).update(explanation="SECRET-EXPLANATION")
        page = self.client.get(f"/exam/session/{self.attempt.pk}/", secure=True)
        self.assertEqual(page.status_code, 200)
        self.assertNotContains(page, "SECRET-EXPLANATION")
        self.assertNotContains(page, "correct_answer")

    def test_review_is_locked_until_submission(self):
        response = self.client.get(f"/exam/session/{self.attempt.pk}/review/", secure=True)
        self.assertEqual(response.status_code, 302)


class RolePermissionTests(SecurityTestCase):
    def setUp(self):
        super().setUp()
        self.staff = User.objects.create_user(email="staff@example.com", password=STRONG, is_staff=True)
        self.root = User.objects.create_superuser("root@example.com", STRONG)
        self.client.force_login(self.staff)

    def test_staff_cannot_take_over_a_superuser(self):
        self.client.post(f"/user/{self.root.pk}/edit/", {"email": "staff-owned@example.com", "password": "hijack"}, secure=True)
        self.root.refresh_from_db()
        self.assertEqual(self.root.email, "root@example.com")
        self.assertTrue(self.root.check_password(STRONG))

    def test_staff_cannot_create_a_superuser(self):
        self.client.post("/users/add/", {
            "email": "evil@example.com", "first_name": "E", "password": STRONG, "confirm_password": STRONG,
            "is_superuser": "on", "is_staff": "on", "is_active": "on",
        }, secure=True)
        created = User.objects.filter(email="evil@example.com").first()
        if created:
            self.assertFalse(created.is_superuser or created.is_staff)

    def test_staff_changes_are_audited(self):
        self.client.post(f"/user/{self.student.pk}/edit/", {"email": "student@example.com", "first_name": "Renamed"}, secure=True)
        self.assertTrue(AdminAuditLog.objects.filter(user=self.staff, action="update").exists())

    def test_audit_log_page_is_superuser_only(self):
        self.assertEqual(self.client.get("/audit-log/", secure=True).status_code, 302)
        self.client.force_login(self.root)
        self.assertEqual(self.client.get("/audit-log/", secure=True).status_code, 200)


class UploadAndMediaTests(SecurityTestCase):
    def test_renamed_file_is_not_accepted_as_pdf(self):
        with self.assertRaises(ValidationError):
            validate_pdf_content(SimpleUploadedFile("fake.pdf", b"<html><script>x</script></html>"))
        validate_pdf_content(SimpleUploadedFile("real.pdf", b"%PDF-1.7\n..."))

    def test_paid_pdfs_cannot_be_fetched_by_url(self):
        self.assertEqual(self.client.get("/media/elibrary/pdfs/anything.pdf", secure=True).status_code, 404)

    def test_contact_form_is_rate_limited(self):
        data = {"name": "A", "email": "a@example.com", "message": "hi"}
        for _ in range(6):
            self.client.post("/contact/submit/", data, secure=True)
        from adminpanel.models import ContactSubmission
        self.assertEqual(ContactSubmission.objects.count(), 5)

    def test_security_headers(self):
        response = self.client.get("/", secure=True)
        self.assertEqual(response["X-Frame-Options"], "DENY")
        self.assertIn("Permissions-Policy", response)
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")
