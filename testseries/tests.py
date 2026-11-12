"""Content engine and 2026 test series: generators are sound, patterns add up, the builder is safe to re-run,
and the exam engine grades numerical answers and fractional marks correctly."""
import random
from decimal import Decimal

from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase

from base.models import User
from base.templatetags.question_tags import question_html
from testseries.content import load_all
from testseries.content.core import as_numeric, from_row, Q
from testseries.content.patterns import EXAMS
from testseries.models import Question, Test, TestAttempt, TestSeries


class GeneratorSoundnessTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.topics = load_all()

    def test_every_topic_yields_valid_questions(self):
        rng = random.Random(2026)
        for key, topic in self.topics.items():
            for _ in range(25 if topic.gen else 1):
                try:
                    q = topic.gen(rng) if topic.gen else from_row(rng, rng.choice(topic.rows)) if topic.rows else None
                except ValueError:
                    continue  # generators retry on these inside draw()
                if q is None or q.kind == 'numerical':
                    continue
                self.assertEqual(len(q.options), 4, key)
                self.assertEqual(len({o.strip() for o in q.options}), 4, (key, q.text, q.options))
                self.assertTrue(0 <= q.answer < 4, key)
                self.assertTrue(q.text.strip(), key)

    def test_every_pattern_topic_exists_and_totals_match_the_official_paper(self):
        for exam in EXAMS:
            for section in exam.sections:
                for key in section.topics:
                    self.assertIn(key, self.topics, f"{exam.name}: {key}")
        official = {'JEE Main': (75, 300), 'NEET UG': (180, 720), 'SSC CGL': (100, 200), 'GATE': (65, 100), 'CAT': (68, 204),
                    'IBPS PO': (100, 100), 'UPSC Civil Services': (100, 200), 'NDA': (120, 300), 'CLAT': (120, 120), 'NIMCET': (120, 1000)}
        by_name = {e.name: e for e in EXAMS}
        for name, (count, marks) in official.items():
            self.assertEqual((by_name[name].total, round(by_name[name].total_marks)), (count, marks), name)

    def test_every_bank_row_gives_four_distinct_options(self):
        rng = random.Random(7)
        for key, topic in self.topics.items():
            for row in topic.rows or []:
                q = from_row(rng, row)
                self.assertEqual(len({o.strip() for o in q.options}), 4, (key, row[0][:60]))

    def test_nov_2026_exams_match_official_totals_and_are_listed_once(self):
        from testseries.boards import STATE_BOARDS
        from testseries.exam_tools import EXAM_GROUPS
        by_name = {e.name: e for e in EXAMS}
        official = {
            'UPPSC PCS': (150, 200), 'BPSC CCE': (150, 150), 'MPPSC State Service': (100, 200), 'RPSC RAS': (150, 200),
            'TNPSC Group 1': (200, 300), 'GPAT': (125, 500), 'KEAM': (150, 600), 'COMEDK UGET': (180, 180), 'KIITEE': (120, 480),
            'IISER IAT': (60, 240), 'UP Police Constable': (150, 300), 'UP Police SI': (160, 400), 'NCHM JEE': (200, 800),
            'Sainik School Class 9 (AISSEE)': (150, 400), 'REET': (150, 150), 'IDBI Junior Assistant Manager': (200, 200),
            'MAH MBA CET': (200, 200), 'INI-CET': (200, 200), 'AIBE': (100, 100), 'IRDAI Assistant Manager': (160, 160),
            'RPF SI': (120, 120), 'NIPER JEE': (200, 200), 'SNAP': (60, 60),
        }
        for name, (count, marks) in official.items():
            self.assertEqual((by_name[name].total, round(by_name[name].total_marks)), (count, marks), name)
        listed = [name for _, _, _, names in EXAM_GROUPS for name in names]
        self.assertEqual(sorted(listed), sorted(by_name), "every exam must sit in exactly one Explore Exams tab")
        self.assertTrue({'ga', 'mn', 'ml', 'mz', 'nl', 'tr'} <= {b.code for b in STATE_BOARDS})

    def test_numeric_conversion_keeps_only_plain_numbers(self):
        self.assertEqual(as_numeric(Q('Speed ___', ['20 m/s', 'a', 'b', 'c'])).value, '20')
        self.assertEqual(as_numeric(Q('Cost ___', ['₹1,331', 'a', 'b', 'c'])).value, '1331')
        self.assertIsNone(as_numeric(Q('Ratio ___', ['3 : 1', 'a', 'b', 'c'])))
        self.assertIsNone(as_numeric(Q('Div ___', ['Quotient 3, remainder 1', 'a', 'b', 'c'])))


class QuestionRenderingTests(TestCase):
    def test_code_blocks_are_escaped_and_kept_as_code(self):
        html = question_html("What is printed?\n```\nif a < b:\n    print('<b>')\n```")
        self.assertIn('<pre class="q-code">', html)
        self.assertIn('&lt;b&gt;', html)
        self.assertIn("    print(", html)
        self.assertNotIn('<b>', html.replace('<pre class="q-code">', ''))


class BuilderTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_build_is_repeatable_and_never_touches_admin_tests(self):
        call_command('build_test_content', exam=['SSC CGL'], verbosity=0)
        series = TestSeries.objects.get(exam='SSC CGL')
        mock = series.tests.get(title__startswith='SSC CGL Full Mock Test 1')
        self.assertEqual((mock.total_questions, mock.total_marks, mock.duration_minutes), (100, 200, 60))
        admin_test = Test.objects.create(test_series=series, title='Teacher upload', duration_minutes=10)
        Question.objects.create(test=admin_test, question_text='Hand-written question', options={'a': '1', 'b': '2'}, correct_answer={'answer': 'a'})
        first = series.tests.count()
        call_command('build_test_content', exam=['SSC CGL'], verbosity=0)
        self.assertTrue(Test.objects.filter(pk=admin_test.pk).exists())
        self.assertEqual(series.tests.count(), first)
        self.assertFalse(series.tests.filter(questions__isnull=True).exclude(pk=admin_test.pk).exists())

    def test_fractional_marks_series_page_renders_and_no_test_is_empty(self):
        # UPPSC PCS uses 1.33 marks per question, which used to crash the series page (float + Decimal).
        call_command('build_test_content', exam=['UPPSC PCS', 'GATE EC'], verbosity=0)
        series = TestSeries.objects.get(exam='UPPSC PCS')
        response = self.client.get(f'/exam-series/{series.pk}/')
        self.assertEqual(response.status_code, 200)
        mock = series.tests.get(title__startswith='UPPSC PCS Full Mock Test 1')
        self.assertEqual((mock.total_questions, mock.total_marks), (150, 200))  # 1.33/1.34 marks add up to the official 200
        self.assertFalse(Test.objects.filter(questions__isnull=True).exists())
        tita = Test.objects.get(test_series__exam='GATE EC', title__icontains='Type In The Answer')
        self.assertEqual(tita.questions.filter(question_type='numerical').count(), 10)


class CalculatorTests(TestCase):
    def test_exams_with_an_on_screen_calculator_get_one_and_others_do_not(self):
        cache.clear()
        call_command('build_test_content', exam=['TCS NQT', 'JEE Main'], verbosity=0)
        self.assertEqual(set(Test.objects.filter(test_series__exam='TCS NQT').values_list('calculator', flat=True)), {'basic'})
        self.assertEqual(set(Test.objects.filter(test_series__exam='JEE Main').values_list('calculator', flat=True)), {'none'})

        user = User.objects.create_user(email='calc@example.com', password='Str0ng!Passw0rd#2026')
        self.client.force_login(user)
        mock = Test.objects.get(test_series__exam='TCS NQT', is_demo=True)  # free, no purchase needed
        self.client.get(f'/exam/{mock.pk}/start/', secure=True)
        attempt = TestAttempt.objects.get(user=user, test=mock)
        page = self.client.get(f'/exam/session/{attempt.pk}/', secure=True, follow=True)
        self.assertContains(page, 'id="calc"')
        self.assertContains(page, 'Basic calculator')


class GradingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='candidate@example.com', password='Str0ng!Passw0rd#2026')
        self.series = TestSeries.objects.create(title='Grading', description='d', estimated_duration='1h', is_free=True, has_negative_marking=True)
        self.test = Test.objects.create(test_series=self.series, title='Paper', duration_minutes=30, shuffle_questions=False, max_attempts=3)
        self.num = Question.objects.create(test=self.test, question_text='Speed?', question_type='numerical', options={},
                                           correct_answer={'answer': '12.5'}, marks=Decimal('2.5'), negative_marks=Decimal('0.83'), order=1)
        self.mcq = Question.objects.create(test=self.test, question_text='Pick a', question_type='mcq_single', options={'a': 'A', 'b': 'B'},
                                           correct_answer={'answer': 'a'}, marks=Decimal('2.5'), negative_marks=Decimal('0.83'), order=2)
        self.test.update_stats()
        self.client.force_login(self.user)
        self.client.get(f'/exam/{self.test.pk}/start/', secure=True)
        self.attempt = TestAttempt.objects.get(user=self.user, test=self.test)

    def test_numerical_answers_match_by_value_and_fractional_marks_add_up(self):
        self.assertEqual(self.test.total_marks, 5)
        self.client.post(f'/exam/session/{self.attempt.pk}/submit/', {f'question_{self.num.pk}': '12.50', f'question_{self.mcq.pk}': 'b'}, secure=True)
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.correct_answers, 1)
        self.assertAlmostEqual(float(self.attempt.marks_obtained), 2.5 - 0.83, places=2)
