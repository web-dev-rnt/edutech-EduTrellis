"""Build the 2026 test series: full-length mocks, previous-year-pattern papers, sectional and topic-wise tests for every
competitive exam, and chapter-wise tests plus board mocks for every school board and class.

Safe to re-run. In each series it only replaces tests it built itself (slug starting 'gen-') and tests made entirely of
the old seed questions (those questions are folded into the new pools, so nothing is lost). Tests that students have
attempted, and tests an admin uploaded by hand, are never touched.
"""
import statistics
import time
from decimal import Decimal

from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Count
from django.utils.text import slugify

from testseries.boards import STATE_BOARDS
from testseries.content import load_all
from testseries.content.core import LETTERS, TOPICS, draw, seeded
from testseries.content.legacy import exam_key
from testseries.content.patterns import EXAMS
from testseries.content.school import legacy_keys, subjects_for
from testseries.exam_tools import EXAM_CALCULATORS
from testseries.stats import clear as stats_clear
from testseries.management.commands.seed_school_series import SUBJECTS
from testseries.models import Question, Subject, Test, TestSeries
from video_courses.models import Category

YEAR = 2026
TOPIC_TEST_SIZE = 10
MAX_TOPIC_TESTS = 40
EXTRA_MOCKS = 1        # full mocks built per exam = Exam.mocks + EXTRA_MOCKS
SCHOOL_BOARD_MOCKS = 3  # board-pattern mocks for Classes 9-12
SCHOOL_BOARDS = [('cbse', 'CBSE', 'CBSE'), ('icse', 'ICSE', 'ISC'), ('up', 'UP Board', 'UP Board')]


class Command(BaseCommand):
    help = __doc__.splitlines()[0]

    def add_arguments(self, parser):
        parser.add_argument('--only', choices=['exams', 'school', 'all'], default='all')
        parser.add_argument('--exam', action='append', default=[], help='Build just this exam (repeatable).')
        parser.add_argument('--board', action='append', default=[], help='Build just this board code, e.g. cbse, mp (repeatable).')
        parser.add_argument('--plan', action='store_true', help='Print how many tests and questions would be built, without writing.')

    def handle(self, *args, **opts):
        load_all()
        self.subjects = {
            code: Subject.objects.get_or_create(code=code, defaults={'name': name, 'color': color, 'icon': icon})[0]
            for code, (name, color, icon) in SUBJECTS.items()
        }
        self.legacy_texts = {row[0].strip().lower() for key, t in TOPICS.items()
                             if key.startswith(('exam.', 'school.', 'pool.')) for row in (t.rows or [])}
        self.plan = opts['plan']
        self.totals = {'series': 0, 'tests': 0, 'questions': 0, 'kept': 0}
        started = time.time()

        exams = [e for e in EXAMS if not opts['exam'] or e.name in opts['exam']]
        if opts['exam'] and len(exams) != len(opts['exam']):
            raise CommandError(f"Unknown exam. Choose from: {', '.join(e.name for e in EXAMS)}")
        if opts['only'] in ('exams', 'all') and not opts['board']:
            prices = [s.price for s in TestSeries.objects.exclude(exam='').filter(is_free=False)]
            self.default_price = statistics.median(prices) if prices else Decimal('199')
            for exam in exams:
                self.build_exam(exam)
        if opts['only'] in ('school', 'all') and not opts['exam']:
            self.build_school(set(opts['board']))

        cache.delete('site-navbar-categories')
        cache.delete('site-search-index-v2')
        stats_clear()
        self.stdout.write(self.style.SUCCESS(
            f"{'Planned' if self.plan else 'Built'} {self.totals['series']} series, {self.totals['tests']} tests, "
            f"{self.totals['questions']:,} questions ({self.totals['kept']} existing tests kept) in {time.time() - started:.0f}s."
        ))

    # ------------------------------------------------------------------ shared helpers

    def _clear(self, series):
        """Delete the tests this command may replace; return how many were kept."""
        kept = 0
        tests = series.tests.annotate(n_attempts=Count('attempts')).prefetch_related('questions')
        for test in tests:
            if test.n_attempts:
                kept += 1
                continue
            if test.slug.startswith('gen-') or all(q.question_text.strip().lower() in self.legacy_texts for q in test.questions.all()):
                test.delete()
            else:
                kept += 1
        self.totals['kept'] += kept
        return kept

    def _questions(self, sections, rng, used):
        """sections: [(subject code, marks, negative, [topic keys], count, numeric count)] -> [(code, marks, neg, Q)]."""
        out = []
        in_test = set()   # a question text appears at most once per test

        def fresh(qs):
            keep = []
            for q in qs:
                k = q.text.strip().lower()
                if k not in in_test:
                    in_test.add(k)
                    keep.append(q)
            return keep

        for code, marks, negative, topics, count, numeric in sections:
            topics = [t for t in topics if t in TOPICS]
            got = []
            if numeric:
                order = [t for t in topics if TOPICS[t].gen or TOPICS[t].numeric] or topics
                i = 0
                while len([q for q in got if q.kind == 'numerical']) < numeric and i < numeric * 12:
                    got += fresh(draw(order[i % len(order)], 1, rng, used, numeric_share=1.0))
                    i += 1
            mcq_needed = count - len(got)
            if mcq_needed > 0 and topics:
                shares = [mcq_needed // len(topics)] * len(topics)
                for i in rng.sample(range(len(topics)), mcq_needed % len(topics)):
                    shares[i] += 1
                for key, n in zip(topics, shares):
                    if n:
                        got += fresh([q for q in draw(key, n, rng, used) if q.kind != 'numerical'][:n])
                # Banks that ran dry: top up from topics that generate questions.
                refill = [t for t in topics if TOPICS[t].gen] or topics
                i = 0
                while len(got) < count and i < count * 10:
                    got += fresh([q for q in draw(refill[i % len(refill)], 1, rng, used) if q.kind != 'numerical'])
                    i += 1
            got = got[:count]
            mcq_part = [q for q in got if q.kind != 'numerical']
            rng.shuffle(mcq_part)
            numeric_part = [q for q in got if q.kind == 'numerical']
            out += [(code, marks, negative, q) for q in mcq_part + numeric_part]  # typed answers come last, as in the CBT
        return out

    def _make_test(self, series, title, description, minutes, paper_type, items, calculator='none', is_demo=False, attempts=3):
        self.totals['tests'] += 1
        self.totals['questions'] += len(items)
        if self.plan:
            return None
        slug = f"gen-{slugify(title)}"[:50].rstrip('-')
        taken = set(series.tests.values_list('slug', flat=True))
        base, n = slug[:46], 2
        while slug in taken:
            slug, n = f"{base}-{n}", n + 1
        test = Test.objects.create(
            test_series=series, title=title, slug=slug, description=description,
            duration_minutes=max(5, int(minutes)), max_attempts=attempts, shuffle_questions=False,
            paper_type=paper_type, calculator=calculator, is_demo=is_demo, show_result_immediately=True, allow_review=True,
        )
        rows = []
        # Marks are stored to 2 decimals. For papers like 200 marks / 150 questions (1.333…), give each question the
        # difference of the rounded running total, so most get 1.33, some 1.34, and the paper adds up to exactly 200.
        running, stored = 0.0, Decimal('0')
        for order, (code, marks, negative, q) in enumerate(items, start=1):
            running += marks
            upto = Decimal(str(round(running, 2)))
            marks, stored = upto - stored, upto
            if q.kind == 'numerical':
                options, answer = {}, {'answer': q.value}
                if '.' in q.value:
                    answer['tolerance'] = '0.01'
            else:
                options = dict(zip(LETTERS, q.options))
                answer = {'answer': LETTERS[q.answer]}
            rows.append(Question(
                test=test, subject=self.subjects.get(code), question_type=q.kind, difficulty=q.difficulty,
                question_text=q.text, marks=Decimal(str(marks)), negative_marks=Decimal(str(negative)),
                options=options, correct_answer=answer, explanation=q.explanation, order=order,
            ))
        Question.objects.bulk_create(rows, batch_size=500)
        test.update_stats()
        return test

    # ------------------------------------------------------------------ competitive exams

    def _exam_series(self, exam):
        series = TestSeries.objects.filter(exam=exam.name).order_by('pk').first()
        negatives = [s.negative for s in exam.sections if s.negative]
        fields = dict(
            title=f"{exam.name} {YEAR} – Full Mocks, PYQ Pattern Papers & Topic Tests",
            description=(f"Complete {exam.name} preparation in the {YEAR} pattern: full-length mock tests with the exact sections, "
                         f"question count, marking scheme and time limit, previous-year-pattern papers, sectional tests and topic-wise tests. "
                         f"Pattern: {exam.pattern}" + (f" {exam.note}" if exam.note else "")),
            difficulty=exam.difficulty,
            estimated_duration=f"{exam.minutes} minutes per full mock",
            has_negative_marking=bool(negatives),
            negative_marks=Decimal(str(max(negatives))) if negatives else Decimal('0'),
            pass_percentage=33,
        )
        if self.plan:
            return series or TestSeries(exam=exam.name, **fields)
        if series:
            for k, v in fields.items():
                setattr(series, k, v)
            series.save()
        else:
            hard = exam.difficulty in ('hard', 'expert')
            series = TestSeries.objects.create(
                exam=exam.name, slug=f"{slugify(exam.name)}-{YEAR}-test-series", is_free=False,
                price=Decimal('299') if hard else self.default_price, **fields,
            )
        category, created = Category.objects.get_or_create(
            name=exam.name, defaults={'icon': exam.icon, 'icon_color': exam.color, 'description': exam.pattern})
        if not created and category.description != exam.pattern:
            category.description = exam.pattern
            category.save(update_fields=['description'])
        return series

    @transaction.atomic
    def build_exam(self, exam):
        series = self._exam_series(exam)
        self.totals['series'] += 1
        if not self.plan:
            self._clear(series)
        rng = seeded('exam', exam.name, YEAR)
        used = set()
        calc = EXAM_CALCULATORS.get(exam.name, 'none')
        per_q = exam.minutes / exam.total

        def full_sections(sections=None):
            out = []
            for s in sections or exam.sections:
                legacy = [k for k in (exam_key(exam.name, s.code),) if k]
                out.append((s.code, s.marks, s.negative, legacy + s.topics + [f"pool.{s.code}"], s.count, s.numeric))
            return out

        summary = ", ".join(f"{s.name} {s.count}" for s in exam.sections)
        for i in range(1, exam.mocks + EXTRA_MOCKS + 1):
            self._make_test(series, f"{exam.name} Full Mock Test {i} ({YEAR} Pattern)",
                            f"Full-length mock exactly like the real paper – {exam.total} questions, {exam.total_marks:g} marks, "
                            f"{exam.minutes} minutes. Sections: {summary}.",
                            exam.minutes, 'mock', self._questions(full_sections(), rng, used), calc)
        for i in range(1, exam.pyp + 1):
            self._make_test(series, f"{exam.name} Previous Year Pattern Paper {i}",
                            f"Built on the topics and weightage asked in recent {exam.name} papers (2023–2025), in the {YEAR} pattern. "
                            "Original practice questions – not a reproduction of an official paper.",
                            exam.minutes, 'pyp', self._questions(full_sections(), rng, used), calc)

        if len(exam.sections) > 1:
            for s in exam.sections:
                if s.count < 10:
                    continue
                n = min(s.count, 50)
                code, marks, negative, topics, _, numeric = full_sections([s])[0]
                self._make_test(series, f"Sectional Test: {s.name}", f"{n} questions on {s.name} at the real exam's level and marking.",
                                round(per_q * n), 'subject', self._questions([(code, marks, negative, topics, n, min(numeric, n))], rng, used), calc)

        # Topic tests: take topics round-robin across sections so every section gets its share.
        queues = [[k for k in s.topics if k in TOPICS] for s in exam.sections]
        seen, keys_seen = [], set()
        while any(queues) and len(seen) < MAX_TOPIC_TESTS:
            for s, queue in zip(exam.sections, queues):
                while queue:
                    key = queue.pop(0)
                    if key not in keys_seen:
                        keys_seen.add(key)
                        seen.append((key, s))
                        break
                if len(seen) >= MAX_TOPIC_TESTS:
                    break
        for key, s in seen:
            label = TOPICS[key].label
            # Topics first met in a numerical-answer-only section (e.g. GATE NAT, 'type in the answer') get typed-answer tests.
            numeric = TOPIC_TEST_SIZE if s.numeric and s.numeric == s.count else 0
            items = self._questions([(s.code, s.marks, s.negative, [key], TOPIC_TEST_SIZE, numeric)], rng, used)
            if not items:
                continue
            self._make_test(series, f"Topic Test: {label}", f"{TOPIC_TEST_SIZE} questions on {label} for {exam.name}, with full solutions.",
                            max(8, round(per_q * TOPIC_TEST_SIZE)), 'topic', items, calc)

        demo_n = max(10, min(25, exam.total // 5))
        demo_sections = [(code, m, n, t, max(1, round(c * demo_n / exam.total)), 0) for code, m, n, t, c, _ in full_sections()]
        self._make_test(series, f"{exam.name} Free Demo Test", f"Try {demo_n} questions in the real {exam.name} format before you buy.",
                        max(10, round(per_q * demo_n)), 'mock', self._questions(demo_sections, seeded('demo', exam.name), set()), calc,
                        is_demo=True)
        if not self.plan:
            series.update_stats()
        self.stdout.write(f"  {exam.name}: done")

    # ------------------------------------------------------------------ school boards

    def build_school(self, only_boards):
        specs = []
        for code, board_name, senior in SCHOOL_BOARDS:
            for grade in range(1, 11):
                specs.append((code, board_name, grade, '', True, None))
            for grade in (11, 12):
                for stream in ('science', 'commerce', 'arts'):
                    specs.append((code, senior, grade, stream, True, None))
        for b in STATE_BOARDS:
            if not self.plan and (not only_boards or b.code in only_boards):
                # Each state board is its own 'Explore Exams' entry (boards added later need it created here).
                Category.objects.get_or_create(name=b.category, defaults={'icon': 'school', 'icon_color': '#0f766e', 'description': b.note})
            specs.append((b.code, b.label, 10, '', b.hindi, b))
            for stream in ('science', 'commerce', 'arts'):
                specs.append((b.code, b.label, 12, stream, b.hindi, b))
        for spec in specs:
            if not only_boards or spec[0] in only_boards:
                self.build_class(*spec)

    @transaction.atomic
    def build_class(self, board, board_name, grade, stream, hindi, state):
        stream_label = f" {stream.title()}" if stream else ''
        label = f"{board_name} Class {grade}{stream_label}"
        series = TestSeries.objects.filter(board=board, grade=grade, stream=stream).order_by('pk').first()
        subjects = subjects_for(board, grade, stream, hindi)
        names = ', '.join(name for _, name, _ in subjects)
        syllabus = ''
        if state:
            syllabus = (" The board follows NCERT(-based) textbooks, so tests follow the NCERT chapters." if state.ncert else
                        " The board has its own textbooks; tests cover the core chapters common to its syllabus and NCERT.")
            syllabus = f" {state.note}{syllabus}"
        description = (f"{label} ({YEAR}–{(YEAR + 1) % 100:02d} session): chapter-wise tests for {names}, a full test for every subject"
                       f"{' and board-pattern mock papers' if grade >= 9 else ' and an annual exam practice paper'}.{syllabus}")
        title = f"{label} – Chapter-wise Tests & {'Board Mocks' if grade >= 9 else 'Practice Papers'} ({YEAR})"
        self.totals['series'] += 1
        if not series:
            if self.plan:
                series = TestSeries(title=title)
            else:
                series = TestSeries.objects.create(
                    title=title, slug=slugify(f"{board}-class-{grade}{'-' + stream if stream else ''}-{YEAR}-test-series"),
                    board=board, grade=grade, stream=stream, description=description, estimated_duration='15–60 minutes per test',
                    is_free=False, price=Decimal('49') if grade <= 5 else Decimal('79') if grade <= 8 else Decimal('99') if grade <= 10 else Decimal('149'),
                    has_negative_marking=False, negative_marks=0, pass_percentage=33,
                )
        elif not self.plan:
            series.title, series.description = title, description
            series.difficulty = 'easy' if grade <= 5 else 'medium' if grade <= 10 else 'hard'
            series.estimated_duration = '15–60 minutes per test'
            series.has_negative_marking, series.negative_marks = False, 0
            series.save()
            self._clear(series)

        rng = seeded('school', board, grade, stream, YEAR)
        used = set()
        chapter_n = 10 if grade <= 8 else 15
        per_q = 1.0 if grade <= 8 else 1.2
        subject_n = 20 if grade <= 5 else 25 if grade <= 8 else 30

        for code, subject, chapters in subjects:
            legacy = legacy_keys(board, grade, code)
            all_topics = [k for _, keys in chapters for k in keys] + legacy
            for chapter, keys in chapters:
                self._make_test(series, f"{subject}: {chapter}", f"Chapter-wise test – {chapter} ({label} {subject}).",
                                round(per_q * chapter_n), 'topic', self._questions([(code, 1, 0, keys, chapter_n, 0)], rng, used))
            if legacy and sum(len(TOPICS[k].rows) for k in legacy) >= 8:
                self._make_test(series, f"{subject}: Board Pattern Practice", f"Board-exam style questions for {label} {subject}.",
                                round(per_q * chapter_n), 'topic', self._questions([(code, 1, 0, legacy, chapter_n, 0)], rng, used))
            self._make_test(series, f"{subject} – Full Subject Test", f"{subject_n} questions across all chapters of {label} {subject}.",
                            round(per_q * subject_n), 'subject', self._questions([(code, 1, 0, all_topics, subject_n, 0)], rng, used))

        per_subject = 6 if grade <= 8 else 10
        mix = [(code, 1, 0, [k for _, keys in chapters for k in keys] + legacy_keys(board, grade, code), per_subject, 0) for code, _, chapters in subjects]
        mock_n = per_subject * len(subjects)
        if grade >= 9:
            for i in range(1, SCHOOL_BOARD_MOCKS + 1):
                self._make_test(series, f"{label} Board Pattern Mock Test {i}",
                                f"Objective board-pattern paper covering {names}: {mock_n} questions.",
                                round(per_q * mock_n), 'mock', self._questions(mix, rng, used))
            if grade in (10, 12):
                self._make_test(series, f"{label} Previous Year Pattern Paper",
                                f"Questions on the topics board papers ask year after year, in the {YEAR} pattern. Original practice questions.",
                                round(per_q * mock_n), 'pyp', self._questions(mix, rng, used))
        else:
            self._make_test(series, f"{label} Annual Exam Practice Paper", f"Mixed paper covering {names}: {mock_n} questions.",
                            round(per_q * mock_n), 'mock', self._questions(mix, rng, used))
        demo = [(code, 1, 0, t, 2, 0) for code, _, _, t, _, _ in mix]
        self._make_test(series, "Free Demo Test", f"A free sample of {label} questions.", max(10, 2 * len(subjects)), 'mock',
                        self._questions(demo, seeded('demo', board, grade, stream), set()), is_demo=True)
        if not self.plan:
            series.update_stats()
        self.stdout.write(f"  {label}: done")
