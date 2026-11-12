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


class ExamListTests(TestCase):
    """The exam list (exam_catalog.csv): every exam has a category and sub-category, new exams get light series."""

    def setUp(self):
        cache.clear()

    def test_every_catalog_exam_has_a_valid_pattern(self):
        from testseries.content.catalog import placement, rows
        from testseries.content.core import TOPICS

        load_all()
        names = {e.name for e in EXAMS}
        catalog = [r for r in rows() if r['kind'] == 'exam']
        self.assertGreater(len(catalog), 1000)
        for row in catalog:
            self.assertIn(row['exam'], names)
        for exam in EXAMS:
            self.assertTrue(exam.sections, exam.name)
            self.assertTrue(all(k in TOPICS for s in exam.sections for k in s.topics), exam.name)
            self.assertNotEqual(placement(exam.name)[0], '', exam.name)
        self.assertEqual(placement('SBI PO'), ('Banking', 'Bank PO/Clerical'))     # existing exam placed from the list
        self.assertEqual(placement('UPSC CMS')[0], 'Medical')                       # alias 'UPSC CMSE' -> existing exam

    def test_light_series_and_category_levels(self):
        call_command('build_test_content', exam=['IBPS SO Law Officer', 'GATE Biotechnology'], verbosity=0)
        series = TestSeries.objects.get(exam='IBPS SO Law Officer')
        titles = list(series.tests.values_list('title', flat=True))
        self.assertEqual(sum('Full Mock Test' in t for t in titles), 2)
        self.assertFalse(any('Sectional' in t or 'Previous Year' in t for t in titles))
        self.assertLessEqual(sum(t.startswith('Topic Test') for t in titles), 4)
        self.assertTrue(series.tests.filter(is_demo=True).exists())
        self.assertFalse(Test.objects.filter(questions__isnull=True).exists())
        from video_courses.models import Category
        category = Category.objects.get(name='IBPS SO Law Officer')
        self.assertEqual((category.group, category.sub_category), ('Banking', 'Bank Specialist Officer (SO)'))
        self.assertEqual(Test.objects.filter(test_series__exam='GATE Biotechnology', is_demo=False).first().calculator, 'scientific')

    def test_import_command_links_existing_exams(self):
        import csv
        import tempfile
        from pathlib import Path
        from unittest.mock import patch

        from testseries.management.commands import import_exam_catalog as importer

        src = Path(tempfile.mkdtemp()) / 'list.csv'
        out = Path(tempfile.mkdtemp()) / 'catalog.csv'
        with src.open('w', encoding='utf-8', newline='') as fh:
            writer = csv.writer(fh)
            writer.writerow(['L0 Name', 'L0_link', 'L1 Name', 'L1_link', 'L2 Name', 'L2_Link'])
            writer.writerow(['SSC', '', 'SSC (CGL - TIER 1 & 2)', '', 'SSC CGL', ''])
            writer.writerow(['Banking', '', 'Bank PO/Clerical', '', 'Bihar State Cooperative Bank', ''])
            writer.writerow(['New Level 0', '', 'Recruitment Test', '', 'Round 1', ''])
            writer.writerow(['School Level - State Boards', '', 'Goa Board', '', 'Goa Board Class XI', ''])
            writer.writerow(['School Level - All India', '', 'CBSE', '', 'CBSE Nursery', ''])
        with patch.object(importer, 'OUT', out):
            call_command('import_exam_catalog', str(src), verbosity=0)
        rows = list(csv.DictReader(out.open(encoding='utf-8')))
        self.assertEqual([(r['kind'], r['exam'], r['site_exam']) for r in rows if r['kind'] == 'exam'],
                         [('exam', 'SSC CGL', 'SSC CGL'), ('exam', 'Bihar State Cooperative Bank', '')])
        self.assertEqual(sorted((r['board'], r['grade'], r['stream']) for r in rows if r['kind'] == 'school'),
                         [('ga', '11', 'arts'), ('ga', '11', 'commerce'), ('ga', '11', 'science')])


class ExamMenuTests(TestCase):
    """Explore Exams: pages carry only the category tabs; exams, under sub-category headings, load with the menu."""

    def setUp(self):
        cache.clear()
        call_command('build_test_content', exam=['SBI PO', 'IBPS SO Law Officer', 'SSC CGL'], verbosity=0)

    def test_menu_loads_on_demand_with_sub_categories(self):
        home = self.client.get('/')
        self.assertContains(home, 'data-src="/exams/menu/"')
        self.assertNotContains(home, 'class="exam-menu-link"')
        menu = self.client.get('/exams/menu/').content.decode()
        self.assertIn('Bank PO/Clerical', menu)
        self.assertIn('Bank Specialist Officer (SO)', menu)
        self.assertIn('IBPS SO Law Officer', menu)
        mobile = self.client.get('/exams/menu/?v=mobile').content.decode()
        self.assertIn('mnav-chip', mobile)

    def test_catalogue_filters_by_exam_category(self):
        page = self.client.get('/test-series/?group=banking').content.decode()
        self.assertIn('IBPS SO Law Officer', page)
        self.assertNotIn('SSC CGL 2026', page)
